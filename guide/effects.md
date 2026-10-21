# Effects and `do` notation

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="effects-pure-core"></a>
## Pure core and `IO` shell

Write the logic of a program as pure functions, and keep `IO` in a thin layer around them. Pure functions are easier to test and to reason about. Keep `main` short.

```lean
-- bad
def main (args : List String) : IO UInt32 := do
  let mut total := 0
  for arg in args do
    match arg.toNat? with
    | some n => total := total + n
    | none =>
      IO.eprintln s!"not a number: {arg}"
      return 1
  IO.println s!"sum: {total}"
  return 0
```

```lean
-- good
def sumArgs (args : List String) : Except String Nat :=
  args.foldlM (init := 0) fun total arg =>
    match arg.toNat? with
    | some n => .ok (total + n)
    | none => .error s!"not a number: {arg}"

def main (args : List String) : IO UInt32 := do
  match sumArgs args with
  | .ok total =>
    IO.println s!"sum: {total}"
    return 0
  | .error msg =>
    IO.eprintln msg
    return 1
```

*Sources: FPIL on [application structure][fpil-core] and [`Main.lean`][fpil-main].*

<a name="effects-config"></a>
## Configuration

Pass configuration that many functions need through `ReaderT`, instead of adding an argument to each function. Define your application's monad with `abbrev`, so Lean still finds the instances of `ReaderT` and `IO`.

```lean
-- good
structure Config where
  verbose : Bool
  root : System.FilePath

abbrev AppM := ReaderT Config IO

def log (msg : String) : AppM Unit := do
  if (← read).verbose then IO.println msg

def resolve (path : String) : AppM System.FilePath := do
  log s!"resolving {path}"
  return (← read).root / path

def runApp (cfg : Config) : IO Unit := do
  IO.println (← (resolve "index.html").run cfg)
```

*Sources: FPIL on [readers][fpil-reader] and [`abbrev` stacks][fpil-abbrev-stack].*

<a name="effects-resources"></a>
## Releasing resources

Put code that acquires and releases a resource in a `with…` helper, such as `withTempFile` below, so callers can't forget the release. Build the helper with `try … finally`, so the release runs even when the work throws. Lean closes a file handle when the last reference to it goes away, but temporary files, child processes and locks need explicit cleanup.

```lean
-- bad: if `process` throws, the file is never removed
def processScratch (process : System.FilePath → IO Unit) : IO Unit := do
  let (_, path) ← IO.FS.createTempFile
  process path
  IO.FS.removeFile path
```

```lean
-- good
def withTempFile {α : Type} (action : System.FilePath → IO α) : IO α := do
  let (_, path) ← IO.FS.createTempFile
  try
    action path
  finally
    IO.FS.removeFile path
```

*Sources: [Haskell `bracket`][hs-bracket], [Lean source][lean-io-handle].*

<a name="effects-concurrency"></a>
## Concurrency

Use plain `IO` for sequential programs, `Task`s for parallel computation, and `Async` for programs that spend most of their time waiting on I/O, such as servers. In a long-running task that does I/O, call `IO.checkCanceled` from time to time, so the task stops when it is cancelled.

```lean
-- good
def sumRange (lo hi : Nat) : Nat := Id.run do
  let mut total := 0
  for i in [lo:hi] do
    total := total + i
  return total

def parallelSum (n : Nat) : Nat :=
  let left := Task.spawn fun _ => sumRange 0 (n / 2)
  let right := Task.spawn fun _ => sumRange (n / 2) n
  left.get + right.get
```

*Sources: Lean Reference on [`Async`][ref-async] and [cancellation][ref-cancel].*

<a name="effects-eval"></a>
## Side effects at compile time

Don't `#eval` actions with side effects in library files. Lean runs every `#eval` when it elaborates the file, so the action also runs in your editor and in other people's builds. Put such checks in tests or in an executable.

*Source: [FPIL][fpil-eval].*

<a name="do-early-return"></a>
## Early return

Handle special cases first and leave with `return` or `throw`, so the main path of the function isn't nested inside them.

```lean
-- bad
def withdraw (balance amount : Nat) : Except String Nat := do
  if amount > 0 then
    if amount ≤ balance then
      return balance - amount
    else
      throw "insufficient funds"
  else
    throw "amount must be positive"
```

```lean
-- good
def withdraw (balance amount : Nat) : Except String Nat := do
  if amount = 0 then throw "amount must be positive"
  if amount > balance then throw "insufficient funds"
  return balance - amount
```

*Sources: [Lean core style][cs-do], [FPIL][fpil-early].*

<a name="do-let-else"></a>
## Unwrapping with a fallback

Use `let some x := e | fallback`, or `let some x ← action | fallback`, to unwrap an `Option` when the failure case is short. A chain of these reads top to bottom, where nested `match`es drift to the right.

```lean
-- bad
def greeting (users : List (Nat × String)) (args : List String) : Except String String :=
  match args.head? with
  | none => .error "missing id"
  | some arg =>
    match arg.toNat? with
    | none => .error s!"bad id {arg}"
    | some id =>
      match users.lookup id with
      | none => .error s!"no user {id}"
      | some name => .ok s!"Hello, {name}"
```

```lean
-- good
def greeting (users : List (Nat × String)) (args : List String) : Except String String := do
  let some arg := args.head? | throw "missing id"
  let some id := arg.toNat? | throw s!"bad id {arg}"
  let some name := users.lookup id | throw s!"no user {id}"
  return s!"Hello, {name}"
```

*Source: [Lean core style][cs-do].*

<a name="do-mutation"></a>
## Local mutation

Inside a function, use `let mut` and `for` loops when they're clearer than a fold or an explicit state monad. The mutation stays local, and the function is still pure from the outside.

```lean
-- bad
def stats (xs : Array Int) : Int × Int × Nat :=
  xs.foldl (fun (lo, hi, n) x => (min lo x, max hi x, if x < 0 then n + 1 else n)) (0, 0, 0)
```

```lean
-- good
def stats (xs : Array Int) : Int × Int × Nat := Id.run do
  let mut lo := 0
  let mut hi := 0
  let mut negatives := 0
  for x in xs do
    lo := min lo x
    hi := max hi x
    if x < 0 then negatives := negatives + 1
  return (lo, hi, negatives)
```

*Source: [FPIL][fpil-mut].*

<a name="effects-modify"></a>
## Updating state

Use `modify` to update state, instead of `get` followed by `set`. You can't set the wrong state by mistake. And no second reference to the state is left behind, so an array in the state can be updated in place.

```lean
-- bad
def bump : StateM Nat Unit := do
  let n ← get
  set (n + 1)
```

```lean
-- good
def bump : StateM Nat Unit := modify (· + 1)
```

*Source: [FPIL][fpil-modify].*

<a name="do-nested-actions"></a>
## Nested actions

Write `(← action)` inline when you use the result once and the line stays short. Bind the result with `let x ← action` when you use it more than once, or when the inline form gets hard to read.

```lean
-- bad
def echo : IO Unit := do
  let stdin ← IO.getStdin
  let line ← stdin.getLine
  IO.print line
```

```lean
-- good
def echo : IO Unit := do
  let line ← (← IO.getStdin).getLine
  IO.print line
```

*Source: [FPIL][fpil-nested].*

<a name="do-return"></a>
## `return` and `pure`

End a `do` block with `return x`. Use `pure x` outside `do` blocks, as in `fun x => pure x`.

*Source: [FRO practice][fro-d].*

---

Previous: [Data modelling](data.md) · [Contents](../README.md#rules) · Next: [Error handling](errors.md)

[cs-do]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#do-notation
[fpil-abbrev-stack]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L337
[fpil-core]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers.lean#L28
[fpil-early]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L151
[fpil-eval]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L213-L216
[fpil-main]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StartingAProject.lean#L40
[fpil-modify]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L434-L476
[fpil-mut]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L653-L656
[fpil-nested]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L67-L85
[fpil-reader]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L201
[fro-d]: ../research/author-survey.md#author-dependent-no-fro-convention
[hs-bracket]: https://hackage.haskell.org/package/base/docs/Control-Exception.html#v:bracket
[lean-io-handle]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/System/IO.lean#L966
[ref-async]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/IO/Async.lean#L34-L36
[ref-cancel]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/IO/Threads.lean#L147
