FROM docker.io/python:3.13.1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get upgrade && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gcc \
    libc6 \
    git

WORKDIR /usr/src/app
COPY pyproject.toml .
COPY uv.lock .
COPY ./src/* .
RUN uv sync --no-dev

CMD ["uv", "run", "main.py"]