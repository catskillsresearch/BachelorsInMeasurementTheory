# Taylor series estimation at $x = 0.5$

$$\frac{(0.5)^3}{3} = \frac{1}{24} \approx 0.041667$$
   $$-\frac{(0.5)^5}{5} = -\frac{1}{160} = -0.006250$$
   $$\frac{5(0.5)^7}{42} = \frac{5}{5376} \approx 0.000930$$
   $$-\frac{5(0.5)^9}{54} = -\frac{5}{27648} \approx -0.000181$$
   Summing these gives:
   $$T_9(0.5) \approx 0.041667 - 0.006250 + 0.000930 - 0.000181 = 0.036166 \approx 0.0362.$$

**[BachelorsInMeasurementTheory/Course21122/TaylorEstimate.lean](../../BachelorsInMeasurementTheory/Course21122/TaylorEstimate.lean)**

@import "../../BachelorsInMeasurementTheory/Course21122/TaylorEstimate.lean"

**Lean formalization.** Specializes the rational Taylor polynomial `T9` at $x=1/2$ and certifies decimal rounding.

**Theorem** (`T9_at_half`). `T9(1/2)` matches the unfolded four-term sum at $1/2$ via `T9_simplified`.

**Proof.** Direct rewrite.

**Theorem** (`term1_eq`). $(1/2)^3/3 = 1/24$.

**Theorem** (`term2_eq`). $(1/2)^5/5 = 1/160$.

**Theorem** (`term3_eq`). $5(1/2)^7/42 = 5/5376$.

**Theorem** (`term4_eq`). $5(1/2)^9/54 = 5/27648$.

**Proof** (each term theorem). `norm_num`.

**Theorem** (`T9_half_eq`). `T9(1/2) = 1/24 - 1/160 + 5/5376 - 5/27648$.

**Proof.** Substitute the four `term*_eq` into `T9_at_half`.

**Theorem** (`T9_half_combined`). That sum equals $34997/967680$.

**Proof.** `norm_num` on the combined rational arithmetic.

**Theorem** (`T9_half_exact`). `T9(1/2) = 34997/967680$.

**Proof.** Chain `T9_half_eq` and `T9_half_combined`.

**Theorem** (`T9_half_rounds_to_0_0362`). $0.03615 < \texttt{T9}(1/2) < 0.03625$.

**Proof.** After rewriting to the four-term sum, `norm_num` proves both strict inequalities.

**Theorem** (`T9_half_close_to_0_0362`). Both $|T_9(1/2)-0.0362| < 0.00005$.

**Proof.** Same evaluation, `norm_num` on each side of $0.0362=362/10000$.
