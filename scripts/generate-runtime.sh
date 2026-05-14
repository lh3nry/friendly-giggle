#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 build/validate_specs.py
python3 build/generate_runtime.py
