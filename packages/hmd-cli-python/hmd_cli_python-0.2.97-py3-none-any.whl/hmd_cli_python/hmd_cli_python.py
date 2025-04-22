import os
from pathlib import Path
import configparser
import shutil
from typing import Any, Dict, List
from urllib.parse import urlparse, urlunparse

from cement.utils import shell
from setuptools import find_packages

from hmd_cli_tools import cd, get_version
from hmd_cli_tools.build_tools import build_dir
from hmd_cli_tools.hmd_cli_tools import get_cloud_region, get_session


def publish(repo_name: str):
    with build_dir(repo_name):
        with cd("./src/python"):
            exitcode = shell.exec_cmd2(
                ["twine", "upload", "-r", "neuronsphere", "dist/*"]
            )
            if exitcode != 0:
                raise Exception("Error uploading distribution.")


def update_setup_py(requirements: List[str]):
    with open("setup.py", "r") as setup:
        setup_data = setup.read().splitlines()

    output = []
    found = False
    for line in setup_data:
        if line.strip().startswith("install_requires=[]"):
            found = True
            indent = line.index("install")
            output.append((" " * indent) + "install_requires=[")
            for req in requirements:
                if not req.strip().startswith("#"):
                    output.append((" " * (indent + 4)) + f'"{req}",')
            output.append((" " * indent) + "]")
        else:
            output.append(line)
    if not found:
        raise Exception("setup.py doesn't contain an empty 'install_requires' line.")
    with open("setup.py", "w") as setup:
        setup.writelines(f"{line}\n" for line in output)


def compile_requirements():
    compiled_deps = None
    if os.path.exists("requirements.in"):
        req_file = Path(os.getcwd()) / "requirements.in"
        command = [
            "pip-compile-multi",
            "-d",
            os.getcwd(),
            "-t",
            req_file,
            "--no-upgrade",
            "--no-annotate-index",
            "-c",
            "hmd-*",
        ]

        compiled_deps, stderr, exitcode = shell.exec_cmd(command)
        if exitcode != 0:
            raise Exception(f"Error evaluating dependencies. ({stderr.decode()})")

        with open("requirements.txt", "r") as fl:
            compiled_deps = fl.read().splitlines()

    return compiled_deps


def fetch_codeartifact_token(
    hmd_region: str, profile: str, domain: str, account: str, repository: str
):
    aws_region = get_cloud_region(hmd_region)
    session = get_session(aws_region, profile)
    client = session.client("codeartifact")

    response = client.get_authorization_token(domain=domain, domainOwner=account)
    token = response["authorizationToken"]
    return token


def login(
    hmd_region: str,
    profile: str,
    registries: Dict[str, Any],
    default_username: str,
    default_password: str,
    default_url: str,
):
    pip_conf_name = Path.home() / ".config" / "pip" / "pip.conf"

    if os.name == "nt":
        pip_conf_name = Path.home() / ".pip" / "pip.ini"

    pip_conf_name = Path(os.environ.get("PIP_CONFIG_FILE", pip_conf_name))

    if not os.path.exists(pip_conf_name):
        pip_conf_name.parent.mkdir(parents=True, exist_ok=True)

    extra_index_urls = []
    registry_urls = []
    twine_urls = []

    for registry, config in registries.items():
        registry_type = config.get("type", None)

        if "url" not in config:
            raise Exception(f"Invalid configuration in PYTHON_REGISTRIES: {registry}")

        url_parts = urlparse(config["url"])
        registry_urls.append(url_parts.hostname)
        print(config["url"], url_parts)

        if registry_type == "codeartifact":
            token = fetch_codeartifact_token(
                hmd_region,
                profile,
                config["domain"],
                config["account"],
                config["repository"],
            )

            if config.get("publish", False):
                twine_urls.append(
                    (
                        urlunparse(
                            url_parts._replace(
                                path=url_parts.path.replace("simple/", "")
                            )
                        ),
                        "aws",
                        token,
                    )
                )

            url_parts = url_parts._replace(netloc=f"aws:{token}@{url_parts.hostname}")
            extra_index_urls.append(urlunparse(url_parts))
        else:
            username = config["username"]
            password = config["password"]

            if config.get("publish", False):
                twine_urls.append(
                    (
                        urlunparse(
                            url_parts._replace(
                                path=url_parts.path.replace("simple/", "")
                            )
                        ),
                        username,
                        password,
                    )
                )

            url_parts = url_parts._replace(
                netloc=f"{username}:{password}@{url_parts.hostname}"
            )
            extra_index_urls.append(urlunparse(url_parts))

    pip_config = configparser.ConfigParser()
    pip_config.read(pip_conf_name)

    extra_urls = []
    if "global" in pip_config:
        extra_urls = pip_config.get("global", "extra-index-url")
        if not isinstance(extra_urls, list):
            extra_urls = extra_urls.split("\n")
    else:
        pip_config["global"] = {}

    existing_urls = list(
        filter(lambda u: urlparse(u.strip()).hostname not in registry_urls, extra_urls)
    )
    pip_config["global"]["extra-index-url"] = "\n".join(
        [*existing_urls, *extra_index_urls]
    )
    with open(pip_conf_name, "w") as pc:
        pip_config.write(pc)

    if len(twine_urls) > 0:
        if not os.path.exists(Path.home() / ".pypirc"):
            with open(Path.home() / ".pypirc", "w") as twine:
                cfg = f"""
[distutils]
index-servers =
    neuronsphere

[neuronsphere]
repository = {twine_urls[0][0]}
username = {twine_urls[0][1]}
password = {twine_urls[0][2]}
                """
                twine.write(cfg)


def build(
    command_name: str, repo_name: str, upload_results: bool, pip_compile_only: bool
):
    version = get_version()
    if os.name == "nt":
        py_cmd = "python"
    else:
        py_cmd = "python3"

    repo_dir = os.getcwd()
    with build_dir(repo_name):
        with cd("./src/python"):
            compiled_deps = compile_requirements()
            reqs_txt_path = os.path.abspath("requirements.txt")
            if os.path.exists(reqs_txt_path):
                shutil.copy2(
                    reqs_txt_path,
                    os.path.join(repo_dir, "./src/python/requirements.txt"),
                )

            if pip_compile_only:
                return

            if compiled_deps:
                update_setup_py(compiled_deps)

            if os.path.exists("test"):
                shell.exec_cmd2(["pip3", "install", "--force-reinstall", "-e", "."])
                packages = find_packages()

                command = [py_cmd, "-m", "pytest"]
                for pkg in packages:
                    command += ["--cov", pkg]

                command += ["--cov-report", "term"]
                command += ["--cov-report", "html:coverage"]

                exitcode = shell.exec_cmd2(command)

                if exitcode != 0:
                    raise Exception("Error running unit tests.")

            exitcode = shell.exec_cmd2([py_cmd, "setup.py", "bdist_wheel"])
            if exitcode != 0:
                raise Exception("Error creating distribution.")


def install_local(repo_name: str):
    version = get_version()
    if os.name == "nt":
        py_cmd = "python"
    else:
        py_cmd = "python3"

    with cd("./src/python"):
        compiled_deps = compile_requirements()

        print("Building python distribution...")
        exitcode = shell.exec_cmd2([py_cmd, "setup.py", "sdist", "bdist_wheel"])
        if exitcode != 0:
            raise Exception("Error creating distribution.")

        deps_install = ["pip3", "install", "-r", "requirements.txt"]
        exitcode = shell.exec_cmd2(deps_install)

        if exitcode != 0:
            raise Exception("Error installing local Python package dependencies")

        install_cmd = [
            "pip3",
            "install",
            "--no-index",
            "--no-deps",
            "--force-reinstall",
            "--find-links=./dist",
            repo_name,
        ]
        print("Installing local package...")
        exitcode = shell.exec_cmd2(install_cmd)

        if exitcode != 0:
            raise Exception("Error installing local Python package")


def release(repo_name: str, repo_version: str):
    download_cmd = ["pip3", "download", f"{repo_name}=={repo_version}", "--no-deps"]

    exitcode = shell.exec_cmd2(download_cmd)

    if exitcode != 0:
        raise Exception("Error downloading Python package")

    wheels = list(Path(".").rglob(f"{repo_name.replace('-','_')}-{repo_version}-*.whl"))

    whl = wheels[0]

    upload_cmd = [
        "twine",
        "upload",
        str(whl),
    ]

    exitcode = shell.exec_cmd2(upload_cmd)

    if exitcode != 0:
        raise Exception("Error uploading Python package")
