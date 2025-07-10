FROM python:3.13-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install uv

COPY pyproject.toml .

RUN uv sync

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .