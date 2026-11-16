# Existence of $\lim_{x\to\infty} f(x)$

For all $t \ge 0$, $|\sin(t^2)| \le 1$, so
   $$\left|\frac{\sin(t^2)}{1+t^2}\right| \le \frac{1}{1+t^2}.$$
   Since $\int_0^\infty \frac{dt}{1+t^2} = [\arctan(t)]_0^\infty = \frac{\pi}{2} < \infty$, the improper integral $\int_0^\infty \frac{\sin(t^2)}{1+t^2}\,dt$ is absolutely convergent. Hence, $\lim_{x\to\infty} f(x)$ exists.

**Lean formalization.** Absolute convergence of the Fresnel-type improper integral via domination by $1/(1+t^2)$, then passage to the limit of the indefinite integral as $x\to\infty$.

**Theorem** (`abs_integrand_le`). For every $t\in\mathbb{R}$, $\bigl|\sin(t^2)/(1+t^2)\bigr|\le 1/(1+t^2)$.

**Proof.** Write the absolute value as a quotient, use $1+t^2>0$, and bound the numerator by $|\sin(t^2)|\le 1$.

**Theorem** (`integrable_majorant`). The comparison majorant $t\mapsto 1/(1+t^2)$ is integrable on $\mathbb{R}$.

**Proof.** Reduce to Mathlib's `integrable_inv_one_add_sq`.

**Theorem** (`integrable_integrand`). The map $t\mapsto \sin(t^2)/(1+t^2)$ is integrable on $\mathbb{R}$.

**Proof.** Dominate by the majorant (`Integrable.mono'`), using continuity of the integrand for measurability and the pointwise bound `abs_integrand_le`.

**Theorem** (`integrableOn_integrand_Ioi`). The same integrand is integrable on $(0,\infty)$.

**Proof.** Restrict the global integrability statement to `Ioi 0`.

**Theorem** (`f_tendsto_integral_Ioi`). As $x\to\infty$, $f(x)=\int_0^x \sin(t^2)/(1+t^2)\,dt$ tends to $\int_{(0,\infty)}\sin(t^2)/(1+t^2)\,dt$.

**Proof.** Apply Mathlib's `intervalIntegral_tendsto_integral_Ioi` with the `Ioi 0` integrability statement and `tendsto_id`.

**Theorem** (`f_limit_exists`). There exists $L\in\mathbb{R}$ such that $f(x)\to L$ as $x\to\infty$.

**Proof.** Take $L$ to be the improper integral over $(0,\infty)$ and quote `f_tendsto_integral_Ioi`.

**[BachelorsInMeasurementTheory/Course21122/Existence.lean](../../BachelorsInMeasurementTheory/Course21122/Existence.lean)**

@import "../../BachelorsInMeasurementTheory/Course21122/Existence.lean"
