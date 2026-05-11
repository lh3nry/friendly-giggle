#!/usr/bin/env python3
"""
Generate runtime artifacts from the lightweight control-plane specs.
For now this is a placeholder. The intended outputs are:
- generated Airflow DAGs
- generated Docker Buildx Bake targets
- generated quality-suite configs
- generated runtime manifests
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"


def main() -> None:
    for path in [
        RUNTIME / "dags" / "generated",
        RUNTIME / "docker" / "generated",
        RUNTIME / "quality" / "generated",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    (RUNTIME / "docker-bake.generated.hcl").write_text(
        '''group "default" {
  targets = ["ingest_news", "normalize_news", "validate_clean_news"]
}

target "ingest_news" {
  context = "./tasks/ingest_news"
  tags = ["market/ingest-news:${GIT_SHA}"]
}

target "normalize_news" {
  context = "./tasks/normalize_news"
  tags = ["market/normalize-news:${GIT_SHA}"]
}

target "validate_clean_news" {
  context = "./tasks/validate_clean_news"
  tags = ["market/validate-clean-news:${GIT_SHA}"]
}
''',
        encoding="utf-8",
    )

    print("Generated runtime artifacts.")


if __name__ == "__main__":
    main()
