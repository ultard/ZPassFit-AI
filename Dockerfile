FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN uv pip install --python /opt/venv/bin/python \
    --no-cache-dir \
    catboost \
    grpcio \
    numpy \
    pandas \
    protobuf

FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}" \
    GRPC_HOST=0.0.0.0 \
    GRPC_PORT=50051 \
    GRPC_SHUTDOWN_GRACE_SECONDS=5

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY models ./models

RUN addgroup --system app && adduser --system --ingroup app app && chown -R app:app /app
USER app

EXPOSE 50051

CMD ["python", "-m", "app.grpc_server"]
