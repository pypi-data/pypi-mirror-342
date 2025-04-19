import subprocess
import typer
import yaml
import boto3
from pathlib import Path
from typing import Dict, Any
from pinger.config import config


class Secrets:
    """
    Uploads decrypted secrets from SOPS-managed files into AWS SSM Parameter Store.
    """

    @classmethod
    def upload_secrets_recursively(cls, ssm, base_path: str, data: Any):
        """
        Recursively upload all dictionary values under base_path.
        Each leaf (non-dict, non-list) becomes a SecureString parameter.
        Lists become separate numbered keys (e.g. base_path/listname/0).
        """
        if isinstance(data, dict):
            for key, value in data.items():
                param_name = f"{base_path}/{key}"
                cls.upload_secrets_recursively(ssm, param_name, value)
        elif isinstance(data, list):
            # For lists, we store each item under an indexed key
            for i, item in enumerate(data):
                param_name = f"{base_path}/{i}"
                cls.upload_secrets_recursively(ssm, param_name, item)
        else:
            # It's a scalar (str, int, bool, float, etc.) -> store as a single param
            try:
                ssm.put_parameter(
                    Name=base_path,
                    Value=str(data),
                    Type="SecureString",
                    Overwrite=True,
                )
                typer.secho(f"✔ Uploaded secret: {base_path}", fg=typer.colors.GREEN)
            except Exception as e:
                typer.secho(
                    f"✘ Failed to upload {base_path}: {e}",
                    fg=typer.colors.RED,
                    err=True,
                )

    @classmethod
    def encrypt(cls, env: str):
        """
        Decrypt a SOPS-managed file and recursively upload each secret into Parameter Store.
        """
        # Path to your secrets file (tokens, passwords, etc.)
        path = Path(f"{config().envs}/{env}/secrets.yaml").resolve()
        ssm_prefix = f"/{config().name}/{env}"

        typer.secho(
            f"[SECRETS] Loading encrypted secrets from: {path}", fg=typer.colors.CYAN
        )

        if not path.exists():
            typer.secho(
                f"✘ Secrets file not found: {path}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(code=1)

        try:
            # Decrypt secrets using SOPS
            decrypted = subprocess.check_output(f"sops -d {path}", shell=True)
            secrets: Dict = yaml.safe_load(decrypted)
        except Exception as e:
            typer.secho(
                f"✘ Failed to decrypt secrets: {e}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(code=1)

        # Create SSM client with desired profile/region
        ssm = boto3.Session(profile_name=env).client(
            "ssm", region_name=config().cd.region
        )

        typer.secho(
            f"[SECRETS] Uploading to Parameter Store with prefix: {ssm_prefix}\n",
            fg=typer.colors.BLUE,
        )

        # Recursively traverse the secrets dictionary and upload each leaf
        cls.upload_secrets_recursively(ssm, ssm_prefix, secrets)

        typer.secho(
            f"\n[SECRETS] Done uploading secrets for environment: {env}",
            fg=typer.colors.GREEN,
            bold=True,
        )
