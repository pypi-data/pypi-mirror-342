import os

from cement import Controller, ex
from importlib.metadata import version
from hmd_cli_tools.hmd_cli_tools import load_hmd_env
from hmd_cli_tools.credential_tools import get_credentials

VERSION_BANNER = """
hmd  version: {}
"""

VERSION = version("hmd_cli_bender")


class LocalController(Controller):
    class Meta:
        label = "bender"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "CLI for bender transform"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the  command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(VERSION),
                },
            ),
            (
                ["-ts", "--test-suite"],
                {
                    "action": "store",
                    "dest": "test_suite",
                    "help": "the name of the test suite where robot test files are stored",
                    "default": "*.robot",
                },
            ),
            (
                ["-i", "--include"],
                {
                    "action": "store",
                    "dest": "include",
                    "help": "the name of the tests within a suite that should be run",
                },
            ),
            (
                ["-ctx", "--transform-context-file"],
                {"action": "store", "dest": "context_file", "required": False},
            ),
        )

    def _default(self):
        """Run the bender transform."""
        load_hmd_env()

        args = {}
        name = self.app.pargs.repo_name
        repo_version = self.app.pargs.repo_version
        profile = self.app.pargs.profile
        context_file = self.app.pargs.context_file

        image_name = f"{os.environ.get('HMD_LOCAL_CONTAINER_REGISTRY', 'ghcr.io/neuronsphere')}/hmd-tf-bender:{os.environ.get('HMD_TF_BENDER_VERSION', 'stable')}"
        test_suite = self.app.pargs.test_suite
        include = self.app.pargs.include

        args.update(
            {
                "name": name,
                "version": repo_version,
                "image_name": image_name,
                "test_suite": test_suite,
                "profile": profile,
                "context_file": context_file,
            }
        )
        if include:
            args.update({"include": include})

        try:
            creds = get_credentials("docker", self.app.config)
            args.update(
                {
                    "docker_username": creds["username"],
                    "docker_password": creds["password"],
                }
            )
        except Exception as e:
            print("Docker credentials not found, continuing without docker repo auth")

        from .hmd_cli_bender import transform

        transform(**args)
