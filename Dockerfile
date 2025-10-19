# https://docs.astral.sh/uv/guides/integration/docker
FROM python:3.13-slim@sha256:5f55cdf0c5d9dc1a415637a5ccc4a9e18663ad203673173b8cda8f8dcacef689 AS main
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
RUN useradd -m -u 1000 appuser
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
	--mount=type=bind,source=uv.lock,target=uv.lock \
	--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --locked --no-install-project

COPY --chown=appuser:appuser . /app

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked

USER appuser
ENV PATH="/app/.venv/bin:$PATH"
