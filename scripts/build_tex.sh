#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "==> Regenerating Graphviz module-dependency SVGs"
python3 scripts/insert_solution_dep_figures.py
echo "==> Expanding BachelorsInMeasurementTheory.md"
bash scripts/generate_report.sh
echo "==> Building BachelorsInMeasurementTheory.tex + lean-listings/ + figures/"
python3 scripts/build_tex.py
