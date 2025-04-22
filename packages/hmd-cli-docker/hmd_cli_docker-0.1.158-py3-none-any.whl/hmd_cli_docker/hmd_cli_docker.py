import json
import os
from pathlib import Path
import platform
from typing import Any, Dict

from docker.errors import ImageNotFound
from cement import shell
from hmd_cli_tools.hmd_cli_tools import (
    cd,
    get_account_session,
    get_deployer_target_session,
    get_cloud_region,
    get_session,
    load_hmd_env,
)
from hmd_cli_tools.build_tools import build_dir
from hmd_lang_deployment.external_artifact import ExternalArtifact
from hmd_lib_containers.hmd_lib_containers import (
    build_image,
    publish_image,
    deploy_images,
    pull_images,
)

from .utils import (
    login_docker,
    get_docker_client,
    get_docker_registry,
    build_docker_tag,
    create_ecr_repository,
    pull_docker_image,
)
from .config import (
    HmdDockerDefaultBuildConfig,
    get_default_pip_secret,
    get_default_npm_secret,
)

TARGET_PLATFORMS = {
    "x86_64": "linux/amd64",
    "arm64": "linux/arm64",
}


def login(hmd_region: str, profile: str, registries: Dict[str, Any]):
    client = None
    for registry, value in registries.items():
        url = value.get("url")
        if url is None:
            raise Exception(f"Missing url in DOCKER_REGISTRIES: {registry}")

        registry_type = value.get("type")

        if registry_type == "ecr":
            session = get_deployer_target_session(
                hmd_region, profile, value.get("account")
            )
            client = session.client("ecr")

        username = value.get("username")
        if username is None and registry_type != "ecr":
            raise Exception(f"Missing username in DOCKER_REGISTRIES: {registry}")

        password = value.get("password")
        if password is None and registry_type != "ecr":
            raise Exception(f"Missing password in DOCKER_REGISTRIES: {registry}")

        login_docker(url, {"username": username, "password": password}, client)


def build(
    name: str,
    version: str,
    docker_username: str,
    docker_password: str,
    pip_username: str,
    pip_password: str,
    is_windows: bool,
    pip_compile_only: bool,
    build_args: Dict = {},
):
    load_hmd_env(override=False)
    if "VERSION" not in build_args:
        build_args["VERSION"] = version
    if "REPO_NAME" not in build_args:
        build_args["REPO_NAME"] = name

    docker_registry, docker_org = get_docker_registry()

    build_config = HmdDockerDefaultBuildConfig.from_manifest()
    install_local = build_config.install_local

    docker_dir = build_config.context_dir

    with build_dir(name):
        pip_conf_name = Path.home() / ".config" / "pip" / "pip.conf"
        npmrc_name = Path.home() / ".npmrc"

        if os.name == "nt":
            pip_conf_name = Path.home() / "pip" / "pip.ini"

        pip_conf_name = os.environ.get("PIP_CONFIG_FILE", pip_conf_name)

        if not pip_conf_name.exists():
            raise Exception("No pypi credentials.")

        pip_conf_name = str(pip_conf_name)

        if os.name == "nt":
            py_cmd = "python"
        else:
            py_cmd = "python3"

        if os.path.exists("src/docker/requirements.in"):
            with open("src/docker/requirements.in", "r") as reqs:
                input_reqs = reqs.read().splitlines()

            new_reqs = []  # if not local else local_reqs
            for req in input_reqs:
                if req.startswith(f"{name}=="):
                    if install_local:
                        continue
                    new_reqs.append(f"{name}=={version}")
                else:
                    new_reqs.append(req)

            print(new_reqs)
            reqs_file = "src/docker/requirements.in"  # if not local else "requirements_local.in"
            with open(reqs_file, "w") as reqs:
                reqs.writelines(f"{line}\n" for line in new_reqs)

            req_file = Path(os.getcwd()) / reqs_file
            command = [
                "pip-compile-multi",
                "-d",
                Path(os.getcwd()) / "src" / "docker",
                "-t",
                req_file,
                "--no-upgrade",
                "--no-annotate-index",
                "-c",
                "hmd-*",
            ]

            compiled_deps, stderr, exitcode = shell.exec_cmd(command, text=True)
            if exitcode != 0:
                raise Exception(f"Error evaluating dependencies. ({stderr})")

            if install_local:
                with open("src/docker/requirements.txt", "a") as reqs:
                    reqs.write(f"\n/src/python/")

        if pip_compile_only:
            return

        dockerfile = "./src/docker/Dockerfile"

        build_config.dockerfile = dockerfile

        if os.environ.get("HMD_DOCKER_SINGLE_ARCH", "false") == "true":
            current_arch = platform.machine()

            target_platform = TARGET_PLATFORMS.get(current_arch)

            if target_platform is not None:
                build_config.platforms = [target_platform]

        if is_windows:
            build_args["PIP_USERNAME_NT"] = pip_username
            build_args["PIP_PASSWORD_NT"] = pip_password

        build_config.build_args = {**build_config.build_args, **build_args}

        tag = build_docker_tag(
            docker_registry=docker_registry,
            docker_org=docker_org,
            name=name,
        )

        if not is_windows:
            build_config.secrets = [
                *build_config.secrets,
                get_default_pip_secret(str(pip_conf_name)),
            ]

            if os.path.exists(npmrc_name):
                build_config.secrets.append(get_default_npm_secret(npmrc_name))

        if os.environ.get("HMD_DOCKER_NETWORK") is not None:
            build_config.network = os.environ.get("HMD_DOCKER_NETWORK")

        build_image(tag, version, build_config)

    build_metadata_path = Path("./build/meta-data/")

    if not os.path.exists(build_metadata_path):
        os.makedirs(build_metadata_path, exist_ok=True)

    with open(build_metadata_path / "docker.ext_artifact.hmdentity", "w") as ea:
        ext_artifact = ExternalArtifact(
            name=name, tool="docker", external_location=f"{tag}:{version}"
        )
        json.dump(ext_artifact.serialize(), ea)


def publish(
    name: str,
    docker_username: str,
    docker_password: str,
    version: str,
    hmd_region: str,
    profile: str,
):
    docker_registry, docker_org = get_docker_registry()
    if docker_registry is None:
        docker_registry = docker_org
    tag = build_docker_tag(
        docker_registry=docker_registry,
        docker_org=docker_org,
        name=name,
    )

    ecr_client = None
    if "ecr." in docker_registry:
        account = docker_registry.split(".")[0]
        session = get_deployer_target_session(hmd_region, profile, account)
        ecr_client = session.client("ecr")

        tag = create_ecr_repository(name, ecr_client=ecr_client)

    # login to docker
    get_docker_client(
        docker_registry=docker_registry,
        username=docker_username,
        password=docker_password,
        ecr_client=ecr_client,
    )

    build_config = HmdDockerDefaultBuildConfig.from_manifest()

    publish_image(tag, version, build_config)


def deploy(
    name: str,
    docker_username: str,
    docker_password: str,
    version: str,
    profile: str,
    hmd_region: str,
    account: str,
    registries: Dict[str, Any] = {},
    target_platform: str = "linux/amd64",
):
    """Transfer an image from the hmd github repository to an AWS ECR. The HMD default
    image repo is in github, but when accessing images in AWS (as a lambda or in EKS)
    the image must be in ECR in the specific account.

    Args:
        name (str): the image name
        docker_username (str): github user name
        docker_password (str): github password
        version (str): image version
        profile (str): aws profile for the target
        region (str): the aws region for the target

    Raises:
        docker.errors.BuildError: [description]
    """

    valid_platforms = ["linux/amd64", "linux/arm64"]

    if target_platform is None:
        target_platform = valid_platforms[0]

    assert (
        target_platform in valid_platforms
    ), f"{target_platform} is not a valid platform options, please choose one of {valid_platforms}"

    ext_artifact_path = Path("./meta-data/docker.ext_artifact.hmdentity")

    if not os.path.exists(ext_artifact_path):
        docker_registry, docker_org = get_docker_registry()
        repository_name = build_docker_tag(
            docker_registry=docker_registry, docker_org=docker_org, name=name
        )
    else:
        with open(ext_artifact_path, "r") as ext:
            ext_dict = json.load(ext)
            ext_artifact: ExternalArtifact = ExternalArtifact.deserialize(
                ExternalArtifact, ext_dict
            )

            repository_name = ext_artifact.external_location
            docker_registry_info = repository_name.split("/")[:-1]
            if len(docker_registry_info) == 1:
                docker_registry = docker_registry_info[0]
                docker_org = None
            else:
                docker_registry = docker_registry_info[0]
                docker_org = docker_registry_info[1]

    aws_region = get_cloud_region(hmd_region)

    if "ecr." in docker_registry:
        aws_region = docker_registry.split(".")[3]

    session = get_session(aws_region, profile)
    source_ecr = session.client("ecr")

    docker_username = registries.get(docker_registry, {}).get(
        "username", docker_username
    )

    docker_password = registries.get(docker_registry, {}).get(
        "password", docker_password
    )

    build_config = HmdDockerDefaultBuildConfig.from_manifest()
    build_config.platforms = [target_platform]

    images = pull_docker_image(
        repository_name=repository_name.split(":")[0],
        version=version,
        docker_registry=docker_registry,
        build_config=build_config,
        username=docker_username,
        password=docker_password,
        ecr_client=source_ecr,
    )

    if len(images) == 0:
        for _, value in registries.items():
            url = value.get("url")

            if url is None:
                continue

            username = value.get("username")
            password = value.get("password")

            docker_registry = url.split("/")[0]

            images = pull_docker_image(
                f"{url}/{name}",
                version,
                docker_registry=docker_registry,
                username=username,
                password=password,
                ecr_client=source_ecr,
            )
            if images is not None:
                break

            if len(images) > 0:
                break

    if len(images) == 0:
        raise ImageNotFound

    # login to the target ecr
    aws_region = get_cloud_region(hmd_region)
    session = get_session(aws_region, profile)

    # the image has to be moved to the target account if specified...
    if account:
        session = get_account_session(
            session, account, "hmd.neuronsphere.deploy", aws_region
        )

    ecr_client = session.client("ecr")

    repo_uri = create_ecr_repository(name, ecr_client=ecr_client)
    login_docker(repo_uri, {}, ecr_client)

    print(f"Deploying {name}:{version} for platform: {target_platform}")

    deploy_images(
        images, repo_uri, version, build_config, target_platform=target_platform
    )


def release(
    name: str,
    docker_username: str,
    docker_password: str,
    version: str,
    profile: str,
    hmd_region: str,
    account: str,
    public_username: str,
    public_password: str,
):
    # login to the target ecr
    aws_region = get_cloud_region(hmd_region)
    session = get_session(aws_region, profile)

    # the image has to be moved to the target account if specified...
    if account:
        session = get_account_session(
            session, account, "hmd.neuronsphere.deploy", aws_region
        )

    ecr_client = session.client("ecr")

    docker_registry, docker_org = get_docker_registry()
    public_registry, public_org = get_docker_registry(
        envvar="HMD_RELEASE_CONTAINER_REGISTRY"
    )

    private_img_name = build_docker_tag(
        docker_registry=docker_registry, docker_org=docker_org, name=name
    )
    get_docker_client(
        docker_registry=docker_registry,
        username=docker_username,
        password=docker_password,
        ecr_client=ecr_client,
    )
    build_config = HmdDockerDefaultBuildConfig.from_manifest()

    private_image = pull_images(private_img_name, version, build_config)

    public_img_name = build_docker_tag(
        docker_registry=public_registry, docker_org=public_org, name=name
    )

    get_docker_client(
        docker_registry=public_registry,
        username=public_username,
        password=public_password,
        ecr_client=ecr_client,
    )

    deploy_images(private_image, public_img_name, version, build_config)
    deploy_images(private_image, public_img_name, "stable", build_config)
