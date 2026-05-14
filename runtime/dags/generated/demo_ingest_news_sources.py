"""
Generated demo DAG from specs/dags.yaml.

Source DAG: demo_ingest_news_sources
Description: Stub ingestion for Kaggle, Finnhub, and Alpha Vantage news inputs.
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
    dag_id='demo_ingest_news_sources',
    description='Stub ingestion for Kaggle, Finnhub, and Alpha Vantage news inputs.',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["demo", "market-data", "generated"],
) as dag:
    tasks = {}

    tasks['ingest_kaggle_stock_news'] = BashOperator(
        task_id='ingest_kaggle_stock_news',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_kaggle_stock_news',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_kaggle_stock_news", "image": {"name": "market/ingest-kaggle-stock-news", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_kaggle_stock_news", "outputs": ["raw_kaggle_stock_news"], "python_version": "3.12", "runtime": "python", "source": "kaggle_stock_news", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_finnhub_company_news'] = BashOperator(
        task_id='ingest_finnhub_company_news',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_finnhub_company_news',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_finnhub_company_news", "image": {"name": "market/ingest-finnhub-company-news", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_finnhub_company_news", "outputs": ["raw_finnhub_company_news"], "python_version": "3.12", "runtime": "python", "source": "finnhub_open_data", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['ingest_alpha_vantage_news_sentiment'] = BashOperator(
        task_id='ingest_alpha_vantage_news_sentiment',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_alpha_vantage_news_sentiment',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task ingest_alpha_vantage_news_sentiment", "image": {"name": "market/ingest-alpha-vantage-news-sentiment", "tag_from": "git_sha"}, "kind": "stub_ingestion", "name": "ingest_alpha_vantage_news_sentiment", "outputs": ["raw_alpha_vantage_news_sentiment"], "python_version": "3.12", "runtime": "python", "source": "alpha_vantage", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

