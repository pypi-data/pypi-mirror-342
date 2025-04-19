import typer
from pinger.app import app
from pinger.secrets import secrets

secrets_app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


@secrets_app.command("edit")
def edit(env):
    """
    edit secrets with your $EDITOR
    """
    app().edit(env)


@secrets_app.command("encrypt")
def encrypt(env):
    """
    store secrets in parameter store as secrets
    """
    secrets().encrypt(env)
