# Explicit error bound

On $[0, 0.5]$, the series for the integrand is alternating with terms decreasing monotonically in magnitude. By the alternating series estimation theorem, the truncation error in the integrand is bounded by the magnitude of the next term:
   $$R_{integrand}(t) \le \left(1 - \frac{1}{6} + \frac{1}{120}\right) t^{10} = \frac{101}{120} t^{10}.$$
   Integrating yields:
   $$|R_f(0.5)| \le \int_0^{0.5} \frac{101}{120} t^{10}\,dt = \frac{101}{1320} (0.5)^{11} = \frac{101}{1320 \times 2048} \approx 3.73 \times 10^{-5} < 0.0001.$$
   Thus, to four decimal places:
   $$f(0.5) \approx 0.0362 \quad (\text{with error } < 4 \times 10^{-5}).$$

**[BachelorsInMeasurementTheory/Course21122/TaylorError.lean](../../BachelorsInMeasurementTheory/Course21122/TaylorError.lean)**

@import "../../BachelorsInMeasurementTheory/Course21122/TaylorError.lean"

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
