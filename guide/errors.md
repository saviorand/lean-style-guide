# Error handling

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="errors-option-except"></a>
## `Option` or `Except`

Return an `Option` when there's only one way to fail and the caller can see what it is, such as a missing key. Return `Except ε α` when the caller needs to know which of several failures happened.

```lean
-- bad: the caller can't tell a missing age from a bad one
def parseAge (s : String) : Option Nat := do
  if s.isEmpty then none
  let n ← s.toNat?
  if n > 150 then none
  return n
```

```lean
-- good
inductive AgeError where
  | missing
  | notANumber (input : String)
  | tooLarge (n : Nat)
deriving Repr

def parseAge (s : String) : Except AgeError Nat := do
  if s.isEmpty then throw .missing
  let some n := s.toNat? | throw (.notANumber s)
  if n > 150 then throw (.tooLarge n)
  return n
```

*Source: [FPIL][fpil-except].*

<a name="errors-types"></a>
## Error types

Give a library an inductive error type with one constructor per kind of failure, as in `AgeError` above, and a `ToString` instance for messages. `IO.ofExcept` needs that instance to turn an `Except` into an `IO` error. Callers can match on an inductive type, but all they can do with a `String` is print it. Plain `String` errors are fine at the outer layer of an application.

```lean
inductive AgeError where
  | missing
  | notANumber (input : String)
  | tooLarge (n : Nat)

-- good
instance : ToString AgeError where
  toString
    | .missing => "age is missing"
    | .notANumber s => s!"not a number: {s}"
    | .tooLarge n => s!"age too large: {n}"
```

*Sources: [`IO.Error`][std-ioerror] in the standard library, [`CliError`][lake-clierror] in Lake.*

<a name="errors-io"></a>
## Errors in `IO` code

In `IO` code, report a failure by throwing it. Use `IO.ofExcept` to turn an `Except` into a thrown error where pure code meets `IO`. Don't turn an error into a default value, because then the caller can't tell that anything went wrong.

```lean
def parseAge (s : String) : Except String Nat :=
  match s.toNat? with
  | some n => .ok n
  | none => .error s!"not a number: {s}"

-- bad
def loadAge (path : System.FilePath) : IO Nat := do
  match parseAge (← IO.FS.readFile path).trimAscii.toString with
  | .ok age => return age
  | .error e =>
    IO.eprintln e
    return 0
```

```lean
def parseAge (s : String) : Except String Nat :=
  match s.toNat? with
  | some n => .ok n
  | none => .error s!"not a number: {s}"

-- good
def loadAge (path : System.FilePath) : IO Nat := do
  IO.ofExcept (parseAge (← IO.FS.readFile path).trimAscii.toString)
```

*Source: [FRO practice][fro-d].*

<a name="errors-panics"></a>
## Panics

Use `panic!`, `unreachable!` and functions ending in `!` only when it's essential: for a condition that would be a bug in your own code, where you can't pass a proof that it holds instead. Never use them to reject bad input. A panic doesn't stop a Lean program. It prints a message and the program carries on with a default value:

```lean
def risky (xs : Array Nat) : Nat := xs[5]!

def main : IO Unit := do
  IO.println s!"before {risky #[1, 2]}"
  IO.println "after"
```

```text
Error: index out of bounds
backtrace:
...
before 0
after
```

Set the environment variable `LEAN_ABORT_ON_PANIC` to make the program abort on the first panic instead.

*Sources: [Lean naming conventions][cn-data], [Google Haskell guide][google-partial], [Lean runtime][lean-panic], [checked with Lean 4.35][checked], [Paul Butcher, issue #1][issue-1].*

<a name="errors-document"></a>
## Documenting failure

Say in the docstring how a function fails: what `none` means, which errors it throws and when it panics.

```lean
-- good
/-- Returns the price of `item`, or `none` if the list doesn't contain it. -/
def price? (prices : List (String × Nat)) (item : String) : Option Nat :=
  prices.lookup item

/-- Returns the price of `item`. Panics if the list doesn't contain it. -/
def price! (prices : List (String × Nat)) (item : String) : Nat :=
  (prices.lookup item).get!
```

*Source: standard library docstrings, such as [`Array.swapAt!`][std-doc-panics] and [`IO.FS.createDir`][std-doc-throws].*

---

Previous: [Effects and `do` notation](effects.md) · [Contents](../README.md#rules) · Next: [API design and visibility](api.md)

[checked]: ../research/decisions.md#facts-checked-while-drafting
[cn-data]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#naming-convention-for-data
[fpil-except]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L206-L218
[fro-d]: ../research/author-survey.md#author-dependent-no-fro-convention
[google-partial]: https://google.github.io/styleguide/haskellguide.html#partial-functions
[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
[lake-clierror]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/CLI/Error.lean#L16
[lean-panic]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/runtime/object.cpp#L80
[std-doc-panics]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/Array/Basic.lean#L447-L455
[std-doc-throws]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/System/IO.lean#L896-L900
[std-ioerror]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/System/IOError.lean#L24
