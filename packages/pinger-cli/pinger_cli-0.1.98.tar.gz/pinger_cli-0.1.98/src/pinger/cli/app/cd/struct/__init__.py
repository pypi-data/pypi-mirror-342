# src/pinger/cli/app/cd/struct/__init__.py

import typer

# import yaml
from pathlib import Path
from pinger.config import config
from pinger.app import app

cd_app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


@cd_app.callback()
def cd_default(env: str = typer.Argument("dev", help="environment name")):
    """
    If no subcommand is given, treat <env> as the environment name to deploy.
    """
    envs_dir = Path(config().envs).expanduser().resolve()
    config_path = envs_dir / env / "config.yml"

    if not config_path.is_file():
        typer.secho(
            f"✘ Environment '{env}' not found (expected {config_path})",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    # try:
    # with config_path.open("r") as f:
    # raw_config = yaml.safe_load(f) or {}
    # except yaml.YAMLError as e:
    #     typer.secho(
    #         f"✘ Failed to parse YAML in {config_path}: {e}", fg=typer.colors.RED
    #     )
    #     raise typer.Exit(code=1)

    typer.secho(f"✓ Deploying '{env}' using {config_path}", fg=typer.colors.GREEN)
    app().cd(env)
