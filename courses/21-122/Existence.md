# Existence of $\lim_{x\to\infty} f(x)$

For all $t \ge 0$, $|\sin(t^2)| \le 1$, so
   $$\left|\frac{\sin(t^2)}{1+t^2}\right| \le \frac{1}{1+t^2}.$$
   Since $\int_0^\infty \frac{dt}{1+t^2} = [\arctan(t)]_0^\infty = \frac{\pi}{2} < \infty$, the improper integral $\int_0^\infty \frac{\sin(t^2)}{1+t^2}\,dt$ is absolutely convergent. Hence, $\lim_{x\to\infty} f(x)$ exists.

**Lean formalization.** Pointwise domination of the integrand by the comparison majorant $1/(1+t^2)$, used to justify absolute convergence of $\int_0^\infty \sin(t^2)/(1+t^2)\,dt$.

**Theorem** (`abs_integrand_le`). For every $t\in\mathbb{R}$, $\bigl|\sin(t^2)/(1+t^2)\bigr|\le 1/(1+t^2)$.

**Proof.** Write the absolute value as a quotient, use $1+t^2>0$, and bound the numerator by $|\sin(t^2)|\le 1$.

**[BachelorsInMeasurementTheory/Course21120/Existence.lean](../../BachelorsInMeasurementTheory/Course21120/Existence.lean)**

@import "../../BachelorsInMeasurementTheory/Course21120/Existence.lean"
