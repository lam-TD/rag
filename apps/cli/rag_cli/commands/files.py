from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import RagAPIClient, RagAPIError

console = Console()

files_app = typer.Typer(help="Manage files stored in the RAG service.")


def _build_client(ctx: typer.Context) -> RagAPIClient:
    ctx.ensure_object(dict)
    settings = get_settings(
        base_url=ctx.obj.get("base_url"),
        timeout=ctx.obj.get("timeout"),
    )
    return RagAPIClient(base_url=settings.base_url, timeout=settings.timeout)


def _handle_api_error(error: RagAPIError) -> None:
    status = f" (HTTP {error.status_code})" if error.status_code else ""
    console.print(f"[red]API error{status}: {error}[/]")
    raise typer.Exit(code=1)


@files_app.command("list")
def list_files(
    ctx: typer.Context,
) -> None:
    """List the files currently stored in the API."""
    try:
        with _build_client(ctx) as client:
            payload = client.list_files()
    except RagAPIError as error:
        _handle_api_error(error)
        return

    if not payload.files:
        console.print("[yellow]No files found.[/]")
        return

    table = Table(title="Files", header_style="bold")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Size (bytes)", justify="right")
    table.add_column("Note")

    for file in payload.files:
        note = file.note or ""
        table.add_row(str(file.id), file.name, str(file.size), note)

    console.print(table)


@files_app.command("upload")
def upload_file(
    ctx: typer.Context,
    path: Path = typer.Argument(..., help="Path to the file to upload."),
    note: Optional[str] = typer.Option(None, "--note", "-n", help="Optional note to store with the file."),
) -> None:
    """Upload a local file to the API."""
    try:
        with _build_client(ctx) as client:
            payload = client.upload_file(path, note=note)
    except FileNotFoundError as error:
        console.print(f"[red]{error}[/]")
        raise typer.Exit(code=1) from error
    except RagAPIError as error:
        _handle_api_error(error)
        return

    file = payload.file
    console.print(f"[green]Uploaded[/] `{file.name}` (id={file.id})")


@files_app.command("summary")
def summarise_file(
    ctx: typer.Context,
    file_id: int = typer.Argument(..., help="Identifier of the file to summarise."),
) -> None:
    """Request a summary for the given file."""
    try:
        with _build_client(ctx) as client:
            payload = client.summarise_file(file_id)
    except RagAPIError as error:
        _handle_api_error(error)
        return

    if not payload.summary:
        console.print("[yellow]The API returned an empty summary.[/]")
        return

    console.print(f"[bold]Summary contains {len(payload.summary)} chunk(s):[/]")
    for index, chunk in enumerate(payload.summary, start=1):
        console.print(f"\n[cyan]Chunk {index}[/]\n{chunk}")

