# Functions

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="functions-signatures"></a>
## Type signatures

Give every top-level definition explicit argument types and an explicit result type. The type tells the reader what the function does and keeps type errors close to the mistake.

```lean
-- bad
def area (width height : Nat) := width * height
```

```lean
-- good
def area (width height : Nat) : Nat := width * height
```

*Sources: [FPIL][fpil-annot], [Google Haskell guide][google-types].*

<a name="functions-implicit"></a>
## Implicit arguments

Make an argument implicit, with braces, when later arguments determine it. That's usually true of type arguments.

```lean
-- bad
def firstOr (α : Type) (xs : List α) (fallback : α) : α := xs.headD fallback

def first := firstOr Nat [1, 2, 3] 0
```

```lean
-- good
def firstOr {α : Type} (xs : List α) (fallback : α) : α := xs.headD fallback

def first := firstOr [1, 2, 3] 0
```

*Source: [FPIL][fpil-implicit].*

<a name="functions-auto-implicit"></a>
## Automatic implicit arguments

Turn off `autoImplicit` (see [Lean options](projects.md#project-options)). By default, Lean turns every unknown name in a signature into a new implicit argument, so a misspelled type name compiles and means something else.

```lean
structure Item where
  price : Nat

-- bad: `Iten` is a typo, and Lean makes it a type variable
def count (items : List Iten) : Nat := items.length
```

```lean
set_option autoImplicit false

structure Item where
  price : Nat

-- good: the typo would be an error, and type variables are declared
def count {α : Type} (items : List α) : Nat := items.length

def totalPrice (items : List Item) : Nat := items.foldl (· + ·.price) 0
```

*Sources: [Mathlib configuration][ml-autoimplicit], [checked with Lean 4.35][checked].*

<a name="functions-size"></a>
## Function size

Keep each function short enough to read at once. If a function does two jobs, such as parsing input and computing a result, split it in two.

*Source: [FPIL][fpil-concerns].*

<a name="functions-helpers"></a>
## Local helpers

Put a helper that only one function uses in a `where` clause after that function, and name a recursive helper `go`. A `where` helper can use the parameters of the function it belongs to. Use `let rec` only when the helper needs a local variable from inside the body.

```lean
-- bad
def sumSquaresAux : List Nat → Nat → Nat
  | [], acc => acc
  | x :: xs, acc => sumSquaresAux xs (acc + x * x)

def sumSquares (xs : List Nat) : Nat := sumSquaresAux xs 0
```

```lean
-- good
def sumSquares (xs : List Nat) : Nat := go xs 0
where
  go : List Nat → Nat → Nat
    | [], acc => acc
    | x :: xs, acc => go xs (acc + x * x)
```

*Source: [FRO practice][fro-c].*

<a name="functions-options"></a>
## Many parameters

If a function takes more than about four parameters, or several of the same type, group them in a structure with default values. Callers then name each value and leave out the ones they don't change. The standard library's `IO.Process.spawn` takes its arguments this way.

```lean
-- bad
def connect (host : String) (port timeoutMs retries : Nat) (useTls : Bool) : String :=
  s!"{host}:{port} timeout={timeoutMs} retries={retries} tls={useTls}"

def localConnection := connect "localhost" 5432 5000 3 false
```

```lean
-- good
structure ConnectOptions where
  host : String
  port : Nat := 5432
  timeoutMs : Nat := 5000
  retries : Nat := 3
  useTls : Bool := true

def connect (opts : ConnectOptions) : String :=
  s!"{opts.host}:{opts.port} timeout={opts.timeoutMs} retries={opts.retries} tls={opts.useTls}"

def localConnection := connect { host := "localhost", useTls := false }
```

*Source: [standard library][std-spawnargs].*

<a name="functions-bool-args"></a>
## Boolean arguments

Pass a `Bool` argument by name, as in `(lastFirst := true)`, because a bare `true` doesn't say what it switches on. If most callers want the same value, make it the parameter's default. Lake works this way: its `proc` function takes `(quiet := false)`, and callers that want no output write `(quiet := true)`.

```lean
-- bad
def formatName (first last : String) (lastFirst : Bool) : String :=
  if lastFirst then s!"{last}, {first}" else s!"{first} {last}"

def label := formatName "Ada" "Lovelace" true
```

```lean
-- good
def formatName (first last : String) (lastFirst : Bool := false) : String :=
  if lastFirst then s!"{last}, {first}" else s!"{first} {last}"

def label := formatName "Ada" "Lovelace" (lastFirst := true)
```

*Sources: [Lake's `proc`][lake-proc], [measured in Std and Lake][checked].*

<a name="functions-exhaustive"></a>
## Exhaustive matches

When you match on a type you control, list every constructor rather than ending with `_`. If someone adds a constructor later, Lean then reports every match that needs to handle it.

```lean
inductive Shape where
  | circle (radius : Float)
  | square (side : Float)
  | triangle (base height : Float)

-- bad
def Shape.isRound : Shape → Bool
  | .circle _ => true
  | _ => false
```

```lean
inductive Shape where
  | circle (radius : Float)
  | square (side : Float)
  | triangle (base height : Float)

-- good
def Shape.isRound : Shape → Bool
  | .circle _ => true
  | .square _ | .triangle _ _ => false
```

*Source: [OCaml guidelines][ocaml-match].*

<a name="functions-pipelines"></a>
## Pipelines

Use `|>` when a value goes through several steps in order, and `|>.` to continue with a method call. Use `<|` to avoid parentheses around a last argument. Don't use `$`.

```lean
-- bad
def report (words : List String) : String :=
  String.intercalate ", " (List.map String.toUpper (List.filter (fun w => w.length > 3) words))
```

```lean
-- good
def report (words : List String) : String :=
  words.filter (·.length > 3) |>.map String.toUpper |> ", ".intercalate
```

*Sources: [FPIL][fpil-pipe], [Mathlib style][ml-delims].*

<a name="functions-lambdas"></a>
## Lambdas

Write lambdas as `fun x => e`. Don't use `λ` or `↦`. For very simple lambdas, use the `·` shorthand, so `(· + 1)` means `fun x => x + 1`.

```lean
-- bad
def incrementAll (xs : List Nat) : List Nat := xs.map (λ x ↦ x + 1)
```

```lean
-- good
def incrementAll (xs : List Nat) : List Nat := xs.map (· + 1)

def names (people : List (String × Nat)) : List String := people.map fun (name, _) => name
```

*Sources: [Lean core style][cs-notation], [FPIL][fpil-fun], [FRO practice][fro-c].*

---

Previous: [Naming](naming.md) · [Contents](../README.md#rules) · Next: [Type classes and instances](classes.md)

[checked]: ../research/decisions.md#facts-checked-while-drafting
[cs-notation]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#notation-and-unicode
[fpil-annot]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L238-L246
[fpil-concerns]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L111-L113
[fpil-fun]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L511-L553
[fpil-implicit]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L288
[fpil-pipe]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L25-L38
[fro-c]: ../research/author-survey.md#consistent-across-authors
[google-types]: https://google.github.io/styleguide/haskellguide.html#type-declarations
[lake-proc]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Util/Proc.lean#L38-L40
[ml-autoimplicit]: https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/lakefile.lean#L44
[ml-delims]: https://leanprover-community.github.io/contribute/style.html#whitespace-and-delimiters
[ocaml-match]: https://ocaml.org/docs/guidelines#pattern-matching-warnings
[std-spawnargs]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/System/IO.lean#L1434-L1455
