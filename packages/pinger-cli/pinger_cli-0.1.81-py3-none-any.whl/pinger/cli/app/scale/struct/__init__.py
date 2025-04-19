import typer
from pinger.app import app

scale_app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


@scale_app.command("to")
def to(env: str, count: int):
    """
    scale to a certain amount of nodes || tasks
    its contextual
    """
    app().scale(env, count)
