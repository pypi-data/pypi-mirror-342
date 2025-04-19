"""
pinger.cli.app.__init__

Lightweight Typer wrapper around the core helpers in ``pinger.app``.
No behavioural changes on the CLI surface – it now proxy‑calls the
refactored ``app()`` singleton that lives in ``pinger.app``.
"""

from __future__ import annotations

import typer

from pinger.app import app  # singleton factory
from pinger.cli.app.cd.struct import cd_app
from pinger.cli.app.env.struct import env_app
from pinger.cli.app.secrets.struct import secrets_app

# ─────────────────────────────────────────────────────────────
# Root „app” sub‑command
# pinger app <…>
# ─────────────────────────────────────────────────────────────
app_sub = typer.Typer(
    no_args_is_help=True,
    help="Local‑dev, CI and deployment helpers for the current service.",
)

# delegate sets of commands that live in their own modules
app_sub.add_typer(cd_app, name="cd", help="promote container images")
app_sub.add_typer(env_app, name="env", help="manage environment configs")
app_sub.add_typer(secrets_app, name="secrets", help="edit encrypted secrets")


# ─────────────────────────────────────────────────────────────
# Local‑dev helpers
# ─────────────────────────────────────────────────────────────
@app_sub.command("start", help="Build image & start local Docker Compose stack.")
def start() -> None:
    app().start()


@app_sub.command("restart", help="Restart all running Compose containers.")
def restart() -> None:
    app().restart()


@app_sub.command(
    "shell",
    help="Attach to a bash shell in the 'main' container (auto‑build/start if needed).",
)
def shell() -> None:
    app().shell()


# ─────────────────────────────────────────────────────────────
# CI  – build & push
# ─────────────────────────────────────────────────────────────
@app_sub.command(
    "ci",
    help="Build Docker image, tag as 'latest' + SHA and push both tags to ECR.",
    epilog="Example:  pinger app ci",
)
def ci() -> None:
    app().ci()


# ─────────────────────────────────────────────────────────────
# ECS scaling helper
# ─────────────────────────────────────────────────────────────
@app_sub.command("scale", help="Scale an ECS service up or down.")
def scale(
    env: str = typer.Argument(..., help="Environment / AWS profile name."),
    count: int = typer.Argument(..., help="Desired task count."),
) -> None:
    app().scale(env, count)
