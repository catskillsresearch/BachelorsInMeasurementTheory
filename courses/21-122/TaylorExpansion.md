# Taylor series expansion

Expanding the integrand around $t=0$:
   $$\sin(t^2) = t^2 - \frac{t^6}{6} + O(t^{10}), \quad \frac{1}{1+t^2} = 1 - t^2 + t^4 - t^6 + O(t^8)$$
   Multiplying through terms up to degree $8$:
   $$g(t) = \left(t^2 - \frac{t^6}{6}\right)(1 - t^2 + t^4 - t^6) + O(t^{10}) = t^2 - t^4 + \frac{5}{6}t^6 - \frac{5}{6}t^8 + O(t^{10}).$$
   Integrating term-by-term from $0$ to $x$:
   $$f(x) = \frac{x^3}{3} - \frac{x^5}{5} + \frac{5}{42}x^7 - \frac{5}{54}x^9 + O(x^{11}).$$

**Lean formalization.** Over $\mathbb{Q}$, `sinTrunc` is $t^2-t^6/6$ and `sinNextTerm` is $t^{10}/120$; `sinTrunc10` is their sum. `geomTrunc` is $1-t^2+t^4-t^6$ with next term `geomNextTerm` $=t^8$ and `geomTrunc8` the sum through degree $8$. `productExact` multiplies the factor truncations; `productTail` is the $t^{10}+$ remainder $-\tfrac16 t^{10}+\tfrac16 t^{12}$; `gTrunc` is the degree-$8$ product $t^2-t^4+\tfrac56 t^6-\tfrac56 t^8$. `integrateMonomial c n x` is $c\,x^{n+1}/(n+1)$; `T9 x` is the term-by-term integral of `gTrunc` through $x^9$.

**Theorem** (`productExact_eq`). For every $t\in\mathbb{Q}$, `productExact t` $=$ `gTrunc t` $+$ `productTail t`.

**Proof.** Expand definitions and `ring`.

**Theorem** (`product_trunc_eq`). For every $t$, discarding `productTail` leaves `gTrunc`.

**Proof.** Rearrange `productExact_eq`.

**Theorem** (`T9_eq_sum`). For every $x$, `T9 x` $= x^3/3 - x^5/5 + (5/6)(x^7/7) - (5/6)(x^9/9)$.

**Proof.** Unfold `T9` and `integrateMonomial`, then `ring`.

**Theorem** (`integrate_coeff_t6`). $(5/6)/7 = 5/42$ in $\mathbb{Q}$.

**Proof.** `norm_num`.

**Theorem** (`integrate_coeff_t8`). $(5/6)/9 = 5/54$ in $\mathbb{Q}$.

**Proof.** `norm_num`.

**Theorem** (`T9_simplified`). For every $x$, `T9 x` $= x^3/3 - x^5/5 + 5x^7/42 - 5x^9/54$.

**Proof.** From `T9_eq_sum`, rewrite the $x^7$ and $x^9$ terms using `integrate_coeff_t6` and `integrate_coeff_t8`.

**[BachelorsInMeasurementTheory/Course21120/TaylorExpansion.lean](../../BachelorsInMeasurementTheory/Course21120/TaylorExpansion.lean)**

@import "../../BachelorsInMeasurementTheory/Course21120/TaylorExpansion.lean"
