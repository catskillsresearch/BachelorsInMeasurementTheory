## Introduction

### A role for AI in goal-directed college advising in mathematics

Imagine that a first-year student at Carnegie Mellon told their faculty advisor that their goal 
for their undergraduate degree was to be able to read a paper on Measurement Theory
written by Dana Scott in 1964 [@Scott64].  This report is an example of responsible answer to that question,
generated with help of large language models. It turns out to be a map of Scott's own
undergraduate training. It is a model of highly individually 
tailored automated advisement to ensure that the student will master the skills
needed to read the paper for understanding and be able, in turn, to reproduce and 
teach the ideas and proofs it contains to themselves and others.  This is a level 
of advising intended to augment and improve on typical standards of advice received
by undergraduates.  The selection of Scott's 1964 paper is not intended to recommend an actual degree
program in Measurement Theory, but to illustrate this unique AI-assisted advisement
tool.  The tool idea is not a criticism of current advisement practices, just a unique
way to augment it.

Measurement theory asks when qualitative comparisons can be represented by
real numbers. Scott's 1964 paper [@Scott64] organizes several such representation
questions around a finite theory of homogeneous linear inequalities, with
applications to intransitive indifference, ordered utility differences, and
subjective probability. The infinite direction, which Scott announced but
did not carry out, runs through the finite-cancellation setting of
Kraft--Pratt--Seidenberg [@Kraft59], Kelley's measures on Boolean algebras
[@Kelley59], Stone spaces, positive functionals, Hahn--Banach extension, and
Riesz representation.

The pedagogical claim of this report is that a complete undergraduate
mathematics major at Carnegie Mellon already contains the pieces of that
argument, if the courses are taken in the right order and each is asked to
do real work. The syllabus below is that ordering. It is framed as a
Bachelor of Science in Measurement Theory: not a new degree program, but a
reading of the existing catalog as a single connected proof.

For each course, we propose and solve, in mathematical English and in Lean, a hypothetical capstone problem which
exercises the key features of the course needed to read Scott [@Scott64] for understanding.
We highlight with diagrams exactly what features of Lean's Mathlib (and hence,
exactly what mathematics) need to be mastered to solve each capstone problem.

Each problem
is built so that quoting a theorem from a later course is not available: the
calculus problem uses the fundamental theorem, comparison, and Taylor
remainders; the linear-algebra problem speaks the dual-space language of
Scott's Theorem 1.1; the discrete-mathematics problem is the combinatorial
counting behind Theorems 1.2 and 3.2; and the independent-study problem
assembles set theory, topology, measure, and functional analysis into the
infinite extension of Theorem 4.1.

The formalizations live in the Lean library `BachelorsInMeasurementTheory`. Each
course snippet is a self-contained module. The root file
`BachelorsInMeasurementTheory.lean` imports all of them. The English arguments occupy the body of this report, in syllabus order,
with each Lean module inlined next to the claim it proves. The appendix
is an index of filenames, each linking to the source on GitHub.
