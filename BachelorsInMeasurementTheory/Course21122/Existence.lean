module

public import Mathlib.Analysis.Complex.Trigonometric
public import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
public import Mathlib.MeasureTheory.Integral.IntegralEqImproper
public import BachelorsInMeasurementTheory.Course21120.FTC

@[expose] public section

open Real Filter Topology MeasureTheory Set

namespace Course21122

/-- Pointwise comparison: the integrand is dominated by $1/(1+t^2)$,
which is the majorant used to get absolute convergence of the improper
integral. -/
theorem abs_integrand_le (t : ℝ) :
    |sin (t ^ 2) / (1 + t ^ 2)| ≤ 1 / (1 + t ^ 2) := by
  have hpos : 0 < 1 + t ^ 2 := by nlinarith [sq_nonneg t]
  rw [abs_div, abs_of_pos hpos]
  exact div_le_div_of_nonneg_right (abs_sin_le_one _) hpos.le

/-- The comparison majorant is integrable on $\mathbb{R}$. -/
theorem integrable_majorant : Integrable fun t : ℝ => (1 : ℝ) / (1 + t ^ 2) := by
  simpa [one_div] using integrable_inv_one_add_sq

/-- Absolute convergence: the Fresnel-type integrand is integrable on $\mathbb{R}$. -/
theorem integrable_integrand :
    Integrable fun t : ℝ => sin (t ^ 2) / (1 + t ^ 2) :=
  Integrable.mono' integrable_majorant
    Course21120FTC.continuous_integrand.aestronglyMeasurable
    (Filter.Eventually.of_forall fun t => by
      rw [Real.norm_eq_abs, one_div]
      simpa [one_div] using abs_integrand_le t)

/-- Restriction of absolute convergence to $(0,\infty)$. -/
theorem integrableOn_integrand_Ioi :
    IntegrableOn (fun t : ℝ => sin (t ^ 2) / (1 + t ^ 2)) (Ioi 0) :=
  integrable_integrand.integrableOn

/-- As $x\to\infty$, $f(x)=\int_0^x \sin(t^2)/(1+t^2)\,dt$ tends to the improper
integral over $(0,\infty)$. -/
theorem f_tendsto_integral_Ioi :
    Tendsto Course21120FTC.f atTop
      (𝓝 (∫ t in Ioi (0 : ℝ), sin (t ^ 2) / (1 + t ^ 2))) :=
  intervalIntegral_tendsto_integral_Ioi (a := 0) integrableOn_integrand_Ioi tendsto_id

/-- Hence $\lim_{x\to\infty} f(x)$ exists. -/
theorem f_limit_exists : ∃ L : ℝ, Tendsto Course21120FTC.f atTop (𝓝 L) :=
  ⟨_, f_tendsto_integral_Ioi⟩

end Course21122
