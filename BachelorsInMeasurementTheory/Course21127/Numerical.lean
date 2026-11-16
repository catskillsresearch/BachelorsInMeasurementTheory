module

public import Mathlib.Data.Rat.Defs
public import BachelorsInMeasurementTheory.Course21127.NonzeroDenomInt
public import BachelorsInMeasurementTheory.Course21127.ToRat -- shake: keep
import Mathlib.Tactic.NormNum.Abs
import Mathlib.Tactic.NormNum.DivMod
import Mathlib.Tactic.NormNum.OfScientific
import Mathlib.Tactic.NormNum.Pow

@[expose] public section

namespace Course21127

-- Example 1: (1, 2) ~ (2, 4) since 1 * 4 = 2 * 2 = 4
def pair1 : NonzeroDenomInt := ⟨1, 2, by decide⟩
def pair2 : NonzeroDenomInt := ⟨2, 4, by decide⟩

example : Rel pair1 pair2 := by
  dsimp [Rel, pair1, pair2]

-- Example 2: Both pairs map to 1/2 in ℚ under toRat
example : toRat pair1 = 1 / 2 := by
  norm_num [toRat, pair1]

example : toRat pair2 = 1 / 2 := by
  norm_num [toRat, pair2]

end Course21127
