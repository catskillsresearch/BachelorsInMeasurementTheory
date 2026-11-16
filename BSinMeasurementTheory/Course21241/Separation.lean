module

public import Mathlib.Algebra.BigOperators.Fin
public import Mathlib.Algebra.BigOperators.Group.Finset.Basic
public import Mathlib.Algebra.Module.LinearMap.Basic
public import Mathlib.Algebra.Order.BigOperators.Group.Finset
public import Mathlib.Basic.Real.Basic
public import Mathlib.Data.Matrix.Mul
public import Mathlib.LinearAlgebra.Matrix.Dual
public import BSinMeasurementTheory.Course21241.Basis
import Mathlib.Tactic.Linarith

@[expose] public section

open BigOperators Matrix

namespace Course21241

/-- Standard Euclidean inner product on V. -/
def dot (u v : V) : ℝ := u ⬝ᵥ v

lemma dot_comm (u v : V) : dot u v = dot v u :=
  dotProduct_comm u v

lemma dot_e (u : V) (i : Fin 3) : dot u (e i) = u i := by
  simp [dot, e, dotProduct_single]

/-- Riesz map from V to V*. -/
def toDual (u : V) : V →ₗ[ℝ] ℝ :=
  (dotProductEquiv ℝ (Fin 3)) u

/-- Inverse Riesz map from V* to V. -/
def toVec (φ : V →ₗ[ℝ] ℝ) : V :=
  (dotProductEquiv ℝ (Fin 3)).symm φ

theorem toDual_toVec (φ : V →ₗ[ℝ] ℝ) : toDual (toVec φ) = φ :=
  (dotProductEquiv ℝ (Fin 3)).apply_symm_apply φ

theorem toVec_toDual (u : V) : toVec (toDual u) = u :=
  (dotProductEquiv ℝ (Fin 3)).symm_apply_apply u

/-- Characterization of functionals nonnegative on C. -/
theorem nonneg_on_C_iff (u : V) :
    (∀ c ∈ C, 0 ≤ dot u c) ↔ ∀ i : Fin 3, 0 ≤ u i := by
  constructor
  · intro h i
    have hei : e i ∈ C := by
      intro j
      simp [e, Pi.single_apply]
      split_ifs <;> linarith
    simpa [dot_e] using h (e i) hei
  · intro hu c hc
    dsimp [dot]
    exact Finset.sum_nonneg fun i _ => mul_nonneg (hu i) (hc i)

/-- Existence of a separating vector under the inner product for any v ∉ C. -/
theorem exists_separating_vector (v : V) (hv : v ∉ C) :
    ∃ u : V, (∀ c ∈ C, 0 ≤ dot u c) ∧ dot u v < 0 := by
  change ¬ (∀ i : Fin 3, 0 ≤ v i) at hv
  push Not at hv
  rcases hv with ⟨i, hi⟩
  use e i
  constructor
  · rw [nonneg_on_C_iff]
    intro j
    simp [e, Pi.single_apply]
    split_ifs <;> linarith
  · rw [dot_comm, dot_e]
    exact hi

end Course21241
