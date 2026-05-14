"""
Generated demo DAG from specs/dags.yaml.

Source DAG: demo_prepare_price_bars
Description: Ingest Alpha Vantage and Tiingo OHLCV bars, normalize them, validate them, and promote them.
"""

from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


DEFAULT_ARGS = {
    "owner": "friendly-giggle",
    "depends_on_past": False,
}


with DAG(
    dag_id='demo_prepare_price_bars',
    description='Ingest Alpha Vantage and Tiingo OHLCV bars, normalize them, validate them, and promote them.',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["demo", "market-data", "generated"],
) as dag:
    tasks = {}

    tasks['ingest_alpha_vantage_daily_bars'] = BashOperator(
        task_id='ingest_alpha_vantage_daily_bars',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_alpha_vantage_daily_bars',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_alpha_vantage_daily_bars", "image": {"name": "market/ingest-alpha-vantage-daily-bars", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_alpha_vantage_daily_bars", "outputs": ["raw_alpha_vantage_daily_bars"], "python_version": "3.12", "runtime": "python", "source": "alpha_vantage", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_tiingo_daily_bars'] = BashOperator(
        task_id='ingest_tiingo_daily_bars',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_tiingo_daily_bars',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_tiingo_daily_bars", "image": {"name": "market/ingest-tiingo-daily-bars", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_tiingo_daily_bars", "outputs": ["raw_tiingo_daily_bars"], "python_version": "3.12", "runtime": "python", "source": "tiingo", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['normalize_price_bars'] = BashOperator(
        task_id='normalize_price_bars',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_price_bars',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_price_bars", "image": {"name": "market/normalize-price-bars", "tag_from": "git_sha"}, "inputs": ["raw_alpha_vantage_daily_bars", "raw_tiingo_daily_bars"], "kind": "python_batch", "name": "normalize_price_bars", "outputs": ["clean_price_bars_candidate"], "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['validate_price_bars'] = BashOperator(
        task_id='validate_price_bars',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_price_bars',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_price_bars", "image": {"name": "market/validate-price-bars", "tag_from": "git_sha"}, "inputs": ["clean_price_bars_candidate"], "kind": "quality_check", "name": "validate_price_bars", "outputs": ["clean_price_bars_quality_scorecard"], "python_version": "3.12", "quality_profile": "clean_price_bars_v1", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['promote_price_bars'] = BashOperator(
        task_id='promote_price_bars',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_price_bars',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_price_bars", "image": {"name": "market/promote-price-bars", "tag_from": "git_sha"}, "inputs": ["clean_price_bars_candidate", "clean_price_bars_quality_scorecard"], "kind": "promotion", "name": "promote_price_bars", "outputs": ["clean_room_price_bars"], "promotion_rule": "price_bars_clean_room_v1", "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_alpha_vantage_daily_bars'] >> tasks['normalize_price_bars']
    tasks['ingest_tiingo_daily_bars'] >> tasks['normalize_price_bars']
    tasks['normalize_price_bars'] >> tasks['validate_price_bars']
    tasks['validate_price_bars'] >> tasks['promote_price_bars']
