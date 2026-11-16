#!/usr/bin/env bash
# Regenerate BachelorsInMeasurementTheory.tex and compile the repo PDF.
set -euo pipefail
cd "$(dirname "$0")/.."

TEX="BachelorsInMeasurementTheory.tex"
PDF="BachelorsInMeasurementTheory.pdf"

echo "==> Regenerating ${TEX} + lean-listings/ + figures/"
bash scripts/build_arxiv_tex.sh

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
