import os
from base64 import b64decode
from typing import Any, Dict

import docker
from docker.errors import ImageNotFound
from cement.utils.shell import exec_cmd2

from hmd_lib_containers.hmd_lib_containers import pull_images, get_client

from .config import HmdDockerDefaultBuildConfig


def get_docker_registry(envvar: str = "HMD_CONTAINER_REGISTRY"):
    docker_registry = os.environ.get(envvar, "ghcr.io/hmdlabs")

    if "/" in docker_registry:
        docker_registry_parts = docker_registry.split("/")
        return docker_registry_parts[0], docker_registry_parts[1]

    return None, docker_registry


def build_docker_tag(docker_registry=None, docker_org=None, name=""):
    tag = f"{docker_registry}/{docker_org}/{name}"
    if docker_registry is None:
        tag = f"{docker_org}/{name}"

    return tag


def get_docker_client(
    docker_registry: str, username: str = None, password: str = None, ecr_client=None
):
    docker_client = get_client()
    if "ecr." in docker_registry and ecr_client is not None:
        # get ecr credentials to use with docker...
        response = ecr_client.get_authorization_token()
        if len(response["authorizationData"]) != 1:
            raise Exception(
                "Unable to get AWS athorization token for the default registry."
            )

        token = b64decode(
            response["authorizationData"][0]["authorizationToken"]
        ).decode("utf-8")
        user_name, token = token.split(":", maxsplit=1)
        username = user_name
        password = token

    docker_client.login(username=username, password=password, server=docker_registry)

    # login_docker(
    #     docker_registry=docker_registry,
    #     info={"username": username, "password": password},
    #     ecr_client=ecr_client,
    # )

    print("Login succeeded")

    return docker_client


def login_docker(docker_registry: str, info: Dict[str, Any], ecr_client=None):
    username = info.get("username", "")
    password = info.get("password", "")
    if "ecr." in docker_registry and ecr_client is not None:
        # get ecr credentials to use with docker...
        response = ecr_client.get_authorization_token()
        if len(response["authorizationData"]) != 1:
            raise Exception(
                "Unable to get AWS athorization token for the default registry."
            )

        token = b64decode(
            response["authorizationData"][0]["authorizationToken"]
        ).decode("utf-8")
        user_name, token = token.split(":", maxsplit=1)
        username = user_name
        password = token

    if "/" in docker_registry:
        docker_registry = docker_registry.split("/")[0]

    command = [
        "docker",
        "login",
        docker_registry,
        "--username",
        username,
        "--password",
        password,
    ]

    return_code = exec_cmd2(command)
    if return_code != 0:
        raise docker.errors.BuildError(
            f"Error logging in to Docker. {docker_registry}", None
        )


def create_ecr_repository(name: str, ecr_client=None):
    try:
        repos = ecr_client.describe_repositories(repositoryNames=[name])
        repo = repos["repositories"][0]
        repo_uri = repo["repositoryUri"]

        if not repo["imageScanningConfiguration"]["scanOnPush"]:
            ecr_client.put_image_scanning_configuration(
                registryId=repo["registryId"],
                repositoryName=repo["repositoryName"],
                imageScanningConfiguration={"scanOnPush": True},
            )
    except ecr_client.exceptions.RepositoryNotFoundException as e:
        repo_uri = ecr_client.create_repository(
            repositoryName=name, imageScanningConfiguration={"scanOnPush": True}
        )["repository"]["repositoryUri"]

    return repo_uri


def pull_docker_image(
    repository_name: str,
    version: str,
    docker_registry: str,
    build_config: HmdDockerDefaultBuildConfig,
    username: str = None,
    password: str = None,
    ecr_client=None,
):
    try:
        get_docker_client(
            docker_registry=docker_registry,
            username=username,
            password=password,
            ecr_client=ecr_client,
        )
        # image = docker_client.images.pull(repository=repository_name, tag=version)
        images = pull_images(repository_name, version, build_config)
        return images
    except ImageNotFound as e:
        return None
