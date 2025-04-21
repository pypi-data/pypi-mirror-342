import typer
from pinger.app import app

env_app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


@env_app.command("deployable")
def deployable():
    envs = app().list_deployable_environments()

    if not envs:
        typer.secho("No deployable environments found.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=0)

    typer.secho("✓ Deployable environments:", fg=typer.colors.GREEN, bold=True)
    for environment in envs:
        typer.echo(f"  • {environment}")
