#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

scripts/generate-runtime.sh
test -n "$(find runtime/dags/generated -name '*.py' -print -quit)"
python3 -m py_compile runtime/dags/generated/*.py
