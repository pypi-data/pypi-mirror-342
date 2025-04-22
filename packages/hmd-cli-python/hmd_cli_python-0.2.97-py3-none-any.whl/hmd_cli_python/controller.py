import json
import os
from importlib.metadata import version

from cement import Controller, ex

from hmd_cli_tools.hmd_cli_tools import get_standard_parameters, load_hmd_env


VERSION_BANNER = """
hmd docker version: {}
"""


class LocalController(Controller):
    class Meta:
        label = "python"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Build and deploy python packages"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the python command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_python")),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="login into multiple registries and edit pip config",
        arguments=get_standard_parameters(["account"]),
    )
    def login(self):
        load_hmd_env(override=False)
        from .hmd_cli_python import login as do_login

        registries = os.environ.get("PYTHON_REGISTRIES", "{}")
        default_username = os.environ.get("PIP_USERNAME")
        default_password = os.environ.get("PIP_PASSWORD")
        default_url = os.environ.get("PIP_EXTRA_INDEX_URL")

        do_login(
            hmd_region=self.app.pargs.hmd_region,
            profile=self.app.pargs.profile,
            registries=json.loads(registries),
            default_username=default_username,
            default_password=default_password,
            default_url=default_url,
        )

    @ex(help="deploy a python package", arguments=[])
    def publish(self):
        from .hmd_cli_python import publish as do_publish

        do_publish(repo_name=self.app.pargs.repo_name)

    @ex(
        label="build",
        help="Execute unit tests and build package.",
        arguments=[
            (
                ["-pco", "--pip-compile-only"],
                {
                    "action": "store_true",
                    "dest": "pip_compile_only",
                    "default": False,
                    "required": False,
                },
            ),
            (
                ["-ur", "--upload-results"],
                {
                    "action": "store_true",
                    "dest": "upload_results",
                    "default": False,
                    "required": False,
                },
            ),
        ],
    )
    def build(self):
        if not hasattr(self.app.pargs, "upload_results"):
            self.app.pargs.upload_results = False
        if not hasattr(self.app.pargs, "pip_compile_only"):
            self.app.pargs.pip_compile_only = False

        args = {
            "repo_name": self.app.pargs.repo_name,
            "command_name": self.Meta.label,
            "upload_results": self.app.pargs.upload_results,
            "pip_compile_only": self.app.pargs.pip_compile_only,
        }

        from .hmd_cli_python import build as do_build

        do_build(**args)

    @ex(label="install-local", help="Install Python package into local environment")
    def install_local(self):
        from .hmd_cli_python import install_local as do_install_local

        do_install_local(repo_name=self.app.pargs.repo_name)

    @ex(label="release", help="release a project to PyPI")
    def release(self):
        from .hmd_cli_python import release as do_release

        do_release(
            repo_name=self.app.pargs.repo_name, repo_version=self.app.pargs.repo_version
        )
