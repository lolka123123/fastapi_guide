#!/usr/bin/env bash


set -e

echo "Waiting for Postgres..."
until nc -z db 5432; do
  sleep 0.5
done
echo "Postgres is up."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Gunicorn..."
exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w "${GUNICORN_WORKERS:-4}" -b "${GUNICORN_BIND:-0.0.0.0:8000}"


