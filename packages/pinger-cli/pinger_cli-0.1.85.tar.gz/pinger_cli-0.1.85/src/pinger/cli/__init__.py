import typer
from pinger.cli.app.struct import app_sub
from pinger.cli.infra.struct import app as infra_sub

cli = typer.Typer(no_args_is_help=True)


cli.add_typer(app_sub, name="app")
cli.add_typer(infra_sub, name="infra")


cli()
