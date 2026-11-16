#!/usr/bin/env python3
"""Insert a Graphviz SVG dependency figure under each course Solution heading.

Mathlib imports use an amber node fill; this course's solution modules use a
blue fill; prior-course modules use a green fill with the course id under the
name (no Mathlib edges for those). Color alone distinguishes the kinds.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEPS_DIR = ROOT / "figures" / "deps"

COURSE_LEANS: list[tuple[str, str, str, list[str]]] = [
    ("21-120.md", "21-120", "Course21120", ["BachelorsInMeasurementTheory/Course21120/FTC.lean"]),
    ("21-122.md", "21-122", "Course21122", [
        "BachelorsInMeasurementTheory/Course21122/Existence.lean",
        "BachelorsInMeasurementTheory/Course21122/TailBound.lean",
        "BachelorsInMeasurementTheory/Course21122/TaylorExpansion.lean",
        "BachelorsInMeasurementTheory/Course21122/TaylorEstimate.lean",
        "BachelorsInMeasurementTheory/Course21122/TaylorError.lean",
        "BachelorsInMeasurementTheory/Course21122/Summary.lean",
    ]),
    ("21-127.md", "21-127", "Course21127", ["BachelorsInMeasurementTheory/Course21127.lean"]),
    ("21-241.md", "21-241", "Course21241", ["BachelorsInMeasurementTheory/Course21241.lean"]),
    ("21-228.md", "21-228", "Course21228", ["BachelorsInMeasurementTheory/Course21228.lean"]),
    ("21-355.md", "21-355", "Course21355", ["BachelorsInMeasurementTheory/Course21355.lean"]),
    ("21-373.md", "21-373", "Course21373", ["BachelorsInMeasurementTheory/Course21373.lean"]),
    ("21-321.md", "21-321", "Course21321", ["BachelorsInMeasurementTheory/Course21321.lean"]),
    ("21-292.md", "21-292", "Course21292", ["BachelorsInMeasurementTheory/Course21292.lean"]),
    ("21-329.md", "21-329", "Course21329", ["BachelorsInMeasurementTheory/Course21329.lean"]),
    ("21-651.md", "21-651", "Course21651", ["BachelorsInMeasurementTheory/Course21651.lean"]),
    ("21-720.md", "21-720", "Course21720", ["BachelorsInMeasurementTheory/Course21720.lean"]),
    ("21-640.md", "21-640", "Course21640", ["BachelorsInMeasurementTheory/Course21640.lean"]),
    ("21-410-21-599.md", "21-410 / 21-599", "Course21410", ["BachelorsInMeasurementTheory/Course21410.lean"]),
    ("21-322.md", "21-322", "Course21322", ["BachelorsInMeasurementTheory/Course21322.lean"]),
]

# Prior-course Lean modules shown as green external nodes (no Mathlib fan-in).
# Map graph stem -> list of (lean path relative to repo, course label).
PRIOR_MODULES: dict[str, list[tuple[str, str]]] = {
    "Course21122": [
        ("BachelorsInMeasurementTheory/Course21120/FTC.lean", "21-120"),
    ],
}

IMPORT_RE = re.compile(
    r"^(?:public\s+(?:meta\s+)?)?import\s+(\S+)\s*$",
    re.MULTILINE,
)
MARKER_RE = re.compile(
    r"\n?<!-- lean-dep-figure -->.*?<!-- /lean-dep-figure -->\n?",
    re.DOTALL,
)

# Amber Mathlib / blue local / green prior-course.
MATHLIB_FILL = "#ffedd5"
MATHLIB_STROKE = "#c2410c"
MATHLIB_FONT = "#7c2d12"
LOCAL_FILL = "#dbeafe"
LOCAL_STROKE = "#1d4ed8"
LOCAL_FONT = "#1e3a8a"
PRIOR_FILL = "#dcfce7"
PRIOR_STROKE = "#15803d"
PRIOR_FONT = "#14532d"

MATHLIB_HINTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bHasDerivAt\b|\bDifferentiableAt\b|\bderiv\b"), "Analysis.Calculus.Deriv"),
    (re.compile(r"\bintegral\b|intervalIntegral|integral_inv"), "MeasureTheory.Integral.IntervalIntegral"),
    (re.compile(r"\barctan\b"), "Analysis.SpecialFunctions.Arctan"),
    (re.compile(r"\bsin\b|\bcos\b|continuous_sin|abs_sin"), "Analysis.SpecialFunctions.Trigonometric"),
    (re.compile(r"\bIsCompact\b|isCompact_Icc"), "Topology.Compactness.Compact"),
    (re.compile(r"\bTendsto\b|\batTop\b|\b𝓝\b|Filter\."), "Order.Filter.Basic"),
    (re.compile(r"\blimsup\b|\bliminf\b|ciSup|ciInf|tailSup|tailInf"), "Order.LiminfLimsup"),
    (re.compile(r"\bBooleanAlgebra\b"), "Order.BooleanAlgebra"),
    (re.compile(r"\bLattice\b|\bBoundedOrder\b"), "Order.BoundedOrder"),
    (re.compile(r"\bZorn\b|zorn"), "Order.Zorn"),
    (re.compile(r"\bCardinal\b"), "SetTheory.Cardinal.Basic"),
    (re.compile(r"\bLinearMap\b|→ₗ"), "Algebra.Module.LinearMap.Basic"),
    (re.compile(r"\bNormedSpace\b|\bNormedAddCommGroup\b|‖"), "Analysis.NormedSpace.Basic"),
    (re.compile(r"\bAddCommGroup\b|\bModule ℝ\b|SublinearFunctional"), "Algebra.Module.Basic"),
    (re.compile(r"\binner\b|\bInnerProductSpace\b"), "Analysis.InnerProductSpace.Basic"),
    (re.compile(r"\bBasis\b"), "LinearAlgebra.Basis.Basic"),
    (re.compile(r"\bPerm\b"), "Data.Fintype.Perm"),
    (re.compile(r"\bFintype\b"), "Data.Fintype.Basic"),
    (re.compile(r"\bFinset\b|∑ |BigOperators"), "Algebra.BigOperators.Group.Finset.Basic"),
    (re.compile(r"\bQuotient\b|\bSetoid\b|\bEquiv\b"), "Order.Setoid.Basic"),
    (re.compile(r"\bWellFounded\b|\bAcc\b|well.?order", re.I), "Order.WellFounded"),
    (re.compile(r"\bℚ\b|\bRat\b"), "Data.Rat.Defs"),
    (re.compile(r"\bℤ\b"), "Data.Int.Basic"),
    (re.compile(r"\bℝ\b"), "Basic.Real.Basic"),
    (re.compile(r"\bContinuousMap\b|\bC\("), "Topology.ContinuousMap.Basic"),
    (re.compile(r"\bIsClosed\b|\bIsOpen\b|\bContinuous\b"), "Topology.Basic"),
    (re.compile(r"\bIsAtom\b|IsBooleanAtom"), "Order.Atoms"),
    (re.compile(r"linarith|nlinarith"), "Tactic.Linarith"),
    (re.compile(r"\bnorm_num\b"), "Tactic.NormNum"),
]


def is_import_line(ln: str) -> bool:
    s = ln.strip()
    return (
        s.startswith("import ")
        or s.startswith("public import ")
        or s.startswith("public meta import ")
    )


def is_import_only(code: str) -> bool:
    """True for barrel files: module header + imports, no declarations."""
    lines = []
    for ln in code.splitlines():
        s = ln.strip()
        if not s or s.startswith("--") or s.startswith("/-"):
            continue
        if s == "module" or s.startswith("module ") or s.startswith("@[expose]"):
            continue
        lines.append(s)
    return bool(lines) and all(is_import_line(ln) for ln in lines)


def course_files(seeds: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()

    def add(rel: str) -> None:
        if rel not in seen and (ROOT / rel).is_file():
            seen.add(rel)
            out.append(rel)

    for rel in seeds:
        add(rel)
        path = ROOT / rel
        sibling = path.with_suffix("") if path.suffix == ".lean" else path
        if sibling.is_dir():
            for child in sorted(sibling.rglob("*.lean")):
                add(child.relative_to(ROOT).as_posix())
    return out


def parse_imports(code: str) -> list[str]:
    return IMPORT_RE.findall(code)


def infer_mathlib(code: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for pat, mod in MATHLIB_HINTS:
        if pat.search(code) and mod not in seen:
            seen.add(mod)
            found.append(mod)
    return found


def module_label(rel: str) -> str:
    name = Path(rel).stem
    if name.startswith("Course") and name[-3:].isdigit():
        return name
    for prefix in (
        "Course21120",
        "Course21122",
        "Course21127",
        "Course21228",
        "Course21241",
        "Course21292",
        "Course21321",
        "Course21322",
        "Course21329",
        "Course21355",
        "Course21373",
        "Course21410",
        "Course21640",
        "Course21651",
        "Course21720",
    ):
        if name.startswith(prefix):
            rest = name[len(prefix) :]
            return rest or name
    return name


def sid(prefix: str, name: str) -> str:
    return prefix + re.sub(r"[^A-Za-z0-9]", "", name)


def lean_path(imp: str) -> str | None:
    if not imp.startswith("BachelorsInMeasurementTheory."):
        return None
    return imp.replace(".", "/") + ".lean"


def mathlib_names(code: str) -> list[str]:
    imports = [imp for imp in parse_imports(code) if imp.startswith("Mathlib")]
    if imports == ["Mathlib"]:
        return infer_mathlib(code)
    if not imports:
        return [] if is_import_only(code) else infer_mathlib(code)
    return [imp.removeprefix("Mathlib.") for imp in imports]


def ancestors(node: str, preds: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    stack = list(preds.get(node, ()))
    while stack:
        parent = stack.pop()
        if parent in seen:
            continue
        seen.add(parent)
        stack.extend(preds.get(parent, ()))
    return seen


def dot_escape(label: str) -> str:
    return label.replace("\\", "\\\\").replace('"', '\\"')


def graph_for(
    rels: list[str],
    graph_name: str,
    priors: list[tuple[str, str]] | None = None,
) -> str:
    priors = priors or []
    prior_course = {rel: course for rel, course in priors if (ROOT / rel).is_file()}
    files = {rel: (ROOT / rel).read_text(encoding="utf-8") for rel in rels}
    for rel in prior_course:
        if rel not in files:
            files[rel] = (ROOT / rel).read_text(encoding="utf-8")

    local = [rel for rel in rels if rel not in prior_course]
    displayed_local = [rel for rel in local if not is_import_only(files[rel])]
    if not displayed_local:
        displayed_local = list(local)

    # Only show prior modules that some local module imports.
    preds: dict[str, set[str]] = {rel: set() for rel in files}
    mathlib_of: dict[str, set[str]] = {}
    for rel, code in files.items():
        # Prior modules contribute no Mathlib fan-in.
        mathlib_of[rel] = set() if rel in prior_course else set(mathlib_names(code))
        for imp in parse_imports(code):
            dest = lean_path(imp)
            if dest in files:
                preds[rel].add(dest)

    used_priors = sorted(
        {
            dest
            for rel in displayed_local
            for dest in preds[rel]
            if dest in prior_course
        },
        key=lambda r: Path(r).stem,
    )

    mathlib_ids = {
        ml: sid("L", ml)
        for rel in displayed_local
        for ml in mathlib_of[rel]
    }
    module_ids = {
        rel: sid("M", Path(rel).stem) for rel in displayed_local + used_priors
    }

    edges: list[tuple[str, str]] = []
    for rel in displayed_local:
        mid = module_ids[rel]
        inherited: set[str] = set()
        for anc in ancestors(rel, preds):
            if anc in prior_course:
                continue
            inherited |= mathlib_of.get(anc, set())
        for ml in mathlib_of[rel]:
            if ml not in inherited:
                edges.append((mathlib_ids[ml], mid))
        for dest in preds[rel]:
            if dest in module_ids:
                edges.append((module_ids[dest], mid))

    lines = [
        f"digraph {graph_name} {{",
        "  rankdir=LR;",
        '  graph [nodesep=0.18, ranksep=0.45, pad=0.12, bgcolor="white"];',
        '  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11];',
        '  edge [color="#334155", arrowsize=0.7];',
        "",
    ]
    for ml, lid in sorted(mathlib_ids.items(), key=lambda kv: kv[0].lower()):
        lines.append(
            f'  {lid} [label="{dot_escape(ml)}",'
            f' fillcolor="{MATHLIB_FILL}", color="{MATHLIB_STROKE}",'
            f' fontcolor="{MATHLIB_FONT}"];'
        )
    for rel in used_priors:
        mid = module_ids[rel]
        name = dot_escape(module_label(rel))
        course = dot_escape(prior_course[rel])
        lines.append(
            f'  {mid} [label=<{name}<br/>{course}>,'
            f' fillcolor="{PRIOR_FILL}", color="{PRIOR_STROKE}",'
            f' fontcolor="{PRIOR_FONT}"];'
        )
    for rel in displayed_local:
        mid = module_ids[rel]
        label = module_label(rel)
        lines.append(
            f'  {mid} [label="{dot_escape(label)}",'
            f' fillcolor="{LOCAL_FILL}", color="{LOCAL_STROKE}",'
            f' fontcolor="{LOCAL_FONT}"];'
        )
    lines.append("")
    seen_e: set[tuple[str, str]] = set()
    known = set(mathlib_ids.values()) | set(module_ids.values())
    for src, dst in edges:
        if src == dst or (src, dst) in seen_e or src not in known or dst not in known:
            continue
        seen_e.add((src, dst))
        lines.append(f"  {src} -> {dst};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def run_dot(dot_path: Path, out_path: Path, fmt: str) -> None:
    exe = shutil.which("dot")
    if not exe:
        raise RuntimeError("graphviz `dot` not found; install graphviz")
    proc = subprocess.run(
        [exe, f"-T{fmt}", str(dot_path), "-o", str(out_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not out_path.is_file():
        raise RuntimeError(
            f"dot -T{fmt} failed for {dot_path.name}: {proc.stderr.strip()}"
        )


def write_assets(stem: str, dot_src: str) -> tuple[Path, Path, Path]:
    DEPS_DIR.mkdir(parents=True, exist_ok=True)
    dot_path = DEPS_DIR / f"{stem}.dot"
    svg_path = DEPS_DIR / f"{stem}.svg"
    pdf_path = DEPS_DIR / f"{stem}.pdf"
    png_path = DEPS_DIR / f"{stem}.png"
    dot_path.write_text(dot_src, encoding="utf-8")
    run_dot(dot_path, svg_path, "svg")
    run_dot(dot_path, pdf_path, "pdf")
    run_dot(dot_path, png_path, "png")
    return dot_path, svg_path, pdf_path


def figure_block(course: str, stem: str) -> str:
    caption = (
        f"Lean module dependencies for the {course} solution. "
        "Amber fill: Mathlib imports. Blue fill: this course's modules. "
        "Green fill: prior-course modules."
    )
    if stem not in PRIOR_MODULES:
        caption = (
            f"Lean module dependencies for the {course} solution. "
            "Amber fill: Mathlib imports. Blue fill: solution modules."
        )
    # Course notes live under ``courses/``; href is relative to that directory.
    rel = f"../figures/deps/{stem}.svg"
    return (
        "<!-- lean-dep-figure -->\n"
        f"<!-- figure-caption: {caption} -->\n"
        f"![{caption}]({rel})\n"
        "<!-- /lean-dep-figure -->\n"
    )


def insert_figure(text: str, block: str) -> str:
    """Place the dep figure under ``## Solution`` when present, else after the H1."""
    text = MARKER_RE.sub("", text)
    m = re.search(r"^## Solution\s*$", text, re.MULTILINE)
    if m:
        insert_at = m.end()
        rest = text[insert_at:].lstrip("\n")
        return text[:insert_at] + "\n\n" + block + "\n" + rest
    m = re.search(r"^# .+$", text, re.MULTILINE)
    if not m:
        raise RuntimeError("missing # title heading")
    insert_at = m.end()
    rest = text[insert_at:].lstrip("\n")
    return text[:insert_at] + "\n\n" + block + "\n" + rest


def main() -> None:
    for md, course, stem, seeds in COURSE_LEANS:
        rels = course_files(seeds)
        write_assets(stem, graph_for(rels, stem, PRIOR_MODULES.get(stem)))
        block = figure_block(course, stem)
        path = ROOT / "courses" / md
        path.write_text(
            insert_figure(path.read_text(encoding="utf-8"), block),
            encoding="utf-8",
        )
        print(f"updated {md} -> figures/deps/{stem}.{{dot,svg,pdf,png}}")


if __name__ == "__main__":
    main()
