ARG SDK_VERSION=3
FROM mcr.microsoft.com/devcontainers/python:${SDK_VERSION}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv tool install pre-commit && \
    uv tool install go-task-bin
