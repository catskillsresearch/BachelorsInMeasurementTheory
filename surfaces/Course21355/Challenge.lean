/-
Copyright (c) 2026 Lars Warren Ericson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Lars Warren Ericson.
-/
module

public import Mathlib.Basic.Real.Basic
public import Mathlib.Order.ConditionallyCompleteLattice.Basic
public import Mathlib.Order.Filter.AtTopBot.Basic
public import Mathlib.Order.Interval.Set.Basic
public import Mathlib.Topology.Defs.Filter
public import Mathlib.Topology.Order.Compact
public import Mathlib.Topology.UniformSpace.Real

@[expose] public section

open Filter Topology

/-!
# Challenge — Course 21-355
-/

namespace Course21355

noncomputable section

/-- Tail supremum $y_k = \sup_{n\ge k} x_n$. -/
def tailSup (x : ℕ → ℝ) (k : ℕ) : ℝ := ⨆ n : ℕ, x (n + k)

/-- Tail infimum $z_k = \inf_{n\ge k} x_n$. -/
def tailInf (x : ℕ → ℝ) (k : ℕ) : ℝ := ⨅ n : ℕ, x (n + k)

theorem limsup_liminf_exist (x : ℕ → ℝ) (m M : ℝ) (h : ∀ n, m ≤ x n ∧ x n ≤ M) :
    (∃ L_sup : ℝ, Tendsto (tailSup x) atTop (𝓝 L_sup)) ∧
    (∃ L_inf : ℝ, Tendsto (tailInf x) atTop (𝓝 L_inf)) := by
  sorry

end

/-- Closed bounded intervals in `ℝ` are compact. -/
theorem compact_Icc (a b : ℝ) : IsCompact (Set.Icc a b) := by
  sorry

end Course21355
