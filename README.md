# Friendly Giggle

A lightweight control-plane definition for a continuous-learning market data system.



## Core Idea

This repo separates intent from runtime artifacts.

```text
specs = portable system definition
generator = compiler
containers = execution units
Airflow/Docker/Kubernetes = runtime
```

```mermaid
flowchart LR
  A[specs/*.yaml] --> B[build/validate_specs.py]
  B --> C[build/generate_runtime.py]
  C --> D[runtime/dags/generated/*.py]
  C --> E[runtime/docker-bake.generated.hcl]
  C --> F[runtime/quality/generated/*.json]
  D --> G[Airflow scheduler]
  E --> H[Container builds]
  F --> I[Quality checks]
```
## Design Principle

Specs answer what exists, what depends on what, and what quality or promotion contract applies.

Generated runtime artifacts answer which Airflow DAGs, task commands, manifests, schema contracts, and container build targets implement that intent for a specific environment.

## Quick Start

Generate and validate runtime artifacts:

```sh
scripts/generate-runtime.sh
```

Validate generated DAG Python files:

```sh
scripts/validate-generated-dags.sh
```

Start local Airflow:

```sh
scripts/start-airflow-local.sh
```

Open `http://localhost:8080` and log in with `airflow` / `airflow`.

More detail:

- [Local Airflow demo](docs/local-airflow.md)
- [Source-shaped demo schemas](docs/source-schemas.md)
- [Spec vs containers](docs/spec-vs-containers.md)

## Control-Plane Structure

```text
specs/
  sources.yaml
  source_schemas.yaml
  assets.yaml
  dags.yaml
  tasks.yaml
  quality_profiles.yaml
  promotion_rules.yaml
build/
  validate_specs.py
  generate_runtime.py
schemas/
  asset_manifest.schema.json
  quality_observation.schema.json
runtime/
  airflow/docker-compose.yaml
  docker-bake.generated.hcl
  dags/generated/
    demo_ingest_news_sources.py
    demo_prepare_news_clean_room.py
    demo_prepare_price_bars.py
    demo_prepare_company_reference.py
    demo_build_training_feature_panel.py
  manifests/generated/
  quality/generated/
  stubs/Dockerfile
  stubs/run_task.py
scripts/
  generate-runtime.sh
  start-airflow-local.sh
  stop-airflow-local.sh
  clean-airflow-local.sh
  validate-generated-dags.sh
docs/
  local-airflow.md
  source-schemas.md
  spec-vs-containers.md
```

```mermaid
flowchart LR
  subgraph Source_DAGs[Source and clean-room DAGs]
    K[Kaggle stock news] --> NI[demo_ingest_news_sources]
    FH[Finnhub company news] --> NI
    AVN[Alpha Vantage news sentiment] --> NI
    NI --> NC[demo_prepare_news_clean_room]

    AVP[Alpha Vantage daily bars] --> PB[demo_prepare_price_bars]
    TP[Tiingo daily bars] --> PB

    FHP[Finnhub company profile] --> CR[demo_prepare_company_reference]
    TM[Tiingo symbol metadata] --> CR
    AVF[Alpha Vantage company overview] --> CR
  end

  NC --> FP[demo_build_training_feature_panel]
  PB --> FP
  CR --> FP
  FP --> TT[trusted_training_market_feature_panel]
```

## Cleaning Metadata and Future Learning

Cleaning and filtering should emit metadata that explains both what happened to the data and why a promotion decision was made. The demo keeps this lightweight through asset manifests and quality scorecards, but the intended production contract should track:

- source metadata: provider, endpoint, request parameters, dataset snapshot, ingestion time, provider event time, raw payload hash, schema version, response status, latency, and retry count
- normalization metadata: input asset versions, transform code version, output schema version, null rates, type coercions, timestamp repairs, entity resolution confidence, provider conflicts, dedupe counts, dropped records, repaired records, and outlier flags
- quality metadata: hard gate results, soft score vector, overall score, freshness lag, distribution stats, leakage checks, join coverage, label maturity, warnings, blocking failures, promotion rule version, and final decision
- feedback metadata: quarantine reason, reviewer override, human review label, downstream model outcome, training run ID, and later incident or drift signals

The future learning loop is:

```mermaid
flowchart LR
  A[cleaning metadata] --> B[promotion decision]
  B --> C[clean room or quarantine]
  C --> D[human review and downstream outcomes]
  D --> E[quality classifier training data]
  E --> F[learned filtering policy]
  F --> B
```

The first implementation should keep deterministic hard gates as the fail-closed boundary. Learned models can later assist soft scoring, quarantine triage, reviewer prioritization, and threshold tuning once enough feedback metadata exists.

## Data Zones

- `raw`: provider-shaped data exactly as landed
- `clean_candidate`: normalized data awaiting quality gates
- `metadata`: manifests, scorecards, lineage, and promotion decisions
- `clean_room`: analysis-safe assets
- `trusted_training`: assets that pass stronger leakage and training-readiness checks
- `quarantine`: assets or decisions blocked from downstream use

## Example Demo Flow

```mermaid
flowchart LR
  A[raw_kaggle_stock_news] --> D[normalize_news]
  B[raw_finnhub_company_news] --> D
  C[raw_alpha_vantage_news_sentiment] --> D
  D --> E[clean_news_candidate]
  E --> F[validate_clean_news]
  F --> G[clean_news_quality_scorecard]
  G --> H[promote_clean_news]
  H --> I[clean_room_news]
```

```mermaid
flowchart LR
  A[clean_room_news] --> E[build_market_feature_panel]
  B[clean_room_price_bars] --> E
  C[clean_room_company_reference] --> E
  D[clean_fundamentals_candidate] --> E
  E --> F[validate_market_feature_panel]
  F --> G[promote_market_feature_panel]
  G --> H[trusted_training_market_feature_panel]
```

## Demo Scope
![Airflow DAGs demo](docs/assets/airflow-dags-demo.png)

The repo now includes a runnable local demo that shows how market-data flows can be described as specs and compiled into Airflow DAGs. The first pass uses no-credential stub tasks for:

- Kaggle stock news dataset snapshots
- Finnhub open-data-style news and company reference flows
- Alpha Vantage daily bars, news sentiment, and company overview flows
- Tiingo daily bars and symbol metadata flows
- a cross-source training feature panel DAG


