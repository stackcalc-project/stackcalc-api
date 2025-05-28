# Stage 1
FROM python:3.13 as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock .
RUN uv venv --prompt stackcalc-worker venv
ENV UV_PROJECT_ENVIRONMENT=/app/venv
RUN uv sync --no-dev --locked

# Stage 2
FROM python:3.13-slim-bullseye AS runner
WORKDIR /app
COPY --from=builder /app/venv venv
COPY stackcalc stackcalc
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
CMD ["celery", "-A", "stackcalc.api", "worker", "--loglevel=INFO"]
