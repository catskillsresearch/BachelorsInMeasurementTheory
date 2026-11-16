module

public import Mathlib.Algebra.BigOperators.Group.Finset.Basic
public import Mathlib.Algebra.Module.Pi
public import Mathlib.Basic.Real.Basic
public import Mathlib.LinearAlgebra.StdBasis
public import BSinMeasurementTheory.Course21241.Space

@[expose] public section

open BigOperators

namespace Course21241

/-- Standard primal basis vectors of V. -/
def e (i : Fin 3) : V := Pi.single i 1

/-- Every vector \(x \in V\) expands uniquely in the primal basis. -/
theorem vector_eq_sum (x : V) :
    x = ∑ i : Fin 3, x i • e i := by
  ext j
  simp [e, Pi.single_apply, smul_eq_mul, Finset.sum_ite_eq]

/-- The basis vectors \(\{e\,0, e\,1, e\,2\}\) are linearly independent. -/
theorem e_linearIndependent :
    LinearIndependent ℝ e :=
  Pi.linearIndependent_single_one (Fin 3) ℝ

end Course21241
