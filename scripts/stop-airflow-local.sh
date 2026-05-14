#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

docker compose --env-file runtime/airflow/.env -f runtime/airflow/docker-compose.yaml down
