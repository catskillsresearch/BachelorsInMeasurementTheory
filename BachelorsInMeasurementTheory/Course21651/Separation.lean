module

public import Mathlib.Topology.Connected.TotallyDisconnected
public import BachelorsInMeasurementTheory.Course21651.BooleanHom
import Mathlib.Algebra.Order.Algebra
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.EReal.Inv
import Mathlib.Tactic.ContinuousFunctionalCalculus
import Mathlib.Tactic.TypeStar
import Mathlib.Topology.NoetherianSpace

@[expose] public section

set_option linter.unusedSectionVars false

open Topology Set

namespace Course21651

namespace StoneRepresentation

variable (B : Type*) [BooleanAlgebra B]

instance : T2Space (StoneSpace B) := inferInstance

instance : TotallyDisconnectedSpace (StoneSpace B) := inferInstance

instance [Finite B] : CompactSpace (StoneSpace B) := inferInstance

end StoneRepresentation

end Course21651
