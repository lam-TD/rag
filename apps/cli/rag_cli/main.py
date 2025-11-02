from __future__ import annotations

from typing import Optional

import typer

from . import __version__
from .commands.files import files_app
from .config import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, get_settings

app = typer.Typer(help="Command-line tools for interacting with the RAG platform.")
app.add_typer(files_app, name="files")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"rag-cli {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    base_url: Optional[str] = typer.Option(
        None,
        "--base-url",
        "-b",
        help=f"Base URL for the API (default: {DEFAULT_BASE_URL}).",
    ),
    timeout: float = typer.Option(
        DEFAULT_TIMEOUT,
        "--timeout",
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT}).",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Display the CLI version and exit.",
    ),
) -> None:
    """Configure global options before dispatching subcommands."""

    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["timeout"] = timeout

    # Validate once so misconfiguration is surfaced early.
    get_settings(base_url=base_url, timeout=timeout)

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.command.get_help(ctx))
        raise typer.Exit()


if __name__ == "__main__":
    app()

