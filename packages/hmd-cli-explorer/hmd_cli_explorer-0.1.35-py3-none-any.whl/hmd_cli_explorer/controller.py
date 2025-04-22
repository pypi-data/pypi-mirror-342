import os
from typing import Dict

from cement import Controller, ex
from importlib.metadata import version
from hmd_cli_tools import get_version
from hmd_cli_tools.hmd_cli_tools import (
    get_standard_parameters,
    STANDARD_DEPLOY_PARAMETERS,
)

VERSION_BANNER = """
hmd explorer version: {}
"""

VERSION = version("hmd_cli_explorer")


class LocalController(Controller):
    class Meta:
        label = "explorer"
        aliases = ["expl"]
        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "CLI for managing Explorer portal assets"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the explorer command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(VERSION),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="build <...>",
    )
    def build(self):
        args = {}
        # build the args values...

        from .hmd_cli_explorer import build as do_build

        result = do_build(**args)

    @ex(help="publish an explorer project")
    def publish(self):
        from .hmd_cli_explorer import publish as do_publish

        result = do_publish()

    @ex(help="deploy Explorer assets", arguments=get_standard_parameters())
    def deploy(self):
        config_values: Dict = self.app.pargs.config_values
        args = {
            "environment": self.app.pargs.environment,
            "customer_code": self.app.pargs.customer_code,
            "account": self.app.pargs.account,
            "hmd_region": self.app.pargs.hmd_region,
            "profile": self.app.pargs.profile,
            "config_values": config_values,
        }

        from .hmd_cli_explorer import deploy as do_deploy

        do_deploy(**args)

    @ex(
        help="Export Dashboard from Explorer instance to local project. Must be called in root of project",
        arguments=[
            STANDARD_DEPLOY_PARAMETERS["environment"],
            STANDARD_DEPLOY_PARAMETERS["account"],
            STANDARD_DEPLOY_PARAMETERS["instance-name"],
            STANDARD_DEPLOY_PARAMETERS["deployment-id"],
            (
                ["dashboard_names"],
                {
                    "action": "store",
                    "nargs": "*",
                },
            ),
        ],
    )
    def export_dashboards(self):
        args = {
            "environment": self.app.pargs.environment,
            "customer_code": self.app.pargs.customer_code,
            "account": self.app.pargs.account,
            "hmd_region": self.app.pargs.hmd_region,
            "profile": self.app.pargs.profile,
            "dashboard_names": self.app.pargs.dashboard_names,
        }

        if self.app.pargs.instance_name is not None:
            args["instance_name"] = self.app.pargs.instance_name

        if self.app.pargs.deployment_id is not None:
            args["deployment_id"] = self.app.pargs.deployment_id

        from .hmd_cli_explorer import extract_dashboards as do_extract_dashboards

        do_extract_dashboards(**args)

    @ex(
        help="Export Database connections from Explorer instance to local project. Must be called in root of project",
        arguments=[
            STANDARD_DEPLOY_PARAMETERS["environment"],
            STANDARD_DEPLOY_PARAMETERS["account"],
            STANDARD_DEPLOY_PARAMETERS["instance-name"],
            STANDARD_DEPLOY_PARAMETERS["deployment-id"],
        ],
    )
    def export_databases(self):
        args = {
            "environment": self.app.pargs.environment,
            "customer_code": self.app.pargs.customer_code,
            "account": self.app.pargs.account,
            "hmd_region": self.app.pargs.hmd_region,
            "profile": self.app.pargs.profile,
        }
        if self.app.pargs.instance_name is not None:
            args["instance_name"] = self.app.pargs.instance_name

        if self.app.pargs.deployment_id is not None:
            args["deployment_id"] = self.app.pargs.deployment_id

        from .hmd_cli_explorer import extract_databases as do_extract_databases

        do_extract_databases(**args)
