# CMU School of Computer Science technical report

Publication checklist for *Bachelors In Measurement Theory*.

## Report metadata

- **Series:** Carnegie Mellon University School of Computer Science Technical
  Report
- **Number:** `CMU-CS-26-XXX` (placeholder)
- **Date:** September 2026
- **Authors:** Lars Warren Ericson
- **Institutional address:** School of Computer Science, Carnegie Mellon
  University, Pittsburgh, PA 15213

Lars Warren Ericson is an independent researcher, d/b/a Catskills Research
Company (`lars.ericson@catskillsresearch.com`).

## Build

```bash
lake exe cache get
lake build
bash scripts/build_pdf.sh
```

The build produces:

- `BachelorsInMeasurementTheory.md` — report barrel (TOC links into `report/`, including one barrel per phase);
- `BachelorsInMeasurementTheory.pdf` — report PDF for the repository;
- `BachelorsInMeasurementTheory.tex` — generated complete LaTeX source (gitignored);
- `lean-listings/` — generated report inputs (gitignored);
- `figures/` — live Mermaid diagrams rendered to PNG (gitignored; never PDF).

The title page is a standard `article` `\maketitle` followed by the abstract.

## Before public release

1. Replace every `CMU-CS-26-XXX` occurrence with the assigned CMU report
   number.
2. Confirm the author, September 2026 date, and correspondence email.
3. Run `lake build` and `bash scripts/build_pdf.sh`.
4. Inspect the cover, abstract, table of contents, list of figures, numbered
   figure captions, syllabus, course chapters, acknowledgments, references,
   and Lean module index (filenames and GitHub links, not source reprints).
