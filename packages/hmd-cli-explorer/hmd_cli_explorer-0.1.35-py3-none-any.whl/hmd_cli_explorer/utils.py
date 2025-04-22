from datetime import datetime
import os
from pathlib import Path
import shutil
from tempfile import gettempdir
from typing import Any, Dict, List
from urllib.parse import urljoin, urlparse, urlunparse
import zipfile
import io

import requests
import yaspin
import yaml
from hmd_cli_tools.hmd_cli_tools import (
    get_deployer_target_session,
    get_secret,
)
from hmd_lib_auth.hmd_lib_auth import okta_service_account_token_by_service
from hmd_cli_tools.okta_tools import get_auth_token


class ExplorerSession:
    def __init__(
        self, base_url: str, auth_token: str = None, login_params: Dict[str, Any] = None
    ) -> None:
        assert (
            auth_token is not None or login_params is not None
        ), "Must provide auth token or login params"
        self.base_url = base_url
        self.session = requests.session()

        if auth_token is None and login_params is not None:
            print(f"Logging into {self.base_url}...")
            login_resp = self.session.post(
                urljoin(base_url, "/api/v1/security/login"), json=login_params
            )
            auth_token = login_resp.json()["access_token"]

        self.base_headers = {
            "Authorization": f"Bearer {auth_token}",
            "Referer": self.base_url,
        }
        print(
            f"Getting CSRF Token for {urljoin(self.base_url, '/api/v1/security/csrf_token')}..."
        )
        csrf_token_resp = self.session.get(
            urljoin(self.base_url, "/api/v1/security/csrf_token"),
            headers=self.base_headers,
        )
        csrf_token_resp.raise_for_status()
        csrf_token = csrf_token_resp.json()["result"]

        self.base_headers["X-CSRFToken"] = csrf_token

    def get(self, url: str, headers: Dict[str, Any] = {}):
        resp = self.session.get(
            urljoin(self.base_url, url), headers={**self.base_headers, **headers}
        )
        resp.raise_for_status()

        return resp.json()

    def post(
        self, url: str, headers: Dict[str, Any] = {}, payload: Dict[str, Any] = {}
    ):
        resp = self.session.post(
            urljoin(self.base_url, url),
            headers={**self.base_headers, **headers},
            json=payload,
        )
        resp.raise_for_status()

        return resp.json()

    def post_files(
        self,
        url: str,
        headers: Dict[str, Any] = {},
        files: Dict[str, Any] = {},
        data: Dict[str, Any] = {},
    ):
        resp = self.session.post(
            urljoin(self.base_url, url),
            headers={**self.base_headers, **headers},
            files=files,
            data=data,
        )
        resp.raise_for_status()

        return resp.json()

    def export_zip(
        self, url: str, headers: Dict[str, Any] = {}, params: Dict[str, Any] = {}
    ):
        resp = self.session.get(
            urljoin(self.base_url, url),
            headers={**self.base_headers, **headers},
            params=params,
            stream=True,
        )
        export_zip = zipfile.ZipFile(io.BytesIO(resp.content))

        return export_zip


def get_explorer_session(
    base_url: str, auth_token: str = None, login_params: Dict[str, Any] = None
):
    return ExplorerSession(
        base_url=base_url, auth_token=auth_token, login_params=login_params
    )


def get_target_explorer_session(
    environment: str,
    customer_code: str,
    hmd_region: str,
    profile: str,
    account: str,
    config: dict,
    login_params: Dict[str, Any] = None,
    instance_name: str = "explorer",
    deployment_id: str = "aaa",
):
    if environment == "local":
        session = ExplorerSession(
            "http://localhost:8088/",
            login_params=login_params,
        )
    else:
        if config is None:
            config = {}
        svc_name = (
            config.get("dependencies", {})
            .get("explorer", {})
            .get("instance_name", instance_name)
        )
        base_url = (
            f"https://{svc_name}.{customer_code}-{environment}-neuronsphere.io",
        )
        aws_session = get_deployer_target_session(hmd_region, profile, account)
        try:
            admin_user_secret = get_secret(
                aws_session,
                f"{instance_name}-{deployment_id}-{environment}-admin-credentials",
            )

            session = ExplorerSession(
                base_url=base_url[0], login_params=admin_user_secret
            )
        except Exception as e:
            token = get_auth_token()
            session = ExplorerSession(base_url=base_url[0], auth_token=token)

    return session


def get_dashboard_ids(session: ExplorerSession, dashboard_names: List[str]):
    dashboards = session.get("/api/v1/dashboard").get("result", [])
    dashboards = list(
        filter(lambda d: d["dashboard_title"] in dashboard_names, dashboards)
    )
    return list(map(lambda d: str(d["id"]), dashboards))


def export_dashboards(
    session: ExplorerSession, project_root: Path, dashboard_names: List[str]
):
    with yaspin.yaspin(
        text=f"Exporting dashboards: {','.join(dashboard_names)}"
    ) as spinner:
        ids = get_dashboard_ids(session, dashboard_names)

        export_zip = session.export_zip(
            "/api/v1/dashboard/export", params={"q": f'!({",".join(ids)})'}
        )
        tmp_path = Path(gettempdir())
        export_dir = f'dashboard_export_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        export_path = tmp_path / export_dir
        export_zip.extractall(export_path)

        for dir_ in os.listdir(export_path):
            shutil.copytree(
                export_path / dir_,
                project_root / "src" / "explorer",
                dirs_exist_ok=True,
            )
        spinner.ok("✅ ")


def get_database_ids(session: ExplorerSession, database_names: List[str]):
    databases = session.get("/api/v1/database").get("result", [])
    databases = list(
        filter(lambda db: db["database_name"] in database_names, databases)
    )

    return list(map(lambda db: str(db["id"]), databases))


def get_database_dataset_ids(session: ExplorerSession, database_names: List[str]):
    db_ids = get_database_ids(session, database_names)
    datasets = session.get("/api/v1/dataset").get("result", [])

    datasets = list(
        filter(lambda ds: str(ds.get("database", {}).get("id", 0)) in db_ids, datasets)
    )

    return list(map(lambda ds: str(ds["id"]), datasets))


def export_databases(
    session: ExplorerSession, project_root: Path, database_names: List[str]
):
    with yaspin.yaspin(text=f"Exporting databases...") as spinner:
        ids = get_database_dataset_ids(session, database_names)

        export_zip = session.export_zip(
            "/api/v1/dataset/export", params={"q": f'!({",".join(ids)})'}
        )
        tmp_path = Path(gettempdir())
        export_dir = f'database_export_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        export_path = tmp_path / export_dir
        export_zip.extractall(export_path)

        prj_db_path = project_root / "src" / "explorer" / "databases"
        if not os.path.exists(prj_db_path):
            os.mkdir(prj_db_path)
        prj_dataset_path = project_root / "src" / "explorer" / "datasets"
        if not os.path.exists(prj_dataset_path):
            os.mkdir(prj_dataset_path)

        exported_dbs = export_path.rglob("*/databases/*.yaml")
        for exported_db in exported_dbs:
            shutil.copyfile(exported_db, prj_db_path / os.path.basename(exported_db))

        exported_datasets = export_path.rglob("*/datasets/**/*.yaml")
        for exported_data in exported_datasets:
            if not os.path.exists(prj_dataset_path / exported_data.parent.parts[-1]):
                os.mkdir(prj_dataset_path / exported_data.parent.parts[-1])
            shutil.copyfile(
                exported_data,
                prj_dataset_path
                / exported_data.parent.parts[-1]
                / os.path.basename(exported_data),
            )
        spinner.ok("✅ ")


def build_import_zip(
    assets_paths: Dict[str, Path], zip_path: Path, metadata: Dict[str, Any]
):
    zip_artifact = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    tmp_path = Path(gettempdir())
    import_path = f'explorer_import_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
    import_assets_path = tmp_path / import_path

    for asset_type, assets_path in assets_paths.items():
        for root, _, files in os.walk(assets_path):
            for asset in files:
                path_ = Path(root) / asset
                if path_.suffix == ".yaml":
                    zip_artifact.write(
                        Path(root) / asset,
                        Path("./explorer_assets")
                        / asset_type
                        / path_.relative_to(assets_path),
                    )
    if not os.path.exists(import_assets_path):
        os.mkdir(import_assets_path)

    metadata_path = import_assets_path / "metadata.yaml"
    with open(metadata_path, "w") as md:
        yaml.dump(metadata, md)

    zip_artifact.write(metadata_path, Path("./explorer_assets") / "metadata.yaml")
    zip_artifact.close()


def import_charts(session: ExplorerSession, project_root: Path):
    print("Importing charts...")
    zip_path = Path(gettempdir()) / "chart_import.zip"
    build_import_zip(
        {
            "charts": project_root / "src" / "explorer" / "charts",
            "databases": project_root / "src" / "explorer" / "databases",
            "datasets": project_root / "src" / "explorer" / "datasets",
        },
        zip_path,
        {
            "version": "1.0.0",
            "type": "Slice",
            "timestamp": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')}",
        },
    )
    session.post_files(
        "/api/v1/chart/import",
        data={"overwrite": "true"},
        files={"formData": ("import.zip", open(zip_path, "rb"), "application/zip")},
    )


def import_dashboards(session: ExplorerSession, project_root: Path):
    print("Importing dashboards...")
    zip_path = Path(gettempdir()) / "dashboard_import.zip"
    build_import_zip(
        {
            "charts": project_root / "src" / "explorer" / "charts",
            "databases": project_root / "src" / "explorer" / "databases",
            "datasets": project_root / "src" / "explorer" / "datasets",
            "dashboards": project_root / "src" / "explorer" / "dashboards",
        },
        zip_path,
        {
            "version": "1.0.0",
            "type": "Dashboard",
            "timestamp": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')}",
        },
    )
    session.post_files(
        "/api/v1/dashboard/import",
        data={"overwrite": "true"},
        files={"formData": ("import.zip", open(zip_path, "rb"), "application/zip")},
    )


def import_databases(
    session: ExplorerSession, project_root: Path, conn_overrides: Dict[str, Any]
):
    print("Importing databases...")
    for db, conn in conn_overrides.items():
        db_path = project_root / "src" / "explorer" / "databases" / f"{db}.yaml"
        if os.path.exists(db_path):
            with open(db_path, "r") as dbf:
                db_info = yaml.safe_load(dbf)
            conn_url = urlparse(db_info["sqlalchemy_uri"])
            hostname = conn_url.hostname
            port = conn_url.port
            username = conn_url.username
            conn_url = conn_url._replace(
                netloc=conn_url.netloc.replace(hostname, conn["hostname"])
                .replace(
                    str(port),
                    conn.get("port", port),
                )
                .replace(username, conn.get("username", username)),
                params=conn.get("params", conn_url.params),
                path=conn.get("path", conn_url.path),
            )
            db_info["sqlalchemy_uri"] = urlunparse(conn_url)

            with open(db_path, "w") as dbf:
                yaml.dump(db_info, dbf)

    zip_path = Path(gettempdir()) / "database_import.zip"
    build_import_zip(
        {
            "databases": project_root / "src" / "explorer" / "databases",
        },
        zip_path,
        {
            "version": "1.0.0",
            "type": "Database",
            "timestamp": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')}",
        },
    )
    session.post_files(
        "/api/v1/database/import",
        data={"overwrite": "true"},
        files={"formData": ("import.zip", open(zip_path, "rb"), "application/zip")},
    )


def import_datasets(session: ExplorerSession, project_root: Path):
    print("Importing datasets...")
    zip_path = Path(gettempdir()) / "dataset_import.zip"
    build_import_zip(
        {
            "databases": project_root / "src" / "explorer" / "databases",
            "datasets": project_root / "src" / "explorer" / "datasets",
        },
        zip_path,
        {
            "version": "1.0.0",
            "type": "SqlaTable",
            "timestamp": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')}",
        },
    )
    session.post_files(
        "/api/v1/dataset/import",
        data={"overwrite": "true"},
        files={"formData": ("import.zip", open(zip_path, "rb"), "application/zip")},
    )
