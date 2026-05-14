#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

scripts/generate-runtime.sh
mkdir -p runtime/airflow/data runtime/airflow/logs runtime/airflow/plugins

if [ ! -f runtime/airflow/.env ]; then
  {
    printf 'AIRFLOW_UID=%s\n' "$(id -u)"
    printf 'AIRFLOW_PROJ_DIR=.\n'
  } > runtime/airflow/.env
fi

docker compose --env-file runtime/airflow/.env -f runtime/airflow/docker-compose.yaml up airflow-init
docker compose --env-file runtime/airflow/.env -f runtime/airflow/docker-compose.yaml up
