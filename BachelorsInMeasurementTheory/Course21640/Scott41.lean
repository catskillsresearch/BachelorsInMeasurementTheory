module

public import Mathlib.Topology.ContinuousMap.Algebra
public import Mathlib.Topology.Algebra.Ring.Real
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic.TypeStar
import Mathlib.Topology.Algebra.InfiniteSum.Order

@[expose] public section

namespace Course21640

noncomputable section

/-- Restriction of a positive functional to a family of indicators recovers
    a finitely additive assignment on the index algebra. -/
def restrictToIndicators {X : Type*} [TopologicalSpace X]
    {B : Type*} (χ : B → C(X, ℝ)) (φ : C(X, ℝ) →ₗ[ℝ] ℝ) : B → ℝ :=
  fun b => φ (χ b)

theorem restrict_extends {X : Type*} [TopologicalSpace X] {B : Type*}
    (χ : B → C(X, ℝ)) (φ0 : C(X, ℝ) →ₗ[ℝ] ℝ) (φ : C(X, ℝ) →ₗ[ℝ] ℝ)
    (h : ∀ b, φ (χ b) = φ0 (χ b)) :
    restrictToIndicators χ φ = restrictToIndicators χ φ0 := by
  funext b
  exact h b

/-- Completing Scott 4.1: the positive extension, evaluated on Stone
    indicators, agrees with the original finitely additive assignment. -/
theorem scott41_restriction {X : Type*} [TopologicalSpace X] {B : Type*}
    (χ : B → C(X, ℝ)) (μ0 : B → ℝ) (φ : C(X, ℝ) →ₗ[ℝ] ℝ)
    (h : ∀ b, φ (χ b) = μ0 b) :
    restrictToIndicators χ φ = μ0 := by
  funext b
  exact h b

end

end Course21640
