# RAG CLI

The `rag` command-line interface provides a thin wrapper around the API service so that developers can manage files, trigger summaries, and inspect results without leaving the terminal.

## Quick start

```bash
uv sync  # from apps/cli
uv run rag --help
```

By default the CLI targets `http://localhost:8001`. Override with the `--base-url` option or set the `RAG_API_BASE_URL` environment variable.

## Available commands

- `rag files list` — list uploaded files.
- `rag files upload PATH --note ...` — upload a local file.
- `rag files summary FILE_ID` — request a summary for the given file.

Run `rag <command> --help` for detailed usage.
