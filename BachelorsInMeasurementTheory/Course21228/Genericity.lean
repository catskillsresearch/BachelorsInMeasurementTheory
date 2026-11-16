module

public import Mathlib.Algebra.Group.End
import Mathlib.Data.Finset.Attr
import Mathlib.Tactic.SetLike
import Mathlib.Tactic.TypeStar

@[expose] public section

open Equiv

namespace Course21228

variable {n : ℕ} {α : Type*}

/-- Assumption 1: the vectors in \(x\) are pairwise distinct. -/
def PairwiseDistinct (x : Fin n → α) : Prop :=
  Function.Injective x

/-- Assumption 2: \(y\) is a permutation of \(x\), so the multisets agree. -/
def MultisetCompatible (x y : Fin n → α) : Prop :=
  ∃ τ : Perm (Fin n), y = x ∘ τ

theorem pairwiseDistinct_iff (x : Fin n → α) :
    PairwiseDistinct x ↔ ∀ i j : Fin n, x i = x j → i = j :=
  Iff.rfl

theorem multisetCompatible_of_perm (x : Fin n → α) (τ : Perm (Fin n)) :
    MultisetCompatible x (x ∘ τ) :=
  ⟨τ, rfl⟩

end Course21228
