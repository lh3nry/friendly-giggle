"""
Generated demo DAG from specs/dags.yaml.

Source DAG: demo_build_training_feature_panel
Description: Join clean-room news, prices, reference data, and fundamentals into a trusted training feature panel.
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
    dag_id='demo_build_training_feature_panel',
    description='Join clean-room news, prices, reference data, and fundamentals into a trusted training feature panel.',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["demo", "market-data", "generated"],
) as dag:
    tasks = {}

    tasks['build_market_feature_panel'] = BashOperator(
        task_id='build_market_feature_panel',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task build_market_feature_panel',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task build_market_feature_panel", "image": {"name": "market/build-market-feature-panel", "tag_from": "git_sha"}, "inputs": ["clean_room_news", "clean_room_price_bars", "clean_room_company_reference", "clean_fundamentals_candidate"], "kind": "python_batch", "name": "build_market_feature_panel", "outputs": ["training_market_feature_panel_candidate"], "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['validate_market_feature_panel'] = BashOperator(
        task_id='validate_market_feature_panel',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_market_feature_panel',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task validate_market_feature_panel", "image": {"name": "market/validate-market-feature-panel", "tag_from": "git_sha"}, "inputs": ["training_market_feature_panel_candidate"], "kind": "quality_check", "name": "validate_market_feature_panel", "outputs": ["training_market_feature_panel_quality_scorecard"], "python_version": "3.12", "quality_profile": "market_feature_panel_v1", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['promote_market_feature_panel'] = BashOperator(
        task_id='promote_market_feature_panel',
        bash_command='python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_market_feature_panel',
        env={
            "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
            "FRIENDLY_GIGGLE_TASK_SPEC": '{"entrypoint": "python /opt/airflow/repo/runtime/stubs/run_task.py --task promote_market_feature_panel", "image": {"name": "market/promote-market-feature-panel", "tag_from": "git_sha"}, "inputs": ["training_market_feature_panel_candidate", "training_market_feature_panel_quality_scorecard"], "kind": "promotion", "name": "promote_market_feature_panel", "outputs": ["trusted_training_market_feature_panel"], "promotion_rule": "market_feature_panel_training_v1", "python_version": "3.12", "runtime": "python", "source_dir": "runtime/stubs"}',
        },
        append_env=True,
    )

    tasks['build_market_feature_panel'] >> tasks['validate_market_feature_panel']
    tasks['validate_market_feature_panel'] >> tasks['promote_market_feature_panel']
