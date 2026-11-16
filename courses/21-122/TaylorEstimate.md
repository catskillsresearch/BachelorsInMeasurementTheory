# Taylor series estimation at $x = 0.5$

$$\frac{(0.5)^3}{3} = \frac{1}{24} \approx 0.041667$$
   $$-\frac{(0.5)^5}{5} = -\frac{1}{160} = -0.006250$$
   $$\frac{5(0.5)^7}{42} = \frac{5}{5376} \approx 0.000930$$
   $$-\frac{5(0.5)^9}{54} = -\frac{5}{27648} \approx -0.000181$$
   Summing these gives:
   $$T_9(0.5) \approx 0.041667 - 0.006250 + 0.000930 - 0.000181 = 0.036166 \approx 0.0362.$$

**[BachelorsInMeasurementTheory/Course21120/TaylorEstimate.lean](../../BachelorsInMeasurementTheory/Course21120/TaylorEstimate.lean)**

@import "../../BachelorsInMeasurementTheory/Course21120/TaylorEstimate.lean"

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

## Explicit error bound

On $[0, 0.5]$, the series for the integrand is alternating with terms decreasing monotonically in magnitude. By the alternating series estimation theorem, the truncation error in the integrand is bounded by the magnitude of the next term:
   $$R_{integrand}(t) \le \left(1 - \frac{1}{6} + \frac{1}{120}\right) t^{10} = \frac{101}{120} t^{10}.$$
   Integrating yields:
   $$|R_f(0.5)| \le \int_0^{0.5} \frac{101}{120} t^{10}\,dt = \frac{101}{1320} (0.5)^{11} = \frac{101}{1320 \times 2048} \approx 3.73 \times 10^{-5} < 0.0001.$$
   Thus, to four decimal places:
   $$f(0.5) \approx 0.0362 \quad (\text{with error } < 4 \times 10^{-5}).$$

**[BachelorsInMeasurementTheory/Course21120/TaylorError.lean](../../BachelorsInMeasurementTheory/Course21120/TaylorError.lean)**

@import "../../BachelorsInMeasurementTheory/Course21120/TaylorError.lean"

**Lean formalization.** `productHigher` is the degree-$\ge 12$ tail in the extended product `sinTrunc10`·`geomTrunc8`. `Rintegrand` is the integrand truncation bound $(101/120)\,t^{10}$. `truncation_error` is `integrateMonomial (101/120) 10 (1/2)`, i.e. $\int_0^{1/2} R_{\mathrm{integrand}}$ in the formal monomial model.

**Theorem** (`t10_coeff_parts`). $1 - 1/6 + 1/120 = 101/120$.

**Proof.** `norm_num`.

**Theorem** (`product_sin10_geom8_eq`). For every $t$, `sinTrunc10 t`·`geomTrunc8 t` $=$ `gTrunc t` $+$ $(101/120)t^{10}$ $+$ `productHigher t`.

**Proof.** Expand all truncations and `ring`.

**Theorem** (`t10_term_from_series`). Isolating the degree-$8$ part and `productHigher` leaves $(101/120)t^{10}$.

**Proof.** Subtract the identity `product_sin10_geom8_eq` and cancel.

**Theorem** (`t10_term_english`). The same isolated $t^{10}$ term equals $(1-1/6+1/120)t^{10}$.

**Proof.** Rewrite with `t10_coeff_parts`.

**Theorem** (`Rintegrand_le_form`). `Rintegrand t` $=$ $(1-1/6+1/120)t^{10}$.

**Proof.** Unfold and apply `t10_coeff_parts`.

**Theorem** (`Rintegrand_eq_extracted`). `Rintegrand` equals the extracted $t^{10}$ difference from the extended product.

**Proof.** Use `t10_term_from_series` and symmetry of equality.

**Theorem** (`integrate_Rintegrand_coeff`). $(101/120)/11 = 101/1320$.

**Proof.** `norm_num`.

**Theorem** (`truncation_error_eq_integral`). `truncation_error` $=$ $(101/120)\cdot (1/2)^{11}/11$.

**Proof.** Unfold `truncation_error` and `integrateMonomial`; `ring`.

**Theorem** (`truncation_error_eq_note`). `truncation_error` $=$ $(101/1320)(1/2)^{11}$.

**Proof.** Factor the integrand using `integrate_Rintegrand_coeff`.

**Theorem** (`truncation_error_eq`). `truncation_error` $=$ $101/2703360$.

**Proof.** `norm_num` after `truncation_error_eq_note`.

**Theorem** (`truncation_error_lt`). `truncation_error` $< 10^{-4}$.

**Proof.** Evaluate with `truncation_error_eq` and `norm_num`.

## Summary of what Lean verifies here

1. **Term-by-term calculation**:
   - $x^3/3 = 1/24 \approx 0.041667$
   - $x^5/5 = 1/160 = 0.006250$
   - $5x^7/42 = 5/5376 \approx 0.000930$
   - $5x^9/54 = 5/27648 \approx 0.000181$
2. **Exact value**: $T_9(1/2) = \frac{34997}{967680} \approx 0.0361659$.
3. **Rounding**: Lean proves $0.03615 < T_9(1/2) < 0.03625$, confirming it rounds to **$0.0362$**.
4. **Error bound**: Lean proves the remainder bound $\frac{101}{2703360} \approx 3.74 \times 10^{-5} < 10^{-4}$.

**[BachelorsInMeasurementTheory/Course21120/Summary.lean](../../BachelorsInMeasurementTheory/Course21120/Summary.lean)**

@import "../../BachelorsInMeasurementTheory/Course21120/Summary.lean"

**Lean formalization.** Bundles the verified rational values at $x=1/2$, the four-decimal enclosure, and the remainder bound from `TaylorEstimate` and `TaylorError`.

**Theorem** (`summary_terms`). The four summands of `T9(1/2)` equal $1/24$, $1/160$, $5/5376$, and $5/27648$ respectively.

**Proof.** Product of `term1_eq`–`term4_eq`.

**Theorem** (`summary_exact`). `T9(1/2) = 34997/967680$.

**Proof.** Alias of `T9_half_exact`.

**Theorem** (`summary_rounding`). $0.03615 < T_9(1/2) < 0.03625$.

**Proof.** Alias of `T9_half_rounds_to_0_0362`.

**Theorem** (`summary_error`). `truncation_error = 101/2703360` and `truncation_error < 1/10000`.

**Proof.** Conjunction of `truncation_error_eq` and `truncation_error_lt`.
