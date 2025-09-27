# API Service

## Local virtual environment

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/), e.g. `pipx install uv` or download the standalone binary.
2. From `services/api`, create/refresh the virtualenv: `uv sync` (add `--dev` if you also need the test tooling).
3. Point your IDE to `services/api/.venv` for fast IntelliSense and local tooling.

When you start the Docker service (`docker compose up api`) the container runs `uv sync --frozen --no-dev` on boot, ensuring the mounted `.venv` stays consistent and matches the lockfile.
