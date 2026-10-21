# Recursion and termination

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="recursion-structural"></a>
## Structural recursion first

Prefer structural recursion, where each recursive call is on a part of an argument, such as the tail of a list. Lean proves these functions terminate without help, and proofs about them are the easiest to write. When the recursion isn't structural, give a decreasing measure with `termination_by`, and a proof with `decreasing_by` if Lean can't find one.

```lean
-- good
def length {α : Type} : List α → Nat
  | [] => 0
  | _ :: xs => length xs + 1

def gcd (a b : Nat) : Nat :=
  if h : b = 0 then a else gcd b (a % b)
termination_by b
decreasing_by exact Nat.mod_lt _ (Nat.pos_of_ne_zero h)
```

*Source: [Joachim Breitner][breitner].*

<a name="recursion-partial"></a>
## `partial`

Mark a function `partial` when it might not terminate, or when proving that it does isn't worth it and you won't prove anything about it. Lean then compiles it without a termination proof, but it can't see inside it in proofs. Its return type must have a value, so derive `Inhabited` or `Nonempty` if Lean can't find one. Add a comment when the reason for `partial` isn't obvious.

```lean
-- good
/-- Counts the steps the Collatz sequence takes to reach 1. Nobody knows if it always does. -/
partial def collatzSteps (n : Nat) (steps : Nat := 0) : Nat :=
  if n ≤ 1 then steps
  else if n % 2 == 0 then collatzSteps (n / 2) (steps + 1)
  else collatzSteps (3 * n + 1) (steps + 1)
```

If you'll want a termination proof later, start with `partial` and test the function first. Then switch to `termination_by` and prove it, so you don't spend time proving that a buggy function terminates.

*Sources: [Lean Reference][ref-partial], [FPIL][fpil-partial], [FRO practice][fro-c].*

<a name="recursion-loops"></a>
## Loops

Use `for`, `while` and `repeat` in a `do` block instead of a recursive helper that only loops. They also spare you a `partial` function.

```lean
-- bad
partial def readLines (stdin : IO.FS.Stream) (acc : Array String) : IO (Array String) := do
  let line ← stdin.getLine
  if line.isEmpty then return acc
  readLines stdin (acc.push line)
```

```lean
-- good
def readLines (stdin : IO.FS.Stream) : IO (Array String) := do
  let mut lines := #[]
  repeat
    let line ← stdin.getLine
    if line.isEmpty then break
    lines := lines.push line
  return lines
```

*Source: [FPIL][fpil-loops].*

<a name="recursion-deep"></a>
## Deep recursion

For inputs that can be large, use a loop or a recursive helper with an accumulator, like `go` in [Local helpers](functions.md#functions-helpers). A recursive call that isn't the last step of a function uses stack space, and a long enough input overflows the stack.

*Source: [FPIL][fpil-tail].*

---

Previous: [Collections](collections.md) · [Contents](../README.md#rules) · Next: [Proofs about programs](proofs.md)


[breitner]: https://lean-lang.org/blog/2024-1-11-recursive-definitions-in-lean
[fpil-loops]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L100-L113
[fpil-partial]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L110-L126
[fpil-tail]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/TailRecursion.lean#L30
[fro-c]: ../research/author-survey.md#consistent-across-authors
[ref-partial]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs.lean#L195-L211
