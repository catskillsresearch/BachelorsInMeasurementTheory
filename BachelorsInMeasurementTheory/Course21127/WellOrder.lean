module

public import Mathlib.Algebra.Order.Ring.Unbundled.Rat
public import Mathlib.Basic.Finite.Defs
public import Mathlib.Order.Interval.Set.Defs
import Mathlib.Data.List.MinMax
import Mathlib.Data.Set.Finite.Basic
import Mathlib.Tactic.Lemma

@[expose] public section

namespace Course21127

/-- A subset of Q is well-ordered under the usual order if every nonempty
    subset has a least element in the set. -/
class IsWellOrderedSet (S : Set ℚ) : Prop where
  least : ∀ T : Set ℚ, T ⊆ S → T.Nonempty → ∃ m ∈ T, ∀ x ∈ T, m ≤ x

/-- The false claim stated in the prompt using Set.Ici to avoid untyped binder problems. -/
def FalseClaim : Prop :=
  ∀ S : Set ℚ, S ⊆ Set.Ici (0 : ℚ) → S.Nonempty → IsWellOrderedSet S →
    (S = ∅ ∨ Set.Infinite S)

lemma singleton_zero_well_ordered : IsWellOrderedSet {(0 : ℚ)} where
  least T hT hne := by
    rcases hne with ⟨t, ht⟩
    have ht0 : t = 0 := hT ht
    subst ht0
    refine ⟨0, ht, ?_⟩
    intro x hx
    have hx0 : x = 0 := hT hx
    subst hx0
    exact le_rfl

lemma singleton_zero_nonneg : ({(0 : ℚ)} : Set ℚ) ⊆ Set.Ici 0 :=
  Set.singleton_subset_iff.mpr (Set.mem_Ici.mpr le_rfl)

lemma singleton_zero_nonempty : ({(0 : ℚ)} : Set ℚ).Nonempty :=
  ⟨0, rfl⟩

/-- (c) Refutation by contradiction:
    The claim implies that {0} must be empty or infinite, both of which are false. -/
theorem false_claim_is_false : ¬ FalseClaim := by
  intro hclaim
  have h_cases := hclaim {0} singleton_zero_nonneg singleton_zero_nonempty
    singleton_zero_well_ordered
  cases h_cases with
  | inl h_empty =>
    have h0 : (0 : ℚ) ∈ ({(0 : ℚ)} : Set ℚ) := rfl
    rw [h_empty] at h0
    exact h0
  | inr h_inf =>
    exact h_inf (Set.finite_singleton 0)

/-- Correct positive statement:
    Every nonempty finite list of rationals contains a least element. -/
lemma list_has_min (a : ℚ) (l : List ℚ) : ∃ m ∈ a :: l, ∀ x ∈ a :: l, m ≤ x := by
  have hlen : 0 < (a :: l).length := by simp
  refine ⟨List.minimum_of_length_pos hlen, List.minimum_of_length_pos_mem hlen, ?_⟩
  intro x hx
  exact List.minimum_of_length_pos_le_of_mem hx hlen

end Course21127
