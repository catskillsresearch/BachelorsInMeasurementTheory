# Tail bound via integration by parts

For any cutoff $M > 0$, decompose the limit into:
   $$\lim_{x\to\infty} f(x) = \int_0^M \frac{\sin(t^2)}{1+t^2}\,dt + \int_M^\infty \frac{\sin(t^2)}{1+t^2}\,dt.$$
   On the tail, rewrite $\sin(t^2)\,dt = \frac{1}{2t}\,d(-\cos(t^2))$. Integrating by parts with $u = \frac{1}{2t(1+t^2)}$ and $dv = 2t\sin(t^2)\,dt$:
   $$\int_M^\infty \frac{\sin(t^2)}{1+t^2}\,dt = \left[ -\frac{\cos(t^2)}{2t(1+t^2)} \right]_M^\infty - \int_M^\infty (-\cos(t^2)) \left( -\frac{1+3t^2}{2t^2(1+t^2)^2} \right) dt$$
   $$= \frac{\cos(M^2)}{2M(1+M^2)} - \int_M^\infty \cos(t^2) \frac{1+3t^2}{2t^2(1+t^2)^2}\,dt.$$
   Since $|\cos(t^2)| \le 1$ and $\frac{1+3t^2}{2t^2(1+t^2)^2} = -\frac{d}{dt}\left(\frac{1}{2t(1+t^2)}\right) > 0$:
   $$\left| \int_M^\infty \frac{\sin(t^2)}{1+t^2}\,dt \right| \le \frac{1}{2M(1+M^2)} + \int_M^\infty \left(-\frac{d}{dt} \frac{1}{2t(1+t^2)}\right) dt = \frac{1}{M(1+M^2)}.$$
   Combining with the comparison bound on $[0, M]$:
   $$\left| \lim_{x\to\infty} f(x) \right| \le \arctan(M) + \frac{1}{M(1+M^2)}.$$
   For example, setting $M = 1$ yields $|f(\infty)| \le \frac{\pi}{4} + \frac{1}{2} \approx 1.2854$.

**Lean formalization.** The integration-by-parts weight is $u(t)=\texttt{ibpWeight}\,t = 1/(2t(1+t^2))$; its positive density is $\texttt{ibpDensity}\,t = (1+3t^2)/(2t^2(1+t^2)^2)$, satisfying $u'(t)=-\texttt{ibpDensity}(t)$. The combined cutoff bound is $\texttt{limAbsBound}(M)=\arctan M + 1/(M(1+M^2))$.

**Theorem** (`majorant_integral`). For all $M,x\in\mathbb{R}$, $\int_M^x (1+t^2)^{-1}\,dt = \arctan x - \arctan M$.

**Proof.** Rewrite as integral of $(1+t^2)^{-1}$ and apply Mathlib's `integral_inv_one_add_sq`.

**Theorem** (`continuous_majorant`). The map $t\mapsto (1+t^2)^{-1}$ is continuous on $\mathbb{R}$.

**Proof.** Constant divided by a nowhere-vanishing continuous quadratic (`positivity` on the denominator).

**Theorem** (`abs_integral_le_arctan`). If $M\ge 0$, then $\bigl|\int_0^M \sin(t^2)/(1+t^2)\,dt\bigr|\le \arctan M$.

**Proof.** Dominate by the pointwise inequality `abs_integrand_le`, then integrate the majorant on $[0,M]$ and evaluate at $0$ to get $\arctan M$.

**Theorem** (`tail_mass_le`). If $M\le x$, then $\arctan x - \arctan M \le \pi/2 - \arctan M$.

**Proof.** Use $\arctan x < \pi/2$ and `nlinarith`.

**Lemma** (`den_deriv`). For every $t$, the map $s\mapsto 2s(1+s^2)$ has derivative $2+6t^2$ at $s=t$.

**Proof.** Product rule on $2s$ and $1+s^2$, then simplify by `ring`.

**Theorem** (`hasDerivAt_ibpWeight`). If $t>0$, then $\texttt{ibpWeight}$ has derivative $-\texttt{ibpDensity}(t)$ at $t$.

**Proof.** Recognize `ibpWeight` as the reciprocal of $2t(1+t^2)$, differentiate via `den_deriv` and `field_simp`/`ring`.

**Theorem** (`ibpDensity_nonneg`). If $t>0$, then $\texttt{ibpDensity}(t)\ge 0$.

**Proof.** `positivity` on the unfolded rational expression.

**Theorem** (`ibpWeight_pos`). If $t>0$, then $\texttt{ibpWeight}(t)>0$.

**Proof.** `positivity` on $1/(2t(1+t^2))$.

**Theorem** (`two_ibpWeight`). If $t\neq 0$, then $2\,\texttt{ibpWeight}(t)=1/(t(1+t^2))$.

**Proof.** Unfold `ibpWeight` and `field_simp`.

**Theorem** (`continuousOn_ibpDensity`). If $0<M\le X$, then $\texttt{ibpDensity}$ is continuous on $[M,X]$.

**Proof.** Rational function with denominator positive on that interval (`positivity` at each point in the `uIcc`).

**Theorem** (`ibpDensity_integral`). If $0<M\le X$, then $\int_M^X \texttt{ibpDensity}(t)\,dt = \texttt{ibpWeight}(M)-\texttt{ibpWeight}(X)`.

**Proof.** FTC interval: $u'=-\texttt{ibpDensity}$ on $(M,X)$ from `hasDerivAt_ibpWeight`, flip a sign in the integral, and recognize the endpoint difference.

**Theorem** (`ibp_tail_mass_le`). If $0<M\le X$, then $\texttt{ibpWeight}(M)+\int_M^X \texttt{ibpDensity} \le 2\,\texttt{ibpWeight}(M)$.

**Proof.** Substitute `ibpDensity_integral` and use $\texttt{ibpWeight}(X)\ge 0$.

**Theorem** (`ibp_tail_bound`). If $0<M\le X$, then $\texttt{ibpWeight}(M)+\int_M^X \texttt{ibpDensity} \le 1/(M(1+M^2))$.

**Proof.** Chain `ibp_tail_mass_le` with `two_ibpWeight`.

**Theorem** (`limAbsBound_eq`). If $M>0$, then $\texttt{limAbsBound}(M)=\arctan M + 2\,\texttt{ibpWeight}(M)`.

**Proof.** Unfold `limAbsBound` and rewrite $1/(M(1+M^2))$ via `two_ibpWeight`.

**Theorem** (`limAbsBound_ge_pieces`). If $0<M\le X$, then
$\bigl|\int_0^M \sin(t^2)/(1+t^2)\,dt\bigr| + \bigl(\texttt{ibpWeight}(M)+\int_M^X \texttt{ibpDensity}\bigr) \le \texttt{limAbsBound}(M)$.

**Proof.** Add `abs_integral_le_arctan` and `ibp_tail_bound`, matching the definition of `limAbsBound`.

**Theorem** (`limAbsBound_one`). $\texttt{limAbsBound}(1)=\pi/4+1/2$.

**Proof.** `arctan_one` and `norm_num` on the tail term.

**Theorem** (`limAbsBound_one_lt`). $\texttt{limAbsBound}(1) < 1.2854$.

**Proof.** Rewrite with `limAbsBound_one`, bound $\pi$ by a rational, and close with `nlinarith`.

**[BachelorsInMeasurementTheory/Course21122/TailBound.lean](../../BachelorsInMeasurementTheory/Course21122/TailBound.lean)**

@import "../../BachelorsInMeasurementTheory/Course21122/TailBound.lean"
