module

public import Mathlib.Algebra.BigOperators.Fin
public import Mathlib.Algebra.BigOperators.Group.Finset.Basic
public import Mathlib.Basic.Real.Basic
public import BSinMeasurementTheory.Course21241.SeparatingU
public import BSinMeasurementTheory.Course21241.Separation
import Mathlib.Tactic.Ring

@[expose] public section

open BigOperators Matrix
open Finset

namespace Course21241

theorem dot_u_c_sum (c : V) :
    dot u c = ∑ i : Fin 3, u i * c i := rfl

theorem dot_u_c_expansion (c : V) :
    dot u c = (1 : ℝ) * c 0 + 0 * c 1 + 0 * c 2 := by
  simp [dot, dotProduct, Fin.sum_univ_three, u_zero, u_one, u_two]

theorem dot_u_c_eq_coord (c : V) :
    dot u c = c 0 := by
  rw [dot_u_c_expansion]
  ring

theorem dot_u_c_nonneg (c : V) (hc : c ∈ C) :
    0 ≤ dot u c := by
  rw [dot_u_c_eq_coord]
  exact hc 0

end Course21241
