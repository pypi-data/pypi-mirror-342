# Implement the lifecycle commands here
import json
import os
from pathlib import Path
import shutil
from hmd_cli_tools import cd
from typing import Dict, List, Any

import yaml

from hmd_cli_explorer.utils import (
    ExplorerSession,
    get_target_explorer_session,
    export_dashboards,
    export_databases,
    import_databases,
    import_datasets,
    import_dashboards,
    import_charts,
)
from hmd_cli_tools.hmd_cli_tools import (
    read_manifest,
    make_standard_name,
    get_deployer_target_session,
    get_secret,
)
from hmd_cli_tools.cdktf_tools import DeploymentConfig, db_secret_name_from_dependencies


LOCAL_LOGIN = {
    "username": "admin",
    "password": "admin",
    "refresh": True,
    "provider": "db",
}


def build():
    """Adds Explorer assets in ./src/explorer to build artifact"""
    shutil.copytree("./src/explorer", "./build/src/explorer/")


def publish():
    pass


def deploy(
    environment: str,
    customer_code: str,
    profile: str,
    hmd_region: str,
    account: str,
    config_values: Dict[str, Any],
):
    """Imports assets into Explorer instance running in the target environment.

    Args:
        environment (str): target deployment environment
        customer_code (str): target environment customer code
        config_values (Dict[str, Any]): deployment configuration
    """
    project_root = Path(os.getcwd())
    dp_config = DeploymentConfig(config_values)
    session = get_target_explorer_session(
        environment=environment,
        customer_code=customer_code,
        hmd_region=hmd_region,
        profile=profile,
        account=account,
        config=config_values,
        login_params=LOCAL_LOGIN if environment == "local" else None,
        instance_name=dp_config.get("explorer", {}).get("instance_name"),
        deployment_id=dp_config.get("explorer", {}).get("deployment_id", "aaa"),
    )
    assets = config_values.get("explorer_assets", [])
    if len(assets) == 0:
        print(
            f"WARNING: No explorer_assets found in deployment config. Exiting and doing nothing."
        )
        return

    aws_session = get_deployer_target_session(
        hmd_region=hmd_region, profile=profile, account=account
    )

    if "databases" in assets:
        conn_overrides = {}
        cfg_overrides = config_values.get("database_overrides", {})
        for k, v in config_values.get("dependencies", {}).items():
            if v.get("repo_class_name") == "hmd-inf-trino":
                hostname_default = "{instance_name}-{deployment_id}-{repo_name}.{instance_name}-{deployment_id}.svc.cluster.local"
                creds_instance = v.get("users", [])
                if isinstance(creds_instance, list) and len(creds_instance) > 0:
                    creds_instance = creds_instance[0]

                try:
                    creds_secret = get_secret(
                        aws_session,
                        make_standard_name(
                            creds_instance["instance_name"],
                            creds_instance["repo_class_name"],
                            creds_instance["deployment_id"],
                            environment,
                            hmd_region,
                            customer_code,
                        ),
                    )
                    db_override = cfg_overrides.get(k, {})
                    conn_overrides[k] = {
                        "hostname": db_override.get(
                            "hostname", hostname_default
                        ).format(**v),
                        "username": db_override.get(
                            "user", creds_secret.get("username")
                        ),
                        "password": creds_secret.get("password"),
                        "port": db_override.get("port", ""),
                        "path": db_override.get("path", ""),
                        "params": db_override.get("params", ""),
                    }
                except Exception as e:
                    print(e)
            elif v.get("repo_class_name") == "hmd-database-account":
                try:
                    creds_secret = get_secret(
                        aws_session,
                        db_secret_name_from_dependencies(
                            dp_config.get(k), environment, hmd_region, customer_code
                        ),
                    )
                    db_override = cfg_overrides.get(k, {})
                    conn_overrides[k] = {
                        "hostname": db_override.get(
                            "hostname", creds_secret.get("host")
                        ).format(**v),
                        "username": db_override.get(
                            "user", creds_secret.get("username")
                        ),
                        "password": creds_secret.get("password"),
                        "port": db_override.get("port", creds_secret.get("port")),
                        "path": db_override.get("path", ""),
                        "params": db_override.get("params", ""),
                    }
                except Exception as e:
                    print(e)
        import_databases(
            session=session,
            project_root=project_root,
            conn_overrides=conn_overrides,
        )

    if "datasets" in assets:
        import_datasets(session=session, project_root=project_root)

    if "charts" in assets:
        import_charts(session=session, project_root=project_root)

    if "dashboards" in assets:
        import_dashboards(session=session, project_root=project_root)


def extract_dashboards(
    environment: str,
    customer_code: str,
    profile: str,
    hmd_region: str,
    account: str,
    dashboard_names: List[str] = None,
    instance_name: str = "explorer",
    deployment_id: str = "aaa",
):
    """Exports one or more dashboards from an Explorer instance

    Args:
        environment (str): target environment where Explorer is deployed
        customer_code (str): customer code for target environment
        profile (str): AWS profile to use
        hmd_region (str): HMD region Explorer is deployed in
        account (str): AWS account number
        dashboard_names (List[str], optional): list of dashboard titles to export. Defaults to None.

    Raises:
        Exception: _description_
    """
    session = get_target_explorer_session(
        environment=environment,
        customer_code=customer_code,
        hmd_region=hmd_region,
        profile=profile,
        account=account,
        config=None,
        login_params=LOCAL_LOGIN,
        instance_name=instance_name,
        deployment_id=deployment_id,
    )

    project_root = Path(os.getcwd())

    if len(dashboard_names) == 0:
        dashboard_path = project_root / "src" / "explorer" / "dashboards"
        if not os.path.exists(dashboard_path):
            raise Exception(
                "No Dashboards passed as arguments, and cannot locate files at ./src/explorer/dashboards/"
            )

        dashboard_files = os.listdir(dashboard_path)
        for dashboard in dashboard_files:
            with open(dashboard_path / dashboard, "r") as df:
                dashboard_data = yaml.safe_load(df)
                dashboard_names.append(dashboard_data["dashboard_title"])

    export_dashboards(
        session=session, project_root=project_root, dashboard_names=dashboard_names
    )


def extract_databases(
    environment: str,
    customer_code: str,
    profile: str,
    hmd_region: str,
    account: str,
    instance_name: str = "explorer",
    deployment_id: str = "aaa",
):
    """Exports database connections and related datasets based on deployment dependencies

    Args:
        environment (str): target environment where Explorer is deployed
        customer_code (str): customer code for target environment
        profile (str): AWS profile to use
        hmd_region (str): HMD region Explorer is deployed in
        account (str): AWS account number
    """
    project_root = Path(os.getcwd())

    manifest = read_manifest()
    dependencies = manifest.get("deploy", {}).get("dependencies", {})

    session = get_target_explorer_session(
        environment=environment,
        customer_code=customer_code,
        hmd_region=hmd_region,
        profile=profile,
        account=account,
        config=None,
        login_params=LOCAL_LOGIN,
        instance_name=instance_name,
        deployment_id=deployment_id,
    )

    export_databases(
        session, project_root=project_root, database_names=dependencies.keys()
    )
