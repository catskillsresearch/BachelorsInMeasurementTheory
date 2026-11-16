# Problem

Let $f(x) = \int_0^x \frac{\sin(t^2)}{1+t^2}\,dt$.

(a) Determine whether $\lim_{x\to\infty} f(x)$ exists, and if so, bound it using comparison and integration by parts on the tail. 

(b) Find the Taylor series of $f$ about $x=0$ through the $x^9$ term, and use it to estimate $f(0.5)$ to four decimal places with an explicit error bound.

*Requires: limits/comparison tests, integration by parts, power series, Taylor remainder estimation.*

Prove it in English and then in Lean 4, using as much Mathlib as possible. No uses of sorry, admit or axiom are allowed. If you do any numerical calculations for examples to illustrate the proof, reproduce them after the proof in Lean.
