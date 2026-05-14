"""
Generated demo DAG from specs/dags.yaml.

Source DAG: demo_prepare_company_reference
Description: Ingest provider reference data and promote a clean company reference asset.
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
    dag_id='demo_prepare_company_reference',
    description='Ingest provider reference data and promote a clean company reference asset.',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["demo", "market-data", "generated"],
) as dag:
    tasks = {}

    tasks['ingest_finnhub_company_profile'] = BashOperator(
        task_id='ingest_finnhub_company_profile',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_finnhub_company_profile',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_finnhub_company_profile", "image": {"name": "market/ingest-finnhub-company-profile", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_finnhub_company_profile", "outputs": ["raw_finnhub_company_profile"], "python_version": "3.12", "runtime": "python", "source": "finnhub_open_data", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_tiingo_symbol_metadata'] = BashOperator(
        task_id='ingest_tiingo_symbol_metadata',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_tiingo_symbol_metadata',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_tiingo_symbol_metadata", "image": {"name": "market/ingest-tiingo-symbol-metadata", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_tiingo_symbol_metadata", "outputs": ["raw_tiingo_symbol_metadata"], "python_version": "3.12", "runtime": "python", "source": "tiingo", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['normalize_company_reference'] = BashOperator(
        task_id='normalize_company_reference',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_company_reference',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_company_reference", "image": {"name": "market/normalize-company-reference", "tag_from": "git_sha"}, "inputs": ["raw_finnhub_company_profile", "raw_tiingo_symbol_metadata"], "kind": "python_batch", "name": "normalize_company_reference", "outputs": ["clean_company_reference_candidate"], "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['validate_company_reference'] = BashOperator(
        task_id='validate_company_reference',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_company_reference',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_company_reference", "image": {"name": "market/validate-company-reference", "tag_from": "git_sha"}, "inputs": ["clean_company_reference_candidate"], "kind": "quality_check", "name": "validate_company_reference", "outputs": ["clean_company_reference_quality_scorecard"], "python_version": "3.12", "quality_profile": "company_reference_v1", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['promote_company_reference'] = BashOperator(
        task_id='promote_company_reference',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_company_reference',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_company_reference", "image": {"name": "market/promote-company-reference", "tag_from": "git_sha"}, "inputs": ["clean_company_reference_candidate", "clean_company_reference_quality_scorecard"], "kind": "promotion", "name": "promote_company_reference", "outputs": ["clean_room_company_reference"], "promotion_rule": "company_reference_clean_room_v1", "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_alpha_vantage_company_overview'] = BashOperator(
        task_id='ingest_alpha_vantage_company_overview',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_alpha_vantage_company_overview',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_alpha_vantage_company_overview", "image": {"name": "market/ingest-alpha-vantage-company-overview", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_alpha_vantage_company_overview", "outputs": ["raw_alpha_vantage_company_overview"], "python_version": "3.12", "runtime": "python", "source": "alpha_vantage", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['normalize_fundamentals'] = BashOperator(
        task_id='normalize_fundamentals',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_fundamentals',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_fundamentals", "image": {"name": "market/normalize-fundamentals", "tag_from": "git_sha"}, "inputs": ["raw_alpha_vantage_company_overview", "clean_room_company_reference"], "kind": "python_batch", "name": "normalize_fundamentals", "outputs": ["clean_fundamentals_candidate"], "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_finnhub_company_profile'] >> tasks['normalize_company_reference']
    tasks['ingest_tiingo_symbol_metadata'] >> tasks['normalize_company_reference']
    tasks['normalize_company_reference'] >> tasks['validate_company_reference']
    tasks['validate_company_reference'] >> tasks['promote_company_reference']
    tasks['promote_company_reference'] >> tasks['normalize_fundamentals']
    tasks['ingest_alpha_vantage_company_overview'] >> tasks['normalize_fundamentals']
