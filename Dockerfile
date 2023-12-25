FROM python:3.11.4-slim as builder

WORKDIR /app

RUN python -m pip install --no-cache-dir poetry==1.5.1 \
    && poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

FROM python:3.11.4-slim

COPY --from=builder /app /app

COPY /app /app

ENV PYTHONPATH=/app

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0"]
