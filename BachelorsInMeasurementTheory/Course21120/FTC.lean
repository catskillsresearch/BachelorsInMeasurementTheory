module

public import Mathlib.Analysis.Calculus.Deriv.Basic
public import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

@[expose] public section

open Real -- gives `sin` and `pow`

namespace Course21120FTC

/-- Definition of f(x) = ∫₀ˣ sin(t²) / (1 + t²) dt -/
noncomputable def f (x : ℝ) : ℝ := ∫ t in (0 : ℝ)..x, sin (t ^ 2) / (1 + t ^ 2)

/-- The integrand is continuous everywhere on ℝ. -/
lemma continuous_integrand : Continuous (fun t : ℝ => sin (t ^ 2) / (1 + t ^ 2)) :=
  (continuous_sin.comp (continuous_pow 2)).div
    (continuous_const.add (continuous_pow 2)) fun _ => by positivity

/-- Fundamental theorem of calculus derivative statement for f. -/
lemma f_hasDerivAt (x : ℝ) : HasDerivAt f (sin (x ^ 2) / (1 + x ^ 2)) x :=
  HasStrictDerivAt.hasDerivAt (continuous_integrand.integral_hasStrictDerivAt 0 x)

/-- (a) Part 1: f is differentiable everywhere on ℝ. -/
theorem part_a_differentiable (x : ℝ) : DifferentiableAt ℝ f x :=
  HasDerivAt.differentiableAt (f_hasDerivAt x)

/-- (a) Part 2: f'(x) = sin(x²) / (1 + x²). -/
theorem part_a_deriv (x : ℝ) : deriv f x = sin (x ^ 2) / (1 + x ^ 2) :=
  HasDerivAt.deriv (f_hasDerivAt x)

end Course21120FTC
