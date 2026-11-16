module

public import Mathlib.Basic.Real.Basic
public import Mathlib.Order.Interval.Set.Basic
public import Mathlib.Topology.Order.Compact
public import Mathlib.Topology.UniformSpace.Real

@[expose] public section

namespace Course21355

/-- Closed bounded intervals in `ℝ` are compact. -/
theorem compact_Icc (a b : ℝ) : IsCompact (Set.Icc a b) :=
  isCompact_Icc

end Course21355
