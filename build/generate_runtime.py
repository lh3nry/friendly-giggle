#!/usr/bin/env python3
"""
Generate local demo runtime artifacts from the control-plane specs.

The spec files are JSON-compatible YAML, which keeps this compiler free of
runtime dependencies while preserving the .yaml extension used by the repo.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "specs"
RUNTIME = ROOT / "runtime"


def load_spec(name: str) -> dict[str, Any]:
    with (SPECS / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", value).strip("_").lower()


def python_literal(value: Any) -> str:
    return repr(value).replace("None", "None")


def render_dag(dag: dict[str, Any], tasks_by_name: dict[str, dict[str, Any]]) -> str:
    task_names = dag["tasks"]
    task_specs = {name: tasks_by_name[name] for name in task_names}
    dependencies = dag.get("dependencies", [])
    schedule = dag.get("schedule")
    schedule_interval = schedule if isinstance(schedule, str) else None

    command_by_task = {
        name: spec["entrypoint"].replace("/opt/airflow/repo/", "/opt/airflow/repo/")
        for name, spec in task_specs.items()
    }

    return textwrap.dedent(
        f'''\
        """
        Generated demo DAG from specs/dags.yaml.

        Source DAG: {dag["name"]}
        Description: {dag.get("description", "No description provided.")}
        """

        from __future__ import annotations

        from datetime import datetime

        from airflow import DAG
        from airflow.operators.bash import BashOperator


        DEFAULT_ARGS = {{
            "owner": "friendly-giggle",
            "depends_on_past": False,
        }}


        with DAG(
            dag_id={dag["name"]!r},
            description={dag.get("description", "")!r},
            default_args=DEFAULT_ARGS,
            start_date=datetime(2024, 1, 1),
            schedule_interval={schedule_interval!r},
            catchup=False,
            tags=["demo", "market-data", "generated"],
        ) as dag:
            tasks = {{}}

        '''
    ) + "".join(
        textwrap.indent(
            textwrap.dedent(
                f'''\
                tasks[{task_name!r}] = BashOperator(
                    task_id={task_name!r},
                    bash_command={command_by_task[task_name]!r},
                    env={{
                        "FRIENDLY_GIGGLE_OUTPUT_DIR": "/opt/airflow/data/demo",
                        "FRIENDLY_GIGGLE_TASK_SPEC": {json.dumps(task_specs[task_name], sort_keys=True)!r},
                    }},
                    append_env=True,
                )

                '''
            ),
            "    ",
        )
        for task_name in task_names
    ) + "".join(
        textwrap.indent(
            f"tasks[{edge['from']!r}] >> tasks[{edge['to']!r}]\n",
            "    ",
        )
        for edge in dependencies
    )


def render_bake(tasks: list[dict[str, Any]]) -> str:
    names = [task["name"] for task in tasks]
    lines = [
        'group "default" {',
        "  targets = [" + ", ".join(json.dumps(name) for name in names) + "]",
        "}",
        "",
    ]

    for task in tasks:
        image = task["image"]
        lines.extend(
            [
                f'target "{task["name"]}" {{',
                f'  context = "./{task["source_dir"]}"',
                f'  tags = ["{image["name"]}:${{GIT_SHA}}"]',
                "}",
                "",
            ]
        )

    return "\n".join(lines)


def render_task_manifest(task: dict[str, Any]) -> str:
    return json.dumps(task, indent=2, sort_keys=True) + "\n"


def render_quality_manifest(profile: dict[str, Any]) -> str:
    return json.dumps(profile, indent=2, sort_keys=True) + "\n"


def main() -> None:
    assets = load_spec("assets.yaml")["assets"]
    sources = load_spec("sources.yaml")["sources"]
    dags = load_spec("dags.yaml")["dags"]
    tasks = load_spec("tasks.yaml")["tasks"]
    quality_profiles = load_spec("quality_profiles.yaml")["quality_profiles"]
    promotion_rules = load_spec("promotion_rules.yaml")["promotion_rules"]
    source_schemas = load_spec("source_schemas.yaml")["source_schemas"]

    tasks_by_name = {task["name"]: task for task in tasks}

    for path in [
        RUNTIME / "dags" / "generated",
        RUNTIME / "docker" / "generated",
        RUNTIME / "quality" / "generated",
        RUNTIME / "manifests" / "generated",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    for dag in dags:
        write_text(
            RUNTIME / "dags" / "generated" / f"{slug(dag['name'])}.py",
            render_dag(dag, tasks_by_name),
        )

    write_text(RUNTIME / "docker-bake.generated.hcl", render_bake(tasks))

    for task in tasks:
        write_text(
            RUNTIME / "manifests" / "generated" / f"task.{slug(task['name'])}.json",
            render_task_manifest(task),
        )

    for profile in quality_profiles:
        write_text(
            RUNTIME / "quality" / "generated" / f"{slug(profile['name'])}.json",
            render_quality_manifest(profile),
        )

    write_text(
        RUNTIME / "manifests" / "generated" / "sources.json",
        json.dumps({"sources": sources}, indent=2, sort_keys=True) + "\n",
    )
    write_text(
        RUNTIME / "manifests" / "generated" / "assets.json",
        json.dumps({"assets": assets}, indent=2, sort_keys=True) + "\n",
    )
    write_text(
        RUNTIME / "manifests" / "generated" / "promotion_rules.json",
        json.dumps({"promotion_rules": promotion_rules}, indent=2, sort_keys=True) + "\n",
    )
    write_text(
        RUNTIME / "manifests" / "generated" / "source_schemas.json",
        json.dumps({"source_schemas": source_schemas}, indent=2, sort_keys=True) + "\n",
    )

    print(
        "Generated "
        f"{len(dags)} DAGs, {len(tasks)} task manifests, "
        f"{len(quality_profiles)} quality profiles, {len(source_schemas)} source schemas, "
        "and Docker bake targets."
    )


if __name__ == "__main__":
    main()
