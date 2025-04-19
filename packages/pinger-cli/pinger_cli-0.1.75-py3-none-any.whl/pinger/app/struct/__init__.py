"""
pinger.app
==========

Core CI/CD + local‑dev helpers used by the Typer‑based CLI.
No Typer decorators in this file — your `pinger.cli.*` code wires commands.

Public surface (unchanged)
--------------------------
    app().ci()          # build + push image
    app().cd(env, commit=None | "latest" | "<sha>")
    app().start()
    app().restart()
    app().shell()
    app().scale(env, count)
    app().list_deployable_environments()
    app().edit(env)

• Passing commit=None **or** commit="latest" deploys the SHA that backs the
  `:latest` tag in ECR.
• Passing commit="<sha>" pins an explicit image.
"""

from __future__ import annotations

import base64
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import boto3

from pinger.config import config


class App:
    # ─────────────────────────────────────────────────────────────
    # Generic helpers
    # ─────────────────────────────────────────────────────────────
    _compose: Optional[str] = None
    _docker: Optional[str] = None

    @classmethod
    def compose(cls, setting: Optional[str] = None) -> str:
        if cls._compose is None:
            cls._compose = setting or "docker-compose"
        return cls._compose

    @classmethod
    def docker(cls, setting: Optional[str] = None) -> str:
        if cls._docker is None:
            cls._docker = setting or "docker"
        return cls._docker

    # quick accessors
    @staticmethod
    def name() -> str:
        return config().name

    # shell wrapper
    @staticmethod
    def sh(cmd: str, *, interactive: bool = False) -> None:
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            executable="/bin/bash",
            stdin=None if interactive else subprocess.PIPE,
        )

    # Git helper
    @staticmethod
    def git_hash() -> str:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode()
            .strip()
        )

    # ─────────────────────────────────────────────────────────────
    # Poetry bootstrap (optional)
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def install_poetry(cls) -> None:
        if shutil.which("poetry"):
            print("Poetry already installed.")
            return

        if platform.system() == "Windows":
            cmd = (
                "(Invoke-WebRequest -Uri https://install.python-poetry.org "
                "-UseBasicParsing | python -)"
            )
            cls.sh(f'powershell -Command "{cmd}"')
        else:
            cls.sh("curl -sSL https://install.python-poetry.org | python3 -")

    @classmethod
    def poetry_install(cls) -> None:
        if not shutil.which("poetry"):
            raise RuntimeError("Poetry not installed")
        cls.sh("poetry install --no-interaction")

    # ─────────────────────────────────────────────────────────────
    # ECR helpers
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def _boto(profile: str):
        return boto3.Session(profile_name=profile)

    @classmethod
    def get_ecr_repo_uri(cls, repo_name: str, profile_name: str) -> str:
        ecr = cls._boto(profile_name).client("ecr")
        repo = ecr.describe_repositories(repositoryNames=[repo_name])["repositories"][0]
        return repo["repositoryUri"]

    @classmethod
    def ecr_login(cls, registry: str) -> None:
        ecr = cls._boto(config().ci.profile).client("ecr")
        token = ecr.get_authorization_token()["authorizationData"][0][
            "authorizationToken"
        ]
        pwd = base64.b64decode(token).decode().split(":")[1]
        cls.sh(f"{cls.docker()} login --username AWS --password {pwd} {registry}")

    @classmethod
    def _resolve_latest_sha(cls, repo_name: str, profile: str) -> str:
        """
        Return the *commit SHA* tag that shares the same digest as 'latest'.
        """
        session = cls._boto(profile)
        ecr = session.client("ecr")

        latest = ecr.describe_images(
            repositoryName=repo_name,
            imageIds=[{"imageTag": "latest"}],
        )["imageDetails"][0]

        digest = latest["imageDigest"]
        # Prefer tag that travelled with 'latest'
        for tag in latest.get("imageTags", []):
            if tag != "latest":
                return tag

        # Fallback: search by digest
        imgs = ecr.describe_images(
            repositoryName=repo_name,
            imageIds=[{"imageDigest": digest}],
        )["imageDetails"]
        for img in imgs:
            for tag in img.get("imageTags", []):
                if tag != "latest":
                    return tag
        raise RuntimeError("Could not resolve SHA for 'latest'")

    # ─────────────────────────────────────────────────────────────
    # CI – build & push
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def ci(cls) -> None:
        repo = config().ci.ecr_repo_name
        repo_uri = cls.get_ecr_repo_uri(repo, profile_name=config().ci.profile)

        dockerfile = (
            "app.dockerfile" if Path("app.dockerfile").exists() else "Dockerfile"
        )
        df_arg = f"-f {dockerfile}" if dockerfile != "Dockerfile" else ""

        cls.sh(f"{cls.docker()} build {df_arg} -t {cls.name()}:latest .")
        cls.ecr_login(registry=repo_uri.split("/")[0])

        sha = cls.git_hash()
        cls.sh(f"{cls.docker()} tag {cls.name()}:latest {repo_uri}:latest")
        cls.sh(f"{cls.docker()} tag {cls.name()}:latest {repo_uri}:{sha}")
        cls.sh(f"{cls.docker()} push {repo_uri}:latest")
        cls.sh(f"{cls.docker()} push {repo_uri}:{sha}")

    # ─────────────────────────────────────────────────────────────
    # CD – promote image
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def cd(cls, env: str, *, commit: str | None = None) -> None:
        """
        Deploy *commit* (or the SHA behind :latest / "latest") to *env*.
        Works for both ECS and Lambda, as per `config().cd.type`.
        """
        if commit == "latest":  # <-- explicit "latest" treated as None
            commit = None

        deploy_type = config().cd.type
        repo_name = config().ci.ecr_repo_name
        repo_uri = cls.get_ecr_repo_uri(repo_name, profile_name=config().ci.profile)

        # ────────────── ECS ──────────────
        if deploy_type == "ecs":
            ecs = cls._boto(env).client("ecs", region_name=config().cd.region)
            cluster = f"{env}-{cls.name()}-cluster"
            service = f"{env}-{cls.name()}-service"

            td = ecs.describe_services(cluster=cluster, services=[service])["services"][
                0
            ]["taskDefinition"]
            family = td.split("/")[-1].split(":")[0]
            latest_td = ecs.list_task_definitions(
                familyPrefix=family, sort="DESC", maxResults=1
            )["taskDefinitionArns"][0]

            ecs.update_service(
                cluster=cluster,
                service=service,
                taskDefinition=latest_td,
                forceNewDeployment=True,
            )
            ecs.get_waiter("services_stable").wait(cluster=cluster, services=[service])

        # ────────────── Lambda ──────────────
        elif deploy_type == "lambda":
            if commit is None:
                commit = cls._resolve_latest_sha(repo_name, profile=config().ci.profile)
            image_uri = f"{repo_uri}:{commit}"

            lam = cls._boto(env).client("lambda", region_name=config().cd.region)
            fn = f"{env}-{cls.name()}"
            alias = "live"

            lam.update_function_code(FunctionName=fn, ImageUri=image_uri, Publish=False)
            lam.get_waiter("function_updated").wait(FunctionName=fn)

            ver = lam.publish_version(FunctionName=fn, Description=f"Deploy {commit}")[
                "Version"
            ]
            lam.update_alias(FunctionName=fn, Name=alias, FunctionVersion=ver)

        else:
            raise RuntimeError(f"Unknown deploy type '{deploy_type}'")

    # ─────────────────────────────────────────────────────────────
    # Local‑dev helpers
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def shell(cls) -> None:
        container = f"{cls.name()}-main-1"
        res = subprocess.run(
            [cls.docker(), "inspect", "-f", "{{.State.Status}}", container],
            capture_output=True,
            text=True,
        )
        status = res.stdout.strip()

        if res.returncode != 0 or status not in {"running", "created", "exited"}:
            cls.sh(f"{cls.docker()} build -t {cls.name()}:latest .")
            cls.sh(f"{cls.compose()} up -d main")
        elif status != "running":
            cls.sh(f"{cls.docker()} start {container}")

        cls.sh(f"{cls.docker()} exec -it {container} bash", interactive=True)

    @classmethod
    def start(cls) -> None:
        cls.sh(f"{cls.docker()} build -t {cls.name()}:latest .")
        cls.sh(f"{cls.compose()} up -d")

    @classmethod
    def restart(cls) -> None:
        cls.sh(f"{cls.compose()} restart")

    # ─────────────────────────────────────────────────────────────
    # ECS scaling
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def scale(cls, env: str, count: int) -> None:
        ecs = cls._boto(env).client("ecs", region_name=config().cd.region)
        cluster = f"{env}-{cls.name()}-cluster"
        service = f"{env}-{cls.name()}-service"

        ecs.update_service(cluster=cluster, service=service, desiredCount=count)
        ecs.get_waiter("services_stable").wait(cluster=cluster, services=[service])

    # ─────────────────────────────────────────────────────────────
    # Misc helpers
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def list_deployable_environments() -> list[str]:
        envs_dir = Path(config().envs).expanduser()
        return sorted(
            p.name
            for p in envs_dir.iterdir()
            if p.is_dir() and (p / "config.yml").is_file()
        )

    @classmethod
    def edit(cls, env: str) -> None:
        cls.sh(f"sops edit envs/{env}/secrets.yaml")


_APP_SINGLETON = App()


def app() -> App:
    return _APP_SINGLETON
