# Local Airflow Demo

This demo runs generated Airflow DAGs against no-credential stub tasks. It is meant to show orchestration shape, asset flow, quality checks, and promotion boundaries before live provider ingestion exists.

## Prerequisites

- Docker with Docker Compose v2
- Python 3
- Port `8080` available for the Airflow webserver

## Generate Runtime Artifacts

```sh
scripts/generate-runtime.sh
```

This validates spec references, then writes:

- `runtime/dags/generated/*.py`
- `runtime/docker-bake.generated.hcl`
- `runtime/manifests/generated/*.json`
- `runtime/quality/generated/*.json`

## Start Airflow

```sh
scripts/start-airflow-local.sh
```

The script generates runtime artifacts, creates local Airflow folders, initializes the Airflow database, and starts the webserver and scheduler.

Open `http://localhost:8080`.

Default login:

- username: `airflow`
- password: `airflow`

## Run the Demo

In the Airflow UI, trigger any generated DAG:

- `demo_ingest_news_sources`
- `demo_prepare_news_clean_room`
- `demo_prepare_price_bars`
- `demo_prepare_company_reference`
- `demo_build_training_feature_panel`

Tasks call `runtime/stubs/run_task.py` and write small JSON asset payloads plus manifests to `runtime/airflow/data/demo`. Ingest tasks emit source-shaped records, and normalization tasks emit the canonical shapes documented in `docs/source-schemas.md`.

## Validate Generated DAGs

```sh
scripts/validate-generated-dags.sh
```

This regenerates runtime artifacts and runs Python bytecode compilation for generated DAG files.

## Stop or Clean Up

Stop containers while keeping local Airflow volumes:

```sh
scripts/stop-airflow-local.sh
```

Remove containers and database volumes:

```sh
scripts/clean-airflow-local.sh
```

The local stack is for demonstration only. Production orchestration should use real task images, provider credentials, retry policies, observability, and a managed Airflow or Kubernetes deployment.
