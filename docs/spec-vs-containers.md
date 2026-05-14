# Spec vs Containers

Friendly Giggle keeps system intent separate from execution packaging.

## Spec Layer

The files in `specs/` describe the portable control plane:

- sources and provider metadata
- source-shaped raw contracts and canonical normalized contracts
- assets, zones, owners, and dependencies
- DAG task order and asset-trigger intent
- task inputs, outputs, quality profiles, and promotion rules

Specs should answer what exists, what depends on what, and what quality or promotion contract applies. They should not encode Docker image build mechanics, Airflow operator details, cloud project names, or local filesystem paths except for explicit task source directories.

## Generator Layer

`build/generate_runtime.py` compiles the spec layer into runtime artifacts:

- Airflow DAG Python files
- Docker Buildx Bake targets
- task manifests
- quality profile manifests
- source, asset, and promotion rule manifests

The generator is the boundary where portable intent becomes runtime-specific configuration. It should be deterministic so generated files are diffable and reviewable.

## Container Layer

Task containers are execution units. A production task image should own:

- code and dependency installation
- provider client libraries
- command entrypoints
- resource requirements
- runtime-only credentials and environment variables

The specs reference container intent through task image names, source directories, and entrypoints. The specs do not define Dockerfiles inline.

## Local Demo Layer

The current local demo uses `runtime/stubs/run_task.py` for every task. This is intentional:

- generated Airflow DAGs can run without provider credentials
- the demo shows orchestration and asset flow
- real ingestion can replace stubs task-by-task without changing the asset contract

When a real provider integration is added, keep the existing asset names and quality profiles stable unless the contract changes. Add or replace the task implementation and container definition, then let the generator refresh the runtime artifacts.
