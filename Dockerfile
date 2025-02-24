ARG UV_DEBIAN=ghcr.io/astral-sh/uv:python3.12-bookworm
ARG PYTHON_SLIM=docker.io/python:3.12
ARG MODEL=ViT-B/32

FROM ${UV_DEBIAN} as builder
ARG MODEL

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    libc6 \
    git \
    curl

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev


ADD . /app

# Download pre-trained models
COPY ./scripts /scripts
RUN chmod +x /scripts/download-models.sh
RUN /scripts/download-models.sh $MODEL

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

FROM ${PYTHON_SLIM} as final

COPY --from=builder --chown=2048:2048 /app /app

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app

USER 2048
ENTRYPOINT [ "python", "src/main.py" ]
