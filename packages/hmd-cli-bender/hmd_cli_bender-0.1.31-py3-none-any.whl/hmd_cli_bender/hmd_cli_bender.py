# Implement the lifecycle commands here
import os
import json
from pathlib import Path
from importlib.util import find_spec
import subprocess
from cement.utils.shell import exec_cmd2
from hmd_cli_tools.hmd_cli_tools import get_env_var
from hmd_cli_tools.okta_tools import get_auth_token
from typing import Dict
from tempfile import TemporaryDirectory
import urllib
import yaml
import traceback
import boto3

hmd_home = os.environ.get("HMD_HOME")


def get_local_package_mount(repo_name: str):
    pkg_path = find_spec(repo_name.replace("-", "_"))

    if pkg_path is None:
        return None

    return {
        "type": "bind",
        "source": str(Path.resolve(Path(pkg_path.get_filename()).parent)),
        "target": f"/usr/local/lib/python3.9/site-packages/{repo_name.replace('-', '_')}",
    }


def get_compose(
    image_name: str,
    instance_name: str,
    transform_instance_context: Dict,
    environment: str,
    region: str,
    customer_code: str,
    account: str,
    include: str,
    test_suite: str,
    repo_path: str,
    docker_secret: Path = None,
    pip_secret: str = None,
    auth_token: str = None,
):
    if not os.path.exists(os.path.join(os.environ["HMD_HOME"], ".cache", "bender")):
        os.mkdir(os.path.join(os.environ["HMD_HOME"], ".cache", "bender"))

    compose = {
        "version": "3.2",
        "services": {
            "bender_transform": {
                "image": image_name,
                "container_name": f"bender-inst_{instance_name}",
                "environment": {
                    "TRANSFORM_INSTANCE_CONTEXT": json.dumps(
                        transform_instance_context
                    ),
                    "HMD_ENVIRONMENT": environment,
                    "HMD_REGION": region,
                    "HMD_ACCOUNT": account,
                    "HMD_CUSTOMER_CODE": customer_code,
                    "HMD_HOME": "/root/hmd_home",
                    "HMD_CONTAINER_REGISTRY": os.environ.get("HMD_CONTAINER_REGISTRY"),
                    "INCLUDE": include,
                    "TEST_SUITE": test_suite,
                    "HMD_REPO_PATH": os.path.join(repo_path, "test"),
                    "PIP_CACHE_DIR": "/root/pip_cache",
                },
                "volumes": [
                    {
                        "type": "bind",
                        "source": repo_path,
                        "target": "/hmd_transform/input",
                    },
                    {
                        "type": "bind",
                        "source": repo_path,
                        "target": "/hmd_transform/output",
                    },
                    {
                        "type": "bind",
                        "source": os.path.join(repo_path, "test"),
                        "target": os.path.join(repo_path, "test"),
                    },
                    {
                        "type": "bind",
                        "source": "/var/run/docker.sock",
                        "target": "/var/run/docker.sock",
                    },
                    {
                        "type": "bind",
                        "source": "$HMD_HOME/.cache/bender/",
                        "target": "/root/pip_cache/",
                    },
                ],
                "secrets": [],
                "extra_hosts": ["host.docker.internal:host-gateway"],
            }
        },
        "networks": {},
    }

    # Check if local NeuronSphere is running and connect to the Docker network
    r = subprocess.run("docker network inspect neuronsphere_default".split(" "))

    if r.returncode == 0:
        compose["networks"]["neuronsphere"] = {
            "name": "neuronsphere_default",
            "external": True,
        }
        compose["services"]["bender_transform"]["networks"] = ["neuronsphere"]

    local_mnt = get_local_package_mount(
        repo_name=os.path.basename(os.path.abspath(repo_path))
    )

    if local_mnt is not None:
        compose["services"]["bender_transform"]["volumes"].append(local_mnt)

    if auth_token is not None:
        compose["services"]["bender_transform"]["environment"][
            "HMD_AUTH_TOKEN"
        ] = auth_token

    try:
        aws_profile = os.environ.get("AWS_PROFILE")
        if hmd_home and aws_profile:
            session = boto3.Session(profile_name=aws_profile)
            creds = session.get_credentials()

            if creds.access_key:
                compose["services"]["bender_transform"]["environment"][
                    "AWS_ACCESS_KEY_ID"
                ] = creds.access_key
            if creds.secret_key:
                compose["services"]["bender_transform"]["environment"][
                    "AWS_SECRET_ACCESS_KEY"
                ] = creds.secret_key
            if creds.token:
                compose["services"]["bender_transform"]["environment"][
                    "AWS_SESSION_TOKEN"
                ] = creds.token
    except:
        pass

    secrets = {"secrets": {}}

    if docker_secret:
        secrets["secrets"].update({"docker_repo": {"file": docker_secret}})
        compose["services"]["bender_transform"]["secrets"].append("docker_repo")
        compose["services"]["bender_transform"]["environment"].update(
            {"DOCKER_REPO": "/run/secrets/docker_repo"}
        )
    if pip_secret:
        secrets["secrets"].update({"pip_url": {"file": pip_secret}})
        compose["services"]["bender_transform"]["secrets"].append("pip_url")
        compose["services"]["bender_transform"]["environment"].update(
            {"PIP_CONF": "/run/secrets/pip_url"}
        )
    compose.update(secrets)

    return compose


def transform(
    name: str,
    version: str,
    image_name: str,
    test_suite: str,
    profile: str,
    include: str = None,
    docker_username: str = None,
    docker_password: str = None,
    context_file: str = None,
):
    if hmd_home:
        instance_name = os.environ.get("HMD_INSTANCE_NAME", f"{name}")
        deployment_id = os.environ.get("HMD_DID", "aaa")
        hmd_env = os.environ.get("HMD_ENVIRONMENT", "local")
        region = os.environ.get("HMD_REGION", "reg1")
        cust_code = os.environ.get("HMD_CUSTOMER_CODE", "hmd")
        account = os.environ.get("HMD_ACCOUNT", "")
        auth_token = get_auth_token()
    else:
        instance_name = get_env_var("HMD_INSTANCE_NAME")
        deployment_id = get_env_var("HMD_DID")
        hmd_env = get_env_var("HMD_ENVIRONMENT")
        region = get_env_var("HMD_REGION")
        cust_code = get_env_var("HMD_CUSTOMER_CODE")
        account = os.environ.get("HMD_ACCOUNT", "")

    repo_path = os.getcwd()

    transform_instance_context = {
        "instance_name": instance_name.replace("-", "_"),
        "repo_name": name,
        "version": version,
        "deployment_id": deployment_id,
    }

    extra_context = {}

    if context_file is None:
        context_file = Path(repo_path) / "test" / "local_context.json"

    if not os.path.exists(context_file):
        context_file = Path(repo_path) / "meta-data" / "config_local.json"

    if context_file is not None and os.path.exists(context_file):
        with open(context_file, "r") as ctx:
            extra_context = json.load(ctx)

    transform_instance_context = {**transform_instance_context, **extra_context}

    pip_username = os.environ.get("PIP_USERNAME")
    pip_password = os.environ.get("PIP_PASSWORD")

    try:
        with TemporaryDirectory() as tempdir:
            pip_config = None
            docker_config = None
            if pip_username and pip_password:
                pip_conf = f"""
[global]
extra-index-url = https://{pip_username}:{urllib.parse.quote(pip_password)}@hmdlabs.jfrog.io/artifactory/api/pypi/hmd_pypi/simple"""
                pip_config = os.path.join(tempdir, "pip.conf")
                with open(pip_config, "w") as pip:
                    pip.write(pip_conf)
            else:
                if os.name == "nt":
                    pip_config = os.path.join(Path.home(), "pip", "pip.ini")
                else:
                    pip_config = Path.home() / ".pip" / "pip.conf"

            if docker_username and docker_password:
                docker_conf = {
                    "docker": {"username": docker_username, "password": docker_password}
                }
                docker_config = os.path.join(tempdir, ".hmd.yml")
                with open(docker_config, "w") as dock:
                    yaml.safe_dump(docker_conf, dock)

            compose = get_compose(
                image_name=image_name,
                instance_name=instance_name,
                transform_instance_context=transform_instance_context,
                environment=hmd_env,
                region=region,
                customer_code=cust_code,
                account=account,
                include=include,
                test_suite=test_suite,
                repo_path=repo_path,
                docker_secret=docker_config,
                pip_secret=str(pip_config),
                auth_token=auth_token,
            )

            inst_config = Path(repo_path) / "bender" / "docker-compose.yaml"
            if not inst_config.parent.exists():
                os.makedirs(inst_config.parent)
            with open(inst_config, "w") as conf:
                yaml.safe_dump(compose, conf)

            command = [
                "docker-compose",
                "--project-name",
                "neuronsphere_bender",
                "--file",
                inst_config,
                "up",
                "--force-recreate",
            ]
            return_code = exec_cmd2(command)

        if return_code != 0:
            raise Exception(f"Process completed with non-zero exit code: {return_code}")

        rm_command = ["docker-compose", "--file", inst_config, "rm", "-f"]
        return_code = exec_cmd2(rm_command)

        if return_code != 0:
            raise Exception(
                f"Docker compose remove finished with non-zero exit code: {return_code}"
            )

    except Exception:
        print(f"Exception occurred running transform: {traceback.format_exc()}")
