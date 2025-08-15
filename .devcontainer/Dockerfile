FROM mcr.microsoft.com/devcontainers/python:3.13
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/

RUN uv tool install pre-commit && \
    uv tool install go-task-bin
