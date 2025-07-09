
ARG SDK_VERSION=3.12
ARG UV_VERSION=0.7.19
FROM mcr.microsoft.com/devcontainers/python:${SDK_VERSION}
COPY --from=ghcr.io/astral-sh/uv:${UV_VERSION} /uv /uvx /bin/

RUN uv tool install pre-commit && \
    uv tool install go-task-bin
