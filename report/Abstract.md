## Abstract

This report presents a reconstructed Carnegie Mellon undergraduate path
through the Mathematical Sciences 21-xxx catalog, sequenced so that Dana
Scott's 1964 measurement theorems (1.1--4.1) and their extension to infinite
Boolean algebras can be read for understanding after these courses are taken
and proved end to end. Each course contributes one
problem that requires the full toolkit of that course rather than a single
technique in isolation. Solutions are written in English and then formalized
in Lean 4 / Mathlib. The accompanying library `BachelorsInMeasurementTheory` is
sorry-free under the pinned toolchain `leanprover/lean4:v4.36.0-rc2` and
introduces no project axioms beyond Mathlib's classical footprint. Large-language-model
assistance was used in drafting solutions, but every accepted declaration is
checked by Lean's kernel. The complete source and a reproducible build
pipeline are publicly available with this report.
