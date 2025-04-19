#!/usr/bin/env python3
"""
Pinger Infra CLI
────────────────
Terraform‑style plan/apply helpers + a snazzy “info” banner.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import typer
from rich.console import Console
from rich.table import Table

from pinger.infra import infra
from pinger.config import config

app = typer.Typer(no_args_is_help=True)
console = Console()

PKG_ROOT = Path("packages")  # central place if you ever move it


# ─────────────────────────────
# helpers
# ─────────────────────────────
def _discover_packages() -> List[str]:
    """
    Return a list of directories inside ./packages/ (not the repo root).
    Hidden dirs (starting with “.”) are ignored.
    """
    if not PKG_ROOT.exists():
        return []

    return sorted(
        d.name for d in PKG_ROOT.iterdir() if d.is_dir() and not d.name.startswith(".")
    )


def _discover_envs(cfg_root: Path = Path("configs")) -> List[str]:
    """Each sub‑directory of ./configs is considered an environment."""
    if not cfg_root.exists():
        return []
    return sorted(
        d.name for d in cfg_root.iterdir() if d.is_dir() and not d.name.startswith(".")
    )


# ─────────────────────────────
# commands
# ─────────────────────────────
@app.command()
def info() -> None:
    """
    📦  Show information about this infra repo & its packages / envs.
    """
    proj = config().name
    packages = _discover_packages()
    envs = _discover_envs()

    console.rule(f"[bold cyan]🛠️  {proj} – infrastructure overview[/]")

    # packages table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("📦 Package")
    table.add_column("Path", style="dim")
    table.add_column("Exists", justify="center")

    for pkg in packages:
        table.add_row(pkg, f"./{pkg}", "✅")

    console.print(table)

    console.print(f"\n🌍  Environments discovered: [green]{', '.join(envs) or '—'}[/]")
    console.print(f"🧮  Total packages: [yellow]{len(packages)}[/]")
    console.print(f"🏞️  Total envs:     [yellow]{len(envs)}[/]\n")
    console.rule("[bold cyan]Done")


# ─────────────────────────────
# plan / apply
# ─────────────────────────────
@app.command()
def plan(
    envs: str = typer.Option(..., help="Comma‑separated list of envs."),
    packages: str = typer.Option(..., help="Comma‑separated list of packages."),
):
    """Generate a Terraform‑style plan."""
    infra().plan(
        [e.strip() for e in envs.split(",")],
        [p.strip() for p in packages.split(",")],
    )


@app.command()
def apply(
    envs: str = typer.Option(..., help="Comma‑separated list of envs."),
    packages: str = typer.Option(..., help="Comma‑separated list of packages."),
):
    """Apply infra changes."""
    infra().apply(
        [e.strip() for e in envs.split(",")],
        [p.strip() for p in packages.split(",")],
    )


if __name__ == "__main__":
    app()
