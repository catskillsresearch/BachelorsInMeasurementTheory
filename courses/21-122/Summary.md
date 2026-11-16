# Summary of what Lean verifies here

1. **Term-by-term calculation**:
   - $x^3/3 = 1/24 \approx 0.041667$
   - $x^5/5 = 1/160 = 0.006250$
   - $5x^7/42 = 5/5376 \approx 0.000930$
   - $5x^9/54 = 5/27648 \approx 0.000181$
2. **Exact value**: $T_9(1/2) = \frac{34997}{967680} \approx 0.0361659$.
3. **Rounding**: Lean proves $0.03615 < T_9(1/2) < 0.03625$, confirming it rounds to **$0.0362$**.
4. **Error bound**: Lean proves the remainder bound $\frac{101}{2703360} \approx 3.74 \times 10^{-5} < 10^{-4}$.

**[BachelorsInMeasurementTheory/Course21122/Summary.lean](../../BachelorsInMeasurementTheory/Course21122/Summary.lean)**

@import "../../BachelorsInMeasurementTheory/Course21122/Summary.lean"

**Lean formalization.** Bundles the verified rational values at $x=1/2$, the four-decimal enclosure, and the remainder bound from `TaylorEstimate` and `TaylorError`.

**Theorem** (`summary_terms`). The four summands of `T9(1/2)` equal $1/24$, $1/160$, $5/5376$, and $5/27648$ respectively.

**Proof.** Product of `term1_eq`–`term4_eq`.

**Theorem** (`summary_exact`). `T9(1/2) = 34997/967680$.

**Proof.** Alias of `T9_half_exact`.

**Theorem** (`summary_rounding`). $0.03615 < T_9(1/2) < 0.03625$.

**Proof.** Alias of `T9_half_rounds_to_0_0362`.

**Theorem** (`summary_error`). `truncation_error = 101/2703360` and `truncation_error < 1/10000`.

**Proof.** Conjunction of `truncation_error_eq` and `truncation_error_lt`.
