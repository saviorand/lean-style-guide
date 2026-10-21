# Source code layout

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="layout-file"></a>
## File structure

Order each file like this:

1. a licence or copyright comment, if your project uses one;
2. `module`, if you use the module system (see [Modules](api.md#api-modules));
3. the imports;
4. a module docstring, `/-! … -/`, that says what the file is for;
5. the code.

Put a blank line between the imports and the module docstring.

```lean
module

public import Std.Data.HashMap

/-!
# Word counts

Counts how often each word occurs in a text.
-/

public section

/-- Returns how often each space-separated word occurs in `text`. -/
def wordCounts (text : String) : Std.HashMap String Nat :=
  (text.splitOn " ").foldl (fun counts w => counts.insert w (counts.getD w 0 + 1)) {}

end
```

*Sources: [Lean core style][cs-file], [Mathlib documentation][ml-doc].*

<a name="layout-indentation"></a>
## Indentation

Indent with two spaces, never with tabs. Nested blocks, declaration bodies and continuation lines go two spaces further in than the line they belong to.

```lean
-- bad
def describe (n : Nat) : String :=
    if n == 0 then
        "none"
    else
        "some"
```

```lean
-- good
def describe (n : Nat) : String :=
  if n == 0 then
    "none"
  else
    "some"
```

*Sources: [Lean core style][cs-decl], [FRO practice][fro-c].*

<a name="layout-line-length"></a>
## Line length

Keep lines under 100 characters. A long string literal or URL can run over.

*Sources: [Mathlib style][ml-line], [FRO practice][fro-c].*

<a name="layout-spaces"></a>
## Spaces

Put single spaces around `:`, `:=`, `|`, `::`, `=>`, `←` and infix operators. Put a space after a comma but not before it. Don't put spaces just inside parentheses or brackets. Structure instances and subtypes are the exception, and are written `{ x := 1 }` and `{ n : Nat // n > 0 }`.

```lean
-- bad
def scale (k:Nat) (p:Nat × Nat):Nat × Nat:=( k*p.1 , k*p.2 )
```

```lean
-- good
def scale (k : Nat) (p : Nat × Nat) : Nat × Nat := (k * p.1, k * p.2)
```

*Source: [Lean core style][cs-ws].*

<a name="layout-top-level"></a>
## Top-level declarations

Start every top-level command at column 0. `namespace` and `section` don't add indentation. Separate declarations with one blank line.

```lean
-- bad
namespace Shape
  def unitSquare : Nat × Nat := (1, 1)
  def unitCube : Nat × Nat × Nat := (1, 1, 1)
end Shape
```

```lean
-- good
namespace Shape

def unitSquare : Nat × Nat := (1, 1)

def unitCube : Nat × Nat × Nat := (1, 1, 1)

end Shape
```

*Source: [Lean core style][cs-decl].*

<a name="layout-headers"></a>
## Long declaration headers

If a declaration's header doesn't fit on one line, indent its continuation lines by four spaces, which sets them apart from the body. Don't start a line with the colon before the result type.

```lean
-- bad
def joinRows (rows : Array (Array String)) (cellSeparator : String)
  (rowSeparator : String)
  : String :=
  rowSeparator.intercalate (rows.map fun row => cellSeparator.intercalate row.toList).toList
```

```lean
-- good
def joinRows (rows : Array (Array String)) (cellSeparator : String)
    (rowSeparator : String) : String :=
  rowSeparator.intercalate (rows.map fun row => cellSeparator.intercalate row.toList).toList
```

*Sources: [Lean core style][cs-decl], [FRO practice][fro-c].*

<a name="layout-splitting"></a>
## Splitting long expressions

Split a long expression at argument boundaries, and indent the following lines by two more spaces. If you split at an infix operator, leave the operator at the end of the first line. Keep `then` on the line with its condition and `else` with its branch. Don't leave a closing parenthesis on a line by itself.

```lean
-- bad
def total (prices : List Nat) (shipping tax : Nat) : Nat :=
  prices.foldl (· + ·) 0
  + shipping
  + tax
```

```lean
-- good
def total (prices : List Nat) (shipping tax : Nat) : Nat :=
  prices.foldl (· + ·) 0 +
    shipping + tax
```

*Source: [Lean core style][cs-split].*

<a name="layout-match"></a>
## Match arms

Put each `|` of a `match` at the column where the `match` would start on its own line. In a definition by pattern matching, indent the arms by two spaces. Don't pad patterns to line up the `=>` arrows, because renaming one pattern then changes every line.

```lean
-- bad
def label (n : Nat) : String :=
  match n with
    | 0     => "zero"
    | 1     => "one"
    | _     => "many"
```

```lean
-- good
def label (n : Nat) : String :=
  match n with
  | 0 => "zero"
  | 1 => "one"
  | _ => "many"

def isZero : Nat → Bool
  | 0 => true
  | _ => false
```

*Sources: [Lean core style][cs-match], [FRO practice][fro-c], [OCaml guidelines][ocaml].*

<a name="layout-where"></a>
## `where`, `deriving` and termination clauses

Start `where`, `deriving`, `termination_by` and `decreasing_by` at the column of the declaration they belong to. Indent what follows them by two spaces.

```lean
-- good
structure Point where
  x : Float
  y : Float
deriving Repr

def countdown (n : Nat) : List Nat := go n []
where
  go : Nat → List Nat → List Nat
    | 0, acc => (0 :: acc).reverse
    | i + 1, acc => go i ((i + 1) :: acc)
```

*Sources: Lean core style on [`where`][cs-where], [termination][cs-term] and [`deriving`][cs-deriving].*

<a name="layout-structure-instances"></a>
## Structure instances

When a structure instance spans several lines, put `{` at the end of the line before it and `}` on a line of its own. Put one field on each line, indented by two spaces. In an update, keep `with` on the line with `{`.

```lean
structure Config where
  host : String
  port : Nat
  verbose : Bool

-- bad
def devConfig : Config :=
  { host := "localhost",
    port := 8080,
    verbose := true }
```

```lean
structure Config where
  host : String
  port : Nat
  verbose : Bool

-- good
def devConfig : Config := {
  host := "localhost"
  port := 8080
  verbose := true
}

def quietConfig : Config := { devConfig with
  verbose := false
}
```

*Source: [Lean core style][cs-struct].*

<a name="layout-do"></a>
## `do` blocks

Put `do` on the same line as the `:=`, `=>` or `←` before it. Write one statement per line, all at the same indentation, without braces or semicolons. Treat `Id.run do` like a bare `do`.

```lean
-- bad
def greet (name : String) : IO Unit :=
  do { IO.println s!"Hello, {name}"; IO.println "Welcome" }
```

```lean
-- good
def greet (name : String) : IO Unit := do
  IO.println s!"Hello, {name}"
  IO.println "Welcome"
```

*Sources: [Lean core style][cs-do], [FPIL][fpil-do-lines].*

---

Previous: [Projects and tooling](projects.md) · [Contents](../README.md#rules)


[cs-decl]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#top-level-commands-and-declarations
[cs-deriving]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#deriving
[cs-do]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#do-notation
[cs-file]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#basic-file-structure
[cs-match]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#pattern-matching-induction-etc
[cs-split]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#splitting-terms-across-multiple-lines
[cs-struct]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#structures
[cs-term]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#termination-arguments
[cs-where]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#where-clauses
[cs-ws]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#basic-whitespace-rules
[fpil-do-lines]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L140-L181
[fro-c]: ../research/author-survey.md#consistent-across-authors
[ml-doc]: https://leanprover-community.github.io/contribute/doc.html
[ml-line]: https://leanprover-community.github.io/contribute/style.html#line-length
[ocaml]: https://ocaml.org/docs/guidelines
