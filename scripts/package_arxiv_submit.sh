#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TEX="arxiv.tex"
LISTINGS_DIR="lean-listings"
FIGURES_DIR="figures"
OUT_DIR="dist"
ZIP="${OUT_DIR}/arxiv_submit.zip"

if [[ "${1:-}" != "--skip-tex-build" ]]; then
  bash scripts/build_arxiv_tex.sh
fi

mapfile -t FIGURE_ASSETS < <(
  {
    find "$FIGURES_DIR" -maxdepth 1 -name 'figure-*.png'
    find "$FIGURES_DIR/deps" -maxdepth 1 \( -name '*.pdf' -o -name '*.png' -o -name '*.svg' -o -name '*.dot' \)
  } 2>/dev/null | sort
)

missing=0
for f in "$TEX"; do
  if [[ ! -f "$f" ]]; then
    echo "error: missing $f" >&2
    missing=1
  fi
done
if [[ ! -d "$LISTINGS_DIR" ]] || [[ -z "$(find "$LISTINGS_DIR" -maxdepth 1 -type f 2>/dev/null)" ]]; then
  echo "error: missing listings in $LISTINGS_DIR" >&2
  missing=1
fi
if [[ ${#FIGURE_ASSETS[@]} -eq 0 ]]; then
  echo "error: no figure assets in $FIGURES_DIR" >&2
  missing=1
fi
if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

mkdir -p "$OUT_DIR"
rm -f "$ZIP"

python3 - <<'PY'
import json
from pathlib import Path

sources = [
    {"filename": "arxiv.tex", "usage": "toplevel"},
]
for path in sorted(p for p in Path("lean-listings").iterdir() if p.is_file()):
    sources.append({"filename": path.as_posix(), "usage": "include"})
for path in sorted(Path("figures").glob("figure-*.png")):
    sources.append({"filename": path.as_posix(), "usage": "include"})
deps = Path("figures/deps")
if deps.is_dir():
    for path in sorted(deps.glob("*.pdf")):
        sources.append({"filename": path.as_posix(), "usage": "include"})
Path("00README.json").write_text(
    json.dumps({"process": {"compiler": "pdflatex"}, "sources": sources}, indent=2) + "\n"
)
print(f"  {len(sources)} sources")
PY

zip -r "$ZIP" 00README.json "$TEX" "$LISTINGS_DIR" "${FIGURE_ASSETS[@]}"
echo "wrote $ZIP ($(du -h "$ZIP" | cut -f1))"
