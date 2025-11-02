from __future__ import annotations

from pathlib import Path

import respx
from httpx import Response
from typer.testing import CliRunner

from rag_cli.main import app

runner = CliRunner()


@respx.mock(base_url="http://localhost:8001")
def test_list_files_displays_table() -> None:
    respx.get("/api/v1/files").mock(
        return_value=Response(
            200,
            json={
                "files": [
                    {
                        "id": 1,
                        "name": "report.pdf",
                        "size": 2048,
                        "note": "Quarterly report",
                    }
                ]
            },
        )
    )

    result = runner.invoke(app, ["files", "list"])

    assert result.exit_code == 0
    assert "report.pdf" in result.output


@respx.mock(base_url="http://localhost:8001")
def test_upload_file_success(tmp_path: Path) -> None:
    sample_file = tmp_path / "document.txt"
    sample_file.write_text("hello world")

    respx.post("/api/v1/files").mock(
        return_value=Response(
            200,
            json={
                "file": {
                    "id": 5,
                    "name": "document.txt",
                    "size": len(sample_file.read_bytes()),
                    "note": None,
                    "sha256": "",
                    "storage_path": "/uploads/document.txt",
                    "mime_type": "text/plain",
                }
            },
        )
    )

    result = runner.invoke(app, ["files", "upload", str(sample_file)])

    assert result.exit_code == 0
    assert "Uploaded" in result.output


@respx.mock(base_url="http://localhost:8001")
def test_summary_success() -> None:
    respx.post("/api/v1/files/1/summary").mock(
        return_value=Response(
            200,
            json={"summary": ["chunk one", "chunk two"]},
        )
    )

    result = runner.invoke(app, ["files", "summary", "1"])

    assert result.exit_code == 0
    assert "chunk one" in result.output

