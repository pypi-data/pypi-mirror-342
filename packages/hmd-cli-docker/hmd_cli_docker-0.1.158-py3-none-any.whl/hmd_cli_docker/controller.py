import json
import os
from importlib.metadata import version

from cement import Controller, ex

from hmd_cli_tools.credential_tools import get_credentials
from hmd_cli_tools.hmd_cli_tools import (
    get_standard_parameters,
    set_pargs_value,
    set_hmd_env,
    load_hmd_env,
)
from hmd_cli_tools.prompt_tools import prompt_for_values

VERSION_BANNER = """
hmd docker version: {}
"""


build_arguments = [
    (
        ["--build-args"],
        {"action": "store", "dest": "build_args", "required": False, "nargs": "*"},
    ),
    (
        ["--is-windows"],
        {
            "action": "store_true",
            "dest": "is_windows",
            "required": False,
            "default": False,
        },
    ),
    (
        ["-pco", "--pip-compile-only"],
        {
            "action": "store_true",
            "dest": "pip_compile_only",
            "required": False,
            "default": False,
        },
    ),
]


class LocalController(Controller):
    class Meta:
        label = "docker"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Build and deploy docker images"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the docker command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_docker")),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(help="logins into multiple Docker registries", arguments=[])
    def login(self):
        registries = os.environ.get("DOCKER_REGISTRIES", "{}")

        from .hmd_cli_docker import login as do_login

        do_login(
            hmd_region=self.app.pargs.hmd_region,
            profile=self.app.pargs.profile,
            registries=json.loads(registries),
        )

    @ex(help="build a docker image", arguments=build_arguments)
    def build(self):
        args = {}
        name = self.app.pargs.repo_name
        version = self.app.pargs.repo_version

        # required because this can be called without going through the argparse stuff
        for _, arg_def in build_arguments:
            set_pargs_value(self.app.pargs, arg_def["dest"], arg_def.get("default"))

        is_windows = self.app.pargs.is_windows
        pip_compile_only = self.app.pargs.pip_compile_only
        args.update(
            {
                "name": name,
                "version": version,
                "is_windows": is_windows,
                "pip_compile_only": pip_compile_only,
            }
        )

        build_args = self.app.pargs.build_args
        if build_args:
            args.update({"build_args": dict([v.split(":") for v in build_args])})

        if is_windows:
            pip_username = os.environ.get("PIP_USERNAME_NT")
            pip_password = os.environ.get("PIP_PASSWORD_NT")
        else:
            pip_username = os.environ.get("PIP_USERNAME")
            pip_password = os.environ.get("PIP_PASSWORD")

        args.update({"pip_username": pip_username, "pip_password": pip_password})

        creds = get_credentials("docker", self.app.config, fail_if_not_found=False)
        if creds is None:
            creds = {"username": None, "password": None}
        args.update(
            {
                "docker_username": creds["username"],
                "docker_password": creds["password"],
            }
        )

        from .hmd_cli_docker import build as do_build

        do_build(**args)

    @ex(help="publish a docker image to the HMD image repo", arguments=[])
    def publish(self):
        args = {}
        name = self.app.pargs.repo_name
        version = self.app.pargs.repo_version

        creds = get_credentials("docker", self.app.config)
        docker_username = creds["username"]
        docker_password = creds["password"]

        args.update(
            {
                "docker_username": docker_username,
                "docker_password": docker_password,
                "version": version,
                "name": name,
                "hmd_region": self.app.pargs.hmd_region,
                "profile": self.app.pargs.profile,
            }
        )

        from .hmd_cli_docker import publish as do_publish

        do_publish(**args)

    @ex(
        help="migrate a docker image to aws",
        arguments=get_standard_parameters(["account", "config-file"]),
    )
    def deploy(self):
        args = {}
        name = self.app.pargs.repo_name
        version = self.app.pargs.repo_version
        profile = self.app.pargs.profile
        hmd_region = self.app.pargs.hmd_region
        account = self.app.pargs.account
        config_values = self.app.pargs.config_values

        if config_values is None:
            config_values = {}

        args.update({"name": name})

        creds = get_credentials("docker", self.app.config)
        docker_username = creds["username"]
        docker_password = creds["password"]

        args.update(
            {
                "docker_username": docker_username,
                "docker_password": docker_password,
                "version": version,
                "profile": profile,
                "hmd_region": hmd_region,
                "account": account,
                "target_platform": config_values.get("target_platform"),
            }
        )

        from .hmd_cli_docker import deploy as do_deploy

        do_deploy(**args)

    @ex(help="Destroy is a noop", arguments=get_standard_parameters(["account"]))
    def destroy(self):
        pass

    @ex(
        help="release a Docker image to the public",
        arguments=get_standard_parameters(["account"]),
    )
    def release(self):
        load_hmd_env()
        args = {}
        name = self.app.pargs.repo_name
        version = self.app.pargs.repo_version
        profile = self.app.pargs.profile
        hmd_region = self.app.pargs.hmd_region
        account = self.app.pargs.account

        args.update({"name": name})

        creds = get_credentials("docker", self.app.config)
        public_creds = get_credentials("docker_release", self.app.config)
        docker_username = creds["username"]
        docker_password = creds["password"]

        args.update(
            {
                "docker_username": docker_username,
                "docker_password": docker_password,
                "version": version,
                "profile": profile,
                "hmd_region": hmd_region,
                "account": account,
                "public_username": public_creds.get("username", docker_username),
                "public_password": public_creds.get("password", docker_password),
            }
        )

        from .hmd_cli_docker import release as do_release

        do_release(**args)

    @ex(help="configure hmd-cli-docker specific environment variables")
    def configure(self):
        config_vars = {
            "DOCKER_USERNAME": {"prompt": "Enter Docker username:"},
            "DOCKER_PASSWORD": {"prompt": "Enter Docker password:", "type": "password"},
            "HMD_CONTAINER_REGISTRY": {
                "hidden": True,
                "default": os.environ.get(
                    "HMD_CONTAINER_REGISTRY", "ghcr.io/neuronsphere"
                ),
            },
            "HMD_DOCKER_SINGLE_ARCH": {"hidden": True, "default": "true"},
        }

        results = prompt_for_values(config_vars)

        if results:
            for k, v in results.items():
                set_hmd_env(k, str(v))
