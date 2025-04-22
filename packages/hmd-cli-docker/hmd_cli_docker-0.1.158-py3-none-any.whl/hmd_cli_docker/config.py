from pathlib import Path
from tempfile import gettempdir
from hmd_lib_containers.config.build_config import ImageBuildConfig, ImageBuildSecret
from hmd_cli_tools.hmd_cli_tools import read_manifest


def get_default_npm_secret(npmrc_name: str):
    return ImageBuildSecret(id="npmrc", src=npmrc_name)


def get_default_pip_secret(pip_conf_name: str):
    return ImageBuildSecret(id="pipconfig", src=pip_conf_name)


class HmdDockerDefaultBuildConfig(ImageBuildConfig):
    context_dir = Path(
        "./src/docker"
    )  # Remove this when all Dockerfiles have been updated

    @staticmethod
    def from_manifest():
        try:
            manifest = read_manifest()
        except Exception as e:
            manifest = {}

        docker_cfg = manifest.get("docker", {}).get(
            "build", {"context_dir": "./src/docker"}
        )
        # Convert secret dicts to ImageBuildSecret class
        if "secrets" in docker_cfg:
            docker_cfg["secrets"] = [
                ImageBuildSecret(id=secret["id"], src=secret["src"])
                for secret in docker_cfg["secrets"]
            ]
        else:
            docker_cfg["secrets"] = []

        build_secrets = manifest.get("build", {}).get("secrets", [])
        for secret in build_secrets:
            if secret["type"] == "file":
                docker_cfg["secrets"].append(
                    ImageBuildSecret(
                        id=secret["name"],
                        src=Path(gettempdir()) / "secrets" / secret["name"],
                    )
                )
            elif secret["type"] == "env":
                docker_cfg["secrets"].append(
                    ImageBuildSecret(
                        id=secret["env"],
                    )
                )
            elif secret["type"] == "envfile":
                docker_cfg["secrets"].append(
                    ImageBuildSecret(
                        id=secret["name"],
                        src=Path(gettempdir()) / "secrets" / secret["name"],
                    )
                )

        return HmdDockerDefaultBuildConfig(**docker_cfg)
