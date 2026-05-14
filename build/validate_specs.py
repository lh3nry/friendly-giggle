#!/usr/bin/env python3
"""Validate cross references in the demo control-plane specs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "specs"


def load_spec(name: str) -> dict[str, Any]:
    with (SPECS / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    assets = load_spec("assets.yaml")["assets"]
    sources = load_spec("sources.yaml")["sources"]
    dags = load_spec("dags.yaml")["dags"]
    tasks = load_spec("tasks.yaml")["tasks"]
    quality_profiles = load_spec("quality_profiles.yaml")["quality_profiles"]
    promotion_rules = load_spec("promotion_rules.yaml")["promotion_rules"]
    source_schemas = load_spec("source_schemas.yaml")["source_schemas"]

    asset_names = {asset["name"] for asset in assets}
    source_names = {source["name"] for source in sources}
    task_names = {task["name"] for task in tasks}
    quality_profile_names = {profile["name"] for profile in quality_profiles}
    promotion_rule_names = {rule["name"] for rule in promotion_rules}
    source_schema_names = {schema["name"] for schema in source_schemas}

    for asset in assets:
        for dependency in asset.get("depends_on", []):
            require(
                dependency in asset_names,
                f"asset {asset['name']} depends on unknown asset {dependency}",
                errors,
            )
        if "source" in asset:
            require(
                asset["source"] in source_names,
                f"asset {asset['name']} references unknown source {asset['source']}",
                errors,
            )

    for task in tasks:
        if "source" in task:
            require(
                task["source"] in source_names,
                f"task {task['name']} references unknown source {task['source']}",
                errors,
            )
        for field in ("inputs", "outputs"):
            for asset_name in task.get(field, []):
                require(
                    asset_name in asset_names,
                    f"task {task['name']} {field} unknown asset {asset_name}",
                    errors,
                )
        if "quality_profile" in task:
            require(
                task["quality_profile"] in quality_profile_names,
                f"task {task['name']} references unknown quality profile {task['quality_profile']}",
                errors,
            )
        if "promotion_rule" in task:
            require(
                task["promotion_rule"] in promotion_rule_names,
                f"task {task['name']} references unknown promotion rule {task['promotion_rule']}",
                errors,
            )

    for profile in quality_profiles:
        require(
            profile["asset"] in asset_names,
            f"quality profile {profile['name']} references unknown asset {profile['asset']}",
            errors,
        )

    for rule in promotion_rules:
        for field in ("input_asset", "scorecard_asset", "output_asset"):
            require(
                rule[field] in asset_names,
                f"promotion rule {rule['name']} {field} unknown asset {rule[field]}",
                errors,
            )

    for schema in source_schemas:
        require(
            schema["asset"] in asset_names,
            f"source schema {schema['name']} references unknown asset {schema['asset']}",
            errors,
        )
        require(
            schema["name"].endswith("_v1"),
            f"source schema {schema['name']} should include a version suffix",
            errors,
        )

    for dag in dags:
        dag_tasks = set(dag["tasks"])
        for task_name in dag["tasks"]:
            require(task_name in task_names, f"dag {dag['name']} references unknown task {task_name}", errors)
        for edge in dag.get("dependencies", []):
            require(edge["from"] in dag_tasks, f"dag {dag['name']} edge from unknown task {edge['from']}", errors)
            require(edge["to"] in dag_tasks, f"dag {dag['name']} edge to unknown task {edge['to']}", errors)
        asset_trigger = dag.get("schedule", {}).get("asset_trigger") if isinstance(dag.get("schedule"), dict) else None
        if asset_trigger:
            for mode in ("any", "all"):
                for asset_name in asset_trigger.get(mode, []):
                    require(
                        asset_name in asset_names,
                        f"dag {dag['name']} asset trigger references unknown asset {asset_name}",
                        errors,
                    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print(
        f"Validated {len(sources)} sources, {len(assets)} assets, "
        f"{len(tasks)} tasks, {len(source_schema_names)} source schemas, and {len(dags)} DAGs."
    )


if __name__ == "__main__":
    main()
