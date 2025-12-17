FROM python:3.15.0a3-alpine3.22 AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"


FROM base AS build

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY image_refresher/ ./image_refresher/
RUN uv build --wheel && pip install dist/*.whl


FROM python:3.15.0a3-alpine3.22 AS runtime

LABEL org.opencontainers.image.source=https://github.com/melvyndekort/image-refresher

COPY --from=build /venv /venv

ENV PATH="/venv/bin:$PATH"

CMD ["python3", "-m", "image_refresher.main"]
