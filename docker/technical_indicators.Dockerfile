# An example of using standalone Python builds with multistage images.

# First, build the application in the `/app` directory
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install ta-lib
ENV TALIB_DIR=/usr/local
RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4/ && \
    ./configure --prefix=$TALIB_DIR && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.6.4-src.tar.gz ta-lib-0.6.4/

# Ensure TA-Lib is linked correctly
RUN ldconfig

# ── NEW: add the CA bundle ───────────────────────────────────
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# ──────────────────────────────────────────────────────────────

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY services /app/services
# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python before the project for caching
RUN uv python install 3.12

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
# RUN ls -l uv.lock && cat uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []

# Run the FastAPI application by default
CMD ["uv", "run", "/app/services/candles/src/candles/main.py"]

## To debug
#CMD ["/bin/bash", "-c", "sleep 999999"]