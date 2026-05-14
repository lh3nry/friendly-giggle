"""
Generated demo DAG from specs/dags.yaml.

Source DAG: demo_prepare_news_clean_room
Description: Normalize multi-source news, validate it, and promote it to the clean room.
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
    dag_id='demo_prepare_news_clean_room',
    description='Normalize multi-source news, validate it, and promote it to the clean room.',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["demo", "market-data", "generated"],
) as dag:
    tasks = {}

    tasks['normalize_news'] = BashOperator(
        task_id='normalize_news',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_news',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task normalize_news", "image": {"name": "market/normalize-news", "tag_from": "git_sha"}, "inputs": ["raw_kaggle_stock_news", "raw_finnhub_company_news", "raw_alpha_vantage_news_sentiment"], "kind": "python_batch", "name": "normalize_news", "outputs": ["clean_news_candidate"], "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['validate_clean_news'] = BashOperator(
        task_id='validate_clean_news',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_clean_news',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_clean_news", "image": {"name": "market/validate-clean-news", "tag_from": "git_sha"}, "inputs": ["clean_news_candidate"], "kind": "quality_check", "name": "validate_clean_news", "outputs": ["clean_news_quality_scorecard"], "python_version": "3.12", "quality_profile": "clean_news_v1", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['promote_clean_news'] = BashOperator(
        task_id='promote_clean_news',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_clean_news',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_clean_news", "image": {"name": "market/promote-clean-news", "tag_from": "git_sha"}, "inputs": ["clean_news_candidate", "clean_news_quality_scorecard"], "kind": "promotion", "name": "promote_clean_news", "outputs": ["clean_room_news"], "promotion_rule": "news_clean_room_v1", "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['normalize_news'] >> tasks['validate_clean_news']
    tasks['validate_clean_news'] >> tasks['promote_clean_news']
