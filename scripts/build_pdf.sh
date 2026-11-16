#!/usr/bin/env bash
# Regenerate the report Markdown and TeX, then compile the repository PDF.
set -euo pipefail
cd "$(dirname "$0")/.."

TEX="BachelorsInMeasurementTheory.tex"
PDF="BachelorsInMeasurementTheory.pdf"

echo "==> Regenerating BachelorsInMeasurementTheory.md, ${TEX}, lean-listings/, and figures/"
bash scripts/build_tex.sh

echo "==> Compiling PDF (pdfLaTeX via latexmk)"
latexmk -C "$TEX" >/dev/null 2>&1 || true
rm -f BachelorsInMeasurementTheory.aux BachelorsInMeasurementTheory.out \
  BachelorsInMeasurementTheory.toc BachelorsInMeasurementTheory.lof
latexmk -pdf \
  -pdflatex="pdflatex -interaction=nonstopmode -halt-on-error" \
  -interaction=nonstopmode \
  -halt-on-error \
  "$TEX" || {
  echo "latexmk reported errors; tail of log:" >&2
  tail -n 60 BachelorsInMeasurementTheory.log >&2 || true
  exit 1
}

echo "wrote $PDF ($(du -h "$PDF" | cut -f1))"
