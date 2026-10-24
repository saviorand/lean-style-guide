# Documentation

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="docs-when"></a>
## When to write a docstring

Write a docstring when the name and type leave something unsaid, such as a unit, what happens at an edge case, or what `none` means when it can mean more than one thing. Don't write one that only restates the name and type. It tells the reader nothing new and goes stale when the code changes. This is looser than Lean's standard library and Batteries, which document every public declaration and turn on `linter.missingDocs`.

```lean
-- bad
/-- The client configuration. -/
structure ClientConfig where
  /-- The base URL. -/
  baseUrl : String
  /-- The number of retries. -/
  retries : Nat := 3
```

```lean
-- good
structure ClientConfig where
  /-- The base URL that relative paths are resolved against. -/
  baseUrl : String
  /-- Extra attempts after the first one fails, so `0` means a single attempt. -/
  retries : Nat := 3
```

*Sources: [Paul Butcher, issue #1][issue-1], [lean4 `AGENTS.md`][agents-comments]; for the stricter practice, [Lean core style][cs-docs] and [Batteries configuration][batteries-docs].*
<a name="docs-module"></a>
## Module docstrings

Begin a file with a module docstring when the file needs an explanation that its code doesn't give, such as how its parts fit together or why it exists. Give it a `#` title, as in the [file structure](layout.md#layout-file) example. Don't add one that only repeats the file name.

*Sources: [Paul Butcher, issue #1][issue-1], [Mathlib documentation][ml-doc].*
<a name="docs-summary"></a>
## The first sentence

Start a docstring with one sentence that says what the declaration does or is. For a function, start with a verb in the third person, such as "Returns" or "Parses". For a type or a constant, start with a noun phrase. Write code, names and values in backticks, and refer to arguments by name.

```lean
-- bad
/-- This function will return the display name of the user. -/
def displayName (first last : String) : String := s!"{first} {last}"
```

```lean
-- good
/-- Returns the name shown in the interface: `first`, a space, then `last`. -/
def displayName (first last : String) : String := s!"{first} {last}"
```

*Sources: [Lean documentation style][ds-constants], [Lean core style][cs-docs].*

<a name="docs-examples"></a>
## Examples

Show how to use the main functions of a library with a short example in the docstring. Check each example in a test with [`#guard_msgs`](testing.md#tests-guard-msgs), so it stays correct.

*Sources: [Rust API guidelines][rust-example], [FPIL][fpil-examples].*

<a name="docs-layout"></a>
## Docstring layout

Put a one-line docstring on the same line as `/--` and `-/`. In a longer docstring, put `/--` and `-/` on lines of their own and don't indent the text.

```lean
-- good
/-- Returns `true` if `s` contains only spaces. -/
def isBlank (s : String) : Bool := s.all (· == ' ')

/--
Splits `text` into lines and drops the empty ones.

Lines are split at `\n`, so a Windows line ending leaves a `\r` at the end of each line.
-/
def nonEmptyLines (text : String) : List String := (text.splitOn "\n").filter (· != "")
```

*Source: [Lean core style][cs-docs].*

---

Previous: [Testing](testing.md) · [Contents](../README.md#rules) · Next: [Comments](comments.md)

[agents-comments]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md?plain=1#L75-L83
[batteries-docs]: https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/lakefile.toml#L7
[cs-docs]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#documentation-comments
[ds-constants]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#constants
[fpil-examples]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L111
[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
[ml-doc]: https://leanprover-community.github.io/contribute/doc.html
[rust-example]: https://rust-lang.github.io/api-guidelines/documentation.html#c-example
