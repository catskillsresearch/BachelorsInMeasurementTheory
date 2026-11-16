module

public import Mathlib.Basic.Real.Basic
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic.Lemma
import Mathlib.Tactic.NormNum.Abs
import Mathlib.Tactic.NormNum.DivMod
import Mathlib.Tactic.NormNum.OfScientific
import Mathlib.Tactic.NormNum.Pow

@[expose] public section

namespace Course21355

noncomputable section

def altSeq (n : ℕ) : ℝ := (-1 : ℝ) ^ n

lemma altSeq_even (k : ℕ) : altSeq (2 * k) = 1 := by
  dsimp [altSeq]
  rw [pow_mul]
  have : (-1 : ℝ) ^ 2 = 1 := by norm_num
  rw [this, one_pow]

lemma altSeq_odd (k : ℕ) : altSeq (2 * k + 1) = -1 := by
  dsimp [altSeq]
  rw [pow_add, pow_one, pow_mul]
  have : (-1 : ℝ) ^ 2 = 1 := by norm_num
  rw [this, one_pow, one_mul]

end

end Course21355
