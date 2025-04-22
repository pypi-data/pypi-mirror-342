import json
import os
import shutil
import subprocess
from collections import namedtuple
from importlib.metadata import version
from pathlib import Path
from tempfile import gettempdir
from typing import Union, List

from cement import Controller, minimal_logger

from hmd_lib_librarian_client.artifact_tools import (
    retrieve_and_unzip,
    zip_and_archive,
    content_item_path_from_spec,
    get_artifact_librarian_client,
)
from hmd_cli_tools.hmd_cli_tools import (
    get_session,
    get_secret,
    get_cloud_region,
    read_manifest,
    load_hmd_env,
)

BUILD_DIR = "build"

VERSION_BANNER = """
hmd build version: {}
"""

VERSION = version("hmd_cli_build")
artifact_name_template = "{}_{}_{}.zip"


Tool = namedtuple("Tool", ["command", "sub_command", "arguments"])

logger = minimal_logger(__name__)


class LocalController(Controller):
    class Meta:
        label = "build"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Generic build tool."

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the build command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(VERSION),
                },
            ),
            (
                ["-pdo", "--prebuild-download-only"],
                {
                    "help": "Do pre-build download only.",
                    "action": "store_true",
                    "dest": "prebuild_download_only",
                },
            ),
        )

    def _find_controller(self, controller_name, strict_mode: bool):
        controller = None
        for h in self.app._meta.handlers:
            if h.Meta.label == controller_name:
                controller = h
                break
        if not controller and strict_mode:
            raise Exception(f"CLI command, {controller_name}, not found.")

        if not controller and not strict_mode:
            logger.warning(
                f"""
WARNING: Could not find HMD CLI tool {controller_name} installed. Strict mode is turned off.

Skipping running {controller_name}.
            """
            )
        return controller

    def _default(self):
        """Default action if no sub-command is passed."""

        load_hmd_env(override=False)

        strict_mode_var = os.environ.get("HMD_BUILD_STRICT_MODE")

        if strict_mode_var is None:
            logger.warning(
                """
Could not find environment variable HMD_BUILD_STRICT_MODE. Defaulting to HMD_BUILD_STRICT_MODE=true.
            """
            )
            strict_mode_var = "true"

        strict_mode = strict_mode_var == "true"

        # build the args values...
        manifest = read_manifest()

        if "build" not in manifest:
            raise Exception("No build commands found in manifest.")

        build_path = Path(BUILD_DIR)
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path)

        try:
            defaults = [None, {}]
            session = get_session(
                get_cloud_region(self.app.pargs.hmd_region), self.app.pargs.profile
            )
            if "pre_build_artifacts" in manifest["build"]:
                print("Retrieving artifacts:")
                content_item_path: str
                dir_or_dirs: Union[str, List[str]]
                for content_item_path, dir_or_dirs in manifest["build"][
                    "pre_build_artifacts"
                ]:
                    if isinstance(dir_or_dirs, str):
                        dir_or_dirs = [dir_or_dirs]
                    print(
                        f"  artifact: {content_item_path}; into: {', '.join(dir_or_dirs)}"
                    )
                    retrieve_and_unzip(
                        self.app.pargs.customer_code,
                        self.app.pargs.hmd_region,
                        content_item_path_from_spec(content_item_path)[0],
                        dir_or_dirs,
                    )
            if self.app.pargs.prebuild_download_only:
                return

            if "secrets" in manifest["build"]:
                secrets_path = Path(gettempdir()) / "secrets"
                os.makedirs(secrets_path, exist_ok=True)
                for secret in manifest["build"]["secrets"]:
                    aws_secret = get_secret(session, secret["name"], use_cache=True)

                    if secret.get("type") == "env":
                        os.environ[secret["env"]] = aws_secret[secret["key"]]
                    elif secret.get("type") == "file":
                        with open(secrets_path / secret["name"], "w") as f:
                            json.dump(aws_secret, f)
                    elif secret.get("type") == "envfile":
                        with open(secrets_path / secret["name"], "w") as f:
                            for k, v in aws_secret.items():
                                f.write(f"{k}={v}\n")
                    else:
                        logger.warning(
                            f"Unknown secret type: {secret.get('type')}. Skipping {secret['name']}"
                        )

            shutil.copytree(Path("meta-data"), build_path / "meta-data")
            standard_dirs = [
                "docs",
                "test",
                "src/opa-bundles",
                "src/mickey",
                "src/entities",
                "src/schemas",
            ]
            for path in standard_dirs:
                if os.path.exists(Path(path)):
                    shutil.copytree(Path(path), build_path / path)

            for tool in manifest["build"]["commands"]:
                if len(tool) < 3:
                    tool = tool + defaults[-(3 - len(tool)) :]
                tool = Tool._make(tool)
                if tool.command == "exec":
                    if not tool.sub_command:
                        raise Exception(f'"exec" build command requires an executable.')
                    print(f"\n\nExecuting: {tool.sub_command}...")
                    result = subprocess.run(
                        [tool.sub_command],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        cwd=os.getcwd(),
                        shell=True,
                    )
                    print(result.stdout)
                    if result.returncode != 0:
                        raise Exception("Error running exec script.")

                else:
                    controller = self._find_controller(tool.command, strict_mode)
                    if controller is None:
                        continue
                    setattr(controller, "app", self.app)

                    print(f"\n\nBuilding: {tool.command}")
                    if tool.sub_command:
                        sub_command = getattr(controller, tool.sub_command)
                        for k, v in tool.arguments.items():
                            setattr(self.app.pargs, k, v)
                        sub_command(controller)
                    else:
                        build_command = getattr(controller, "build")
                        build_command(controller)
                        if os.environ.get("HMD_AUTO_PUBLISH") == "true":
                            publish_command = getattr(controller, "publish")
                            publish_command(controller)

            if "pre_build_artifacts" in manifest["build"]:
                dir_or_dirs: Union[str, List[str]]
                for content_item_path, dir_or_dirs in manifest["build"][
                    "pre_build_artifacts"
                ]:
                    if isinstance(dir_or_dirs, str):
                        dir_or_dirs = [dir_or_dirs]
                    for dir in dir_or_dirs:
                        shutil.rmtree(dir, ignore_errors=True)

            _, dirs, _ = next(os.walk(build_path))
            if len(dirs) > 1 and set(dirs) != {"meta-data", "docs"}:
                # there's always 1 directory, 'meta-data'. Only publish if there's something else.
                artifact_name = artifact_name_template.format(
                    self.app.pargs.repo_name, self.app.pargs.repo_version, "build"
                )
                if os.environ.get("HMD_AUTO_PUBLISH") == "true":
                    result = zip_and_archive(
                        self.app.pargs.customer_code,
                        self.app.pargs.hmd_region,
                        f"repository:/{self.app.pargs.repo_name}/{self.app.pargs.repo_version}/{artifact_name}",
                        "build",
                        build_path,
                    )
                    if manifest["build"].get("auto_deploy"):
                        client = get_artifact_librarian_client(
                            self.app.pargs.customer_code, self.app.pargs.hmd_region
                        )
                        client.add_tags(
                            result["nid"],
                            {"auto_deploy": manifest["build"].get("auto_deploy")},
                        )
                else:
                    tmpdir = os.environ.get("HMD_BUILD_OUTPUT_DIR", gettempdir())
                    artifact_path = os.path.join(
                        tmpdir,
                        f"{self.app.pargs.repo_name}-{self.app.pargs.repo_version}-build",
                        artifact_name.removesuffix(".zip"),
                    )
                    shutil.make_archive(artifact_path, "zip", build_path)

        finally:
            # shutil.rmtree(build_path)
            if os.path.exists(os.path.join(gettempdir(), self.app.pargs.repo_name)):
                shutil.rmtree(os.path.join(gettempdir(), self.app.pargs.repo_name))
