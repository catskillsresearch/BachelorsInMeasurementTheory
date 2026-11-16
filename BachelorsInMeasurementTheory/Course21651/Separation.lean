module

public import Mathlib.Order.BooleanAlgebra.Basic
public import Mathlib.Topology.Connected.TotallyDisconnected
public import Mathlib.Topology.ContinuousMap.Compact
public import BachelorsInMeasurementTheory.Course21651.BooleanHom

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
