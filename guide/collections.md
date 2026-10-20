# Collections

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="collections-array"></a>
## `Array` or `List`

Use `Array` for sequences you build up, index into or update. Use `List` when you mostly take a sequence apart from the front with pattern matching, or when it's small. Appending to the end of a `List` copies it, so building one in a loop takes quadratic time. Pushing onto an `Array` that nothing else refers to happens in place.

```lean
-- bad
def squares (n : Nat) : List Nat := Id.run do
  let mut out := []
  for i in [0:n] do
    out := out ++ [i * i]
  return out
```

```lean
-- good
def squares (n : Nat) : Array Nat := Id.run do
  let mut out := #[]
  for i in [0:n] do
    out := out.push (i * i)
  return out
```

*Sources: [FPIL][fpil-arrays], [Lean Reference][ref-array].*

<a name="collections-sharing"></a>
## Unshared arrays

Keep a single reference to an array you're updating, so Lean can update it in place. If another variable still refers to the old version, each update copies the whole array. `dbgTraceIfShared` reports copies in a compiled program.

*Sources: FPIL on [unique references][fpil-unique] and [checking for copies][fpil-copy].*

<a name="collections-iterate"></a>
## Iteration and indexing

Loop over the elements with `for x in xs` rather than over indices. When you do index, use `xs[i]?` if the index may be out of range, and `xs[i]` with a proof if you know it isn't. Use `xs[i]!` only when an out-of-range index would be a bug (see [Panics](errors.md#errors-panics)).

```lean
-- bad
def sum (xs : Array Nat) : Nat := Id.run do
  let mut total := 0
  for i in [0:xs.size] do
    total := total + xs[i]!
  return total

def outputPath (args : Array String) : String := args[1]!
```

```lean
-- good
def sum (xs : Array Nat) : Nat := Id.run do
  let mut total := 0
  for x in xs do
    total := total + x
  return total

def outputPath? (args : Array String) : Option String := args[1]?
```

*Source: [FPIL][fpil-index].*

<a name="collections-maps"></a>
## Maps

Use `Std.HashMap` to look values up by key, and `Std.TreeMap` when you need the keys in order. A list of pairs is fine for a handful of entries.

```lean
import Std.Data.HashMap

-- good
def countWords (words : List String) : Std.HashMap String Nat :=
  words.foldl (fun counts w => counts.insert w (counts.getD w 0 + 1)) {}
```

---

Previous: [Type classes and instances](classes.md) · [Contents](../README.md#rules) · Next: [Error handling](errors.md)


[fpil-arrays]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Indexing.lean#L26
[fpil-copy]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L512-L513
[fpil-index]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/PropsProofsIndexing.lean#L287-L331
[fpil-unique]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L691
[ref-array]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/BasicTypes/Array.lean#L28-L38
