#!/usr/bin/env python3
"""Flatten the report note tree for the PDF build.

Walks TOC markdown links from ``BachelorsInMeasurementTheory.md`` (and nested
phase barrels), expands remaining ``@import`` directives, and writes
``report-expanded.md``.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB = "https://github.com/catskillsresearch/BachelorsInMeasurementTheory"

BARREL = ROOT / "BachelorsInMeasurementTheory.md"
EXPANDED = ROOT / "report-expanded.md"
IMPORT_RE = re.compile(
    r'^@import\s+"([^"]+)"(?:\s*\{([^}]*)\})?[ \t]*$',
    re.MULTILINE,
)
TOC_BULLET_RE = re.compile(
    r"^(?P<indent>[ \t]*)[-*][ \t]+\[(?P<title>.+?)\]\((?P<href>[^)]+\.md)\)[ \t]*$",
    re.MULTILINE,
)
YAML_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n+", re.DOTALL)

def library_lean_files() -> list[str]:
    files = ["BachelorsInMeasurementTheory.lean"]
    lib = ROOT / "BachelorsInMeasurementTheory"
    files.extend(sorted(p.relative_to(ROOT).as_posix() for p in lib.rglob("*.lean")))
    return files


LEAN_FILES = library_lean_files()

MODULE_DOC = re.compile(r"/-!\s*(.*?)\s*-/", re.DOTALL)
DECL_DOC = re.compile(r"/--\s*(.*?)\s*-/", re.DOTALL)


_ASCII_FROM_UNICODE = (
    ("ℝ", "R"),
    ("ℚ", "Q"),
    ("ℤ", "Z"),
    ("ℕ", "N"),
    ("ℵ", "aleph"),
    ("∫", "integral "),
    ("≤", "<="),
    ("≥", ">="),
    ("≠", "!="),
    ("∈", " in "),
    ("⊆", " subset "),
    ("∅", "empty"),
    ("⊥", "bottom"),
    ("⊤", "top"),
    ("∧", " and "),
    ("∨", " or "),
    ("¬", "not "),
    ("→", " -> "),
    ("↔", " <-> "),
    ("∀", "for all "),
    ("∃", "exists "),
    ("∞", "infinity"),
    ("α", "alpha"),
    ("ε", "epsilon"),
    ("φ", "phi"),
    ("Λ", "Lambda"),
    ("₀", "0"),
    ("₁", "1"),
    ("₂", "2"),
    ("₃", "3"),
    ("ˣ", "x"),
    ("²", "^2"),
    ("³", "^3"),
    ("⁴", "^4"),
    ("⁵", "^5"),
    ("—", "--"),
    ("–", "-"),
    ("‘", "'"),
    ("’", "'"),
    ("“", '"'),
    ("”", '"'),
    ("×", "x"),
)


def _ascii(text: str) -> str:
    for src, dst in _ASCII_FROM_UNICODE:
        text = text.replace(src, dst)
    text = re.sub(r"[^\x00-\x7f]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clip(text: str) -> str:
    text = _ascii(re.sub(r"\s+", " ", text.replace("`", "")).strip())
    if not text:
        return ""
    cut = len(text)
    for sep in (". ", "; "):
        idx = text.find(sep)
        if 20 <= idx < cut:
            cut = idx
    sentence = text[:cut].rstrip(" .;:")
    if len(sentence) > 140:
        sentence = sentence[:137].rsplit(" ", 1)[0] + "..."
    return sentence


def _one_line(text: str) -> str:
    """Prefer the first heading or sentence, not the whole module comment."""
    for raw in text.splitlines():
        line = re.sub(r"^#+\s*", "", raw.strip())
        if line:
            return _clip(line)
    return _clip(text)


def _looks_like_identifier(text: str) -> bool:
    return bool(text) and " " not in text and text.isalnum()


# Path-keyed first, then basename. Used when module comments are headings or fragments.
FILE_BLURBS: dict[str, str] = {
    "BachelorsInMeasurementTheory/Course21120/FTC.lean":
        "Fundamental theorem of calculus for the Fresnel-type integrand.",
    "BachelorsInMeasurementTheory/Course21120/Existence.lean":
        "Comparison bound that gives absolute convergence of the improper integral.",
    "BachelorsInMeasurementTheory/Course21122/TailBound.lean":
        "Arctan comparison bound for the tail integral.",
    "BachelorsInMeasurementTheory/Course21122/TaylorExpansion.lean":
        "Degree-9 Taylor polynomial of the integrated expansion.",
    "BachelorsInMeasurementTheory/Course21122/TaylorEstimate.lean":
        "Exact value and four-decimal rounding of T9 at 1/2.",
    "BachelorsInMeasurementTheory/Course21122/TaylorError.lean":
        "Alternating-series tail bound for the degree-9 truncation.",
    "BachelorsInMeasurementTheory/Course21122/Summary.lean":
        "Summary of the four Lean checks for the degree-9 estimate.",
    "BachelorsInMeasurementTheory/Course21241/PrimalBasis.lean":
        "Standard primal basis of three-space: spanning and independence.",
    "BachelorsInMeasurementTheory/Course21241/DualBasis.lean":
        "Dual basis functionals and the dual expansion of a linear map.",
    "BachelorsInMeasurementTheory/Course21228/ValidPair.lean":
        "Permutation pairs that make two sequences agree termwise.",
    "BachelorsInMeasurementTheory/Course21228/Genericity.lean":
        "Pairwise distinctness and multiset compatibility of two sequences.",
    "BachelorsInMeasurementTheory/Course21355/Completeness.lean":
        "Least-upper-bound property of the reals.",
    "BachelorsInMeasurementTheory/Course21355/MonotoneConvergence.lean":
        "Monotone convergence for bounded real sequences.",
    "BachelorsInMeasurementTheory/Course21355/PeakPoints.lean":
        "Peak-point construction of a monotonic subsequence.",
    "BachelorsInMeasurementTheory/Course21292/StrongDuality.lean":
        "Strong duality in certificate form from weak duality.",
    "BachelorsInMeasurementTheory/Course21292/ScottInstance.lean":
        "The concrete 3x3 Scott-type linear program.",
    "BachelorsInMeasurementTheory/Course21292/DualFormulation.lean":
        "Dual objective and dual constraints of the 3x3 instance.",
    "BachelorsInMeasurementTheory/Course21292/Simplex.lean":
        "Optimal primal and dual vertices of the 3x3 instance.",
    "BachelorsInMeasurementTheory/Course21292/Scott11.lean":
        "Scott's Theorem 1.1 from primal feasibility versus a dual witness.",
    "BachelorsInMeasurementTheory/Course21720/Riesz.lean":
        "Comparison and boundedness used by the Riesz representation.",
    "BachelorsInMeasurementTheory/Course21640/PreciseStatement.lean":
        "Precise statement of Hahn-Banach dominated extension.",
    "BachelorsInMeasurementTheory/Course21640/RoleOfSublinear.lean":
        "One-step bounds that make the sublinear functional usable.",
    "BachelorsInMeasurementTheory/Course21640/NormSublinear.lean":
        "The sublinear functional p(f) = C ||f||.",
    "BachelorsInMeasurementTheory/Course21640/Dominance.lean":
        "Dominance of a positive functional by the norm bound on a subspace.",
    "BachelorsInMeasurementTheory/Course21640/ApplyHahnBanach.lean":
        "Application of dominated extension to the norm bound.",
    "BachelorsInMeasurementTheory/Course21640/PositiveExtension.lean":
        "A dominated extension that fixes the unit is positive.",
    "BachelorsInMeasurementTheory/Course21640/Scott41.lean":
        "Restriction of the positive extension recovers the original assignment.",
    "BachelorsInMeasurementTheory/Course21410/StoneSpace.lean":
        "Stone space of a Boolean algebra and its basic clopens.",
    "BachelorsInMeasurementTheory/Course21410/StepFunctions.lean":
        "Stone indicators, the nonnegative cone, and preference differences.",
    "BachelorsInMeasurementTheory/Course21410/PositiveExtension.lean":
        "Positivity and preference agreement for a Stone-space functional.",
    "BachelorsInMeasurementTheory/Course21410/RestrictToB.lean":
        "Restriction of a Stone-space functional back to B.",
    "BachelorsInMeasurementTheory/Course21410/Representation.lean":
        "The restricted functional is a monotone assignment on B.",
    "BachelorsInMeasurementTheory/Course21410/Formalization.lean":
        "Umbrella importer for the infinite-algebra extension modules.",
    "BachelorsInMeasurementTheory/Course21241/PointV.lean":
        "A concrete point v outside the non-negative orthant.",
    "BachelorsInMeasurementTheory/Course21241/SeparatingU.lean":
        "The standard-basis separating vector u = e_0.",
    "BachelorsInMeasurementTheory/Course21241/DotAtV.lean":
        "Inner product of the separator with v.",
    "BachelorsInMeasurementTheory/Course21241/DotOnC.lean":
        "Inner product of the separator on the orthant.",
    "BachelorsInMeasurementTheory/Course21241/PhiSeparates.lean":
        "The linear functional associated to u separates v from C.",
    "BachelorsInMeasurementTheory/Course21355/TailExtremes.lean":
        "Tail supremum and tail infimum, and their monotonicity.",
    "BachelorsInMeasurementTheory/Course21355/LimsupLiminfExist.lean":
        "Existence of limsup and liminf for a bounded real sequence.",
    "BachelorsInMeasurementTheory/Course21355/AltSeqValues.lean":
        "Even and odd values of the sequence (-1)^n.",
    "BachelorsInMeasurementTheory/Course21355/AltSeqDiverges.lean":
        "Epsilon-argument that the alternating sequence diverges.",
    "BachelorsInMeasurementTheory/Course21228/SmallN2.lean":
        "Exact pair count for n = 2.",
    "BachelorsInMeasurementTheory/Course21228/SmallN3.lean":
        "Exact pair count for n = 3.",
    "BachelorsInMeasurementTheory/Course21640/Positivity.lean":
        "A norm-dominated linear functional is positive.",
    "BachelorsInMeasurementTheory/Course21127/NonzeroDenomInt.lean":
        "Integers with a nonzero denominator: the domain of the fraction relation.",
    "BachelorsInMeasurementTheory/Course21127/ToRat.lean":
        "The explicit map from a pair (a, b) to the rationals, and the induced bijection.",
    "BachelorsInMeasurementTheory/Course21127/WellOrder.lean":
        "Well-ordered subsets of Q, and a refutation of the claimed well-order of the positives.",
    "BachelorsInMeasurementTheory/Course21228/Counting.lean":
        "Count of permutation pairs that make two sequences agree termwise.",
    "BachelorsInMeasurementTheory/Course21228/SmallN.lean":
        "Exact pair counts for n = 2 and n = 3.",
    "BachelorsInMeasurementTheory/Course21228/Symmetric.lean":
        "Symmetric conditions on length-n sequences and permutation invariance of sums.",
    "BachelorsInMeasurementTheory/Course21241/Basis.lean":
        "Standard primal basis of three-space and the dual basis functionals.",
    "BachelorsInMeasurementTheory/Course21241/DualCone.lean":
        "The dual cone of the non-negative orthant.",
    "BachelorsInMeasurementTheory/Course21241/Numerical.lean":
        "Concrete separating functional for a point outside the orthant.",
    "BachelorsInMeasurementTheory/Course21241/Separation.lean":
        "Euclidean inner product, Riesz identification, and a separating vector.",
    "BachelorsInMeasurementTheory/Course21241/Space.lean":
        "The non-negative orthant cone in three-space.",
    "BachelorsInMeasurementTheory/Course21292/Instance.lean":
        "A concrete 3x3 Scott-type linear program.",
    "BachelorsInMeasurementTheory/Course21292/LinearProgram.lean":
        "Inequality-form linear programs over the rationals.",
    "BachelorsInMeasurementTheory/Course21292/WeakDuality.lean":
        "Weak duality for a primal/dual linear program.",
    "BachelorsInMeasurementTheory/Course21292/Numerical.lean":
        "Numerical checks of the four calculations in the 21-292 example.",
    "BachelorsInMeasurementTheory/Course21321/Kraft.lean":
        "Kraft difference vectors as a ScottPair with a cancellation witness.",
    "BachelorsInMeasurementTheory/Course21321/ScottPair.lean":
        "Scott pairs, separating functionals, and the cancellation-witness class.",
    "BachelorsInMeasurementTheory/Course21321/Theorem11.lean":
        "Scott's Theorem 1.1: a separable pair satisfies real non-cancellation.",
    "BachelorsInMeasurementTheory/Course21321/Theorem12.lean":
        "Scott's Theorem 1.2: rational separability implies combinatorial non-cancellation.",
    "BachelorsInMeasurementTheory/Course21321/Theorem13.lean":
        "Scott's Theorem 1.3 (one direction): rational non-cancellation implies real non-cancellation.",
    "BachelorsInMeasurementTheory/Course21322/AtomIso.lean":
        "Canonical bijection between atoms and the Stone space of a finite algebra.",
    "BachelorsInMeasurementTheory/Course21322/Hom.lean":
        "Boolean homomorphisms from a power set into Bool, and principal evaluations.",
    "BachelorsInMeasurementTheory/Course21322/MeasureCollapse.lean":
        "Collapse of Stone-space measure evaluation to the discrete atomic measure.",
    "BachelorsInMeasurementTheory/Course21322/Numerical.lean":
        "Direct calculation of the atomic measure on {0, 2}.",
    "BachelorsInMeasurementTheory/Course21322/StoneClopen.lean":
        "The Stone clopen associated with an element and preservation of membership.",
    "BachelorsInMeasurementTheory/Course21329/Cardinality.lean":
        "Cardinal-arithmetic argument that the Stone space is large.",
    "BachelorsInMeasurementTheory/Course21329/Filter.lean":
        "Filters, proper filters, and ultrafilters on a bounded lattice.",
    "BachelorsInMeasurementTheory/Course21329/StoneNonempty.lean":
        "The principal filter generated by top, and non-emptiness of the Stone space.",
    "BachelorsInMeasurementTheory/Course21329/UltrafilterExtension.lean":
        "Ultrafilter extension: a chain of proper filters unions to a proper filter.",
    "BachelorsInMeasurementTheory/Course21355/AltSeq.lean":
        "The alternating sequence of plus and minus one, and an epsilon-argument that it diverges.",
    "BachelorsInMeasurementTheory/Course21355/BolzanoWeierstrass.lean":
        "Bolzano-Weierstrass: a bounded real sequence has a convergent subsequence.",
    "BachelorsInMeasurementTheory/Course21355/CompactIcc.lean":
        "Closed bounded intervals in R are compact.",
    "BachelorsInMeasurementTheory/Course21355/LimsupLiminf.lean":
        "Tail supremum and tail infimum of a real sequence.",
    "BachelorsInMeasurementTheory/Course21355/Numerical.lean":
        "Computable alternating sequence used to inspect the example of (c).",
    "BachelorsInMeasurementTheory/Course21373/AtomJoin.lean":
        "Join and disjointness properties of Boolean atoms.",
    "BachelorsInMeasurementTheory/Course21373/BooleanAction.lean":
        "Boolean automorphisms and atoms of the fixed-point subalgebra.",
    "BachelorsInMeasurementTheory/Course21373/IsBooleanAtom.lean":
        "Atoms in a Boolean algebra.",
    "BachelorsInMeasurementTheory/Course21373/Representation.lean":
        "Canonical representation of an element as the join of the atoms below it.",
    "BachelorsInMeasurementTheory/Course21373/Numerical.lean":
        "Numerical example for the finite Boolean-algebra representation.",
    "BachelorsInMeasurementTheory/Course21410/Glue.lean":
        "Glue lemmas: inclusion-exclusion, monotonicity, and preference preservation.",
    "BachelorsInMeasurementTheory/Course21410/Measure.lean":
        "Finitely additive probability measures on a finite space.",
    "BachelorsInMeasurementTheory/Course21640/Numerical.lean":
        "Sup-norm example of a sublinear functional and a dominated extension on the plane.",
    "BachelorsInMeasurementTheory/Course21640/Sublinear.lean":
        "Sublinear functionals and dominated linear extensions.",
    "BachelorsInMeasurementTheory/Course21651/BooleanHom.lean":
        "Boolean algebra homomorphisms from B to Bool.",
    "BachelorsInMeasurementTheory/Course21651/ClosedEmbedding.lean":
        "The Stone space as an intersection of closed equalizer sets in B -> Bool.",
    "BachelorsInMeasurementTheory/Course21651/Separation.lean":
        "Separation properties used by the Stone embedding argument.",
    "BachelorsInMeasurementTheory/Course21651/StoneMap.lean":
        "The Stone clopen associated with an element of B.",
    "BachelorsInMeasurementTheory/Course21651/TwoAlgebra.lean":
        "Stone space of the four-element Boolean algebra on Fin 2.",
    "BachelorsInMeasurementTheory/Course21720/Boundedness.lean":
        "Positive linear functionals on C(X, R) are bounded.",
    "BachelorsInMeasurementTheory/Course21720/Numerical.lean":
        "The concrete functional Lambda(f) = 3 f(0) + 2 f(1).",
    "BachelorsInMeasurementTheory/Course21720/StoneMeasure.lean":
        "Finitely additive measures on a Boolean algebra from a positive functional.",
    "Numerical.lean": "Numerical checks reproducing the English example.",
}


def is_import_only(code: str) -> bool:
    lines = [
        ln.strip()
        for ln in code.splitlines()
        if ln.strip() and not ln.strip().startswith("--")
    ]
    return bool(lines) and all(ln.startswith("import ") for ln in lines)


def describe_lean(rel: str) -> str:
    """One-line English for the appendix index; sources stay inlined in the notes."""
    if rel == "BachelorsInMeasurementTheory.lean":
        return "Root importer for the library."
    code = (ROOT / rel).read_text(encoding="utf-8")
    if is_import_only(code):
        stem = Path(rel).stem
        m = re.fullmatch(r"Course(\d{5})", stem)
        if m:
            num = m.group(1)
            return f"Umbrella importer for the 21-{num[2:]} modules."
        if stem.startswith("Course"):
            return f"Umbrella importer for the {stem} modules."
        return "Umbrella importer for this course."
    for key in (rel, Path(rel).name):
        if key in FILE_BLURBS:
            return _ascii(FILE_BLURBS[key])
    m = MODULE_DOC.search(code)
    if m:
        desc = _one_line(m.group(1))
        if desc and not _looks_like_identifier(desc):
            return desc
    m = DECL_DOC.search(code)
    if m:
        desc = _one_line(m.group(1))
        if desc and not _looks_like_identifier(desc):
            return desc
    return Path(rel).stem


def demote_headings(text: str, n: int = 2) -> str:
    def repl(match: re.Match[str]) -> str:
        hashes = match.group(1)
        rest = match.group(2)
        level = min(len(hashes) + n, 6)
        return "#" * level + rest

    return re.sub(r"^(#{1,6})([ \t].*)$", repl, text, flags=re.MULTILINE)


GEMINI_LINE = re.compile(r"^\*\*Gemini[^*]*\*\*\.?[^\n]*$", re.MULTILINE)
LEAN_IMPORT_RE = re.compile(
    r'^@import\s+"([^"]+\.lean)"(?:\s*\{[^}]*\})?[ \t]*$',
    re.MULTILINE,
)


def expand_lean_imports(text: str, base: Path) -> str:
    """Expand nowakowska-style ``@import "….lean"`` into fenced source for the PDF."""

    def repl(match: re.Match[str]) -> str:
        path = (base / match.group(1)).resolve()
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise FileNotFoundError(
                f"lean import escapes the repository: {match.group(1)}"
            ) from exc
        if not path.is_file():
            raise FileNotFoundError(f"lean import missing: {rel}")
        code = path.read_text(encoding="utf-8").rstrip()
        # Keep a lean-path marker for build_tex title extraction; the clickable
        # ``**[path](…)`` line already sits above the @import in the source.
        return f"<!-- lean: {rel} -->\n\n```lean\n{code}\n```\n"

    return LEAN_IMPORT_RE.sub(repl, text)


def rewrite_lean_links(text: str, base: Path) -> str:
    text = re.sub(r"^\[← Syllabus\]\([^)]+\)\s*\n+", "", text)
    text = GEMINI_LINE.sub("", text)
    text = expand_lean_imports(text, base)
    return text


def ensure_blank_before_headings(text: str) -> str:
    return re.sub(r"(?<!\n)\n(#{1,6}[ \t])", r"\n\n\1", text)


def flatten_deep_headings(text: str) -> str:
    """Course `####` steps become level-5 subparagraphs (3.1.2.b.1).
    Nothing at that depth is flattened anymore."""
    return text


def strip_horizontal_rules(text: str) -> str:
    return re.sub(r"^---\s*$", "", text, flags=re.MULTILINE)


def strip_part_letters(text: str) -> str:
    """Drop leading (a)/(b)/(c) from headings; the PDF numbers those levels
    as 3.1.2.a, so the letter in the title is redundant."""
    return re.sub(r"^(#{1,6}[ \t]+)\([a-z]\)[ \t]+", r"\1", text, flags=re.MULTILINE)


def prepare_course(text: str, course_path: Path) -> str:
    text = rewrite_lean_links(text, course_path.parent)
    # Course notes use ``../`` for Lean sources and dep figures; the flattened
    # report lives at the repo root.
    text = re.sub(
        r"\((?:\.\./)+(BachelorsInMeasurementTheory/[^)]+\.lean)\)",
        r"(\1)",
        text,
    )
    text = re.sub(
        r"\((?:\.\./)+(figures/deps/[^)]+)\)",
        r"(\1)",
        text,
    )
    text = strip_horizontal_rules(text)
    text = demote_headings(text, 2)
    text = flatten_deep_headings(text)
    text = strip_part_letters(text)
    text = ensure_blank_before_headings(text)
    return text.strip() + "\n"


def load_note(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return YAML_FRONTMATTER_RE.sub("", text, count=1)


def expand_svg_import(path: Path, opts: str) -> str:
    """Turn an SVG ``@import`` into a markdown image (prefer sibling ``.dot`` → PDF)."""
    import hashlib
    import shutil
    import subprocess

    caption = path.stem
    if opts:
        cm = re.search(r'caption\s*=\s*"([^"]+)"', opts) or re.search(
            r"caption\s*=\s*'([^']+)'", opts
        )
        if cm:
            caption = cm.group(1).strip()

    figures = ROOT / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(path.read_bytes()).hexdigest()[:10]
    try:
        stem = path.relative_to(ROOT).as_posix().replace("/", "-")
    except ValueError:
        stem = path.stem
    if stem.lower().endswith(".svg"):
        stem = stem[:-4]

    dot_src = path.with_suffix(".dot")
    pdf = figures / f"{stem}-{digest}.pdf"
    if dot_src.is_file() and shutil.which("dot"):
        if not pdf.is_file():
            proc = subprocess.run(
                ["dot", "-Tpdf", str(dot_src), "-o", str(pdf)],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode != 0 or not pdf.is_file():
                raise RuntimeError(f"dot→PDF failed for {path.name}")
        return f"\n\n![{caption}]({pdf.relative_to(ROOT).as_posix()})\n\n"

    rel = path.relative_to(ROOT).as_posix()
    return f"\n\n![{caption}]({rel})\n\n"


def is_top_course(rel: str) -> bool:
    """``courses/21-122.md`` is a top course; ``courses/21-122/Problem.md`` is not."""
    parts = Path(rel).parts
    return len(parts) == 2 and parts[0] == "courses" and parts[1].endswith(".md")


def expand_imports(text: str, base: Path, stack: tuple[str, ...] = ()) -> str:
    """Resolve `@import` paths from the importing file, as Markdown Preview Enhanced does."""

    def repl(match: re.Match[str]) -> str:
        path = (base / match.group(1)).resolve()
        opts = match.group(2) or ""
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise FileNotFoundError(f"import escapes the repository: {match.group(1)}") from exc
        if rel in stack:
            raise RuntimeError(f"import cycle: {' -> '.join(stack + (rel,))}")
        if not path.is_file():
            raise FileNotFoundError(f"import missing: {rel}")
        if path.suffix.lower() == ".svg":
            return expand_svg_import(path, opts)
        if path.suffix.lower() == ".lean":
            code = path.read_text(encoding="utf-8").rstrip()
            return f"<!-- lean: {rel} -->\n\n```lean\n{code}\n```\n\n"
        chunk = load_note(path)
        if is_top_course(rel):
            chunk = expand_note(chunk, path, stack + (rel,))
            chunk = prepare_course(chunk, path)
        elif rel.startswith("courses/"):
            # Nested course-barrel section: expand, but demote once at the top course.
            chunk = expand_note(chunk, path, stack + (rel,))
        else:
            chunk = expand_note(chunk, path, stack + (rel,))
        return chunk.strip() + "\n\n"

    return IMPORT_RE.sub(repl, text)


def expand_toc_links(text: str, base: Path, stack: tuple[str, ...] = ()) -> str:
    """Inline TOC bullet links (nowakowska-style barrels), leaving non-TOC links alone."""

    def repl(match: re.Match[str]) -> str:
        href = match.group("href")
        path = (base / href).resolve()
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise FileNotFoundError(f"TOC link escapes the repository: {href}") from exc
        if rel in stack:
            raise RuntimeError(f"import cycle: {' -> '.join(stack + (rel,))}")
        if not path.is_file():
            raise FileNotFoundError(f"TOC link missing: {rel}")
        chunk = load_note(path)
        if is_top_course(rel):
            chunk = expand_note(chunk, path, stack + (rel,))
            chunk = prepare_course(chunk, path)
        elif rel.startswith("courses/"):
            chunk = expand_note(chunk, path, stack + (rel,))
        else:
            chunk = expand_note(chunk, path, stack + (rel,))
        return chunk.strip() + "\n\n"

    return TOC_BULLET_RE.sub(repl, text)


def expand_note(text: str, path: Path, stack: tuple[str, ...] = ()) -> str:
    """Expand TOC links then `@import`s for one note."""
    text = expand_toc_links(text, path.parent, stack)
    text = expand_imports(text, path.parent, stack)
    return text


def main() -> None:
    if not BARREL.is_file():
        raise SystemExit(f"error: missing {BARREL}")
    expanded = expand_note(load_note(BARREL), BARREL)
    parts = [expanded.rstrip(), "\n\n", "## Lean module index\n\n"]
    parts.append(
        f"Checked by `lake build`. Each module is inlined next to the English "
        f"it proves. This appendix lists the files only; the sources live at "
        f"[{GITHUB}]({GITHUB}).\n\n"
    )
    parts.append("| File | Contents |\n| --- | --- |\n")
    for rel in LEAN_FILES:
        link = f"[`{rel}`]({GITHUB}/blob/main/{rel})"
        parts.append(f"| {link} | {describe_lean(rel)} |\n")
    parts.append("\n")

    total_lines = sum(
        len((ROOT / rel).read_text(encoding="utf-8").splitlines()) for rel in LEAN_FILES
    )
    parts.append(f"**Total:** {len(LEAN_FILES)} modules, {total_lines} lines.\n")

    EXPANDED.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {EXPANDED.name} ({total_lines} Lean lines across {len(LEAN_FILES)} files)")


if __name__ == "__main__":
    main()
