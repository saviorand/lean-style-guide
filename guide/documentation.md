# Documentation

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="docs-public"></a>
## Docstrings on public declarations

Give every public declaration in a library a docstring, written `/-- … -/` just before it. Turn on `linter.missingDocs` to find the ones you missed. In an application, document whatever isn't obvious from the name and type.

```lean
set_option linter.missingDocs true

-- good
/-- Settings for the HTTP client. -/
structure ClientConfig where
  /-- The base URL that relative paths are resolved against. -/
  baseUrl : String
  /-- How long to wait for a response, in milliseconds. -/
  timeoutMs : Nat := 5000
```

*Sources: [Lean core style][cs-docs], [Batteries configuration][batteries-docs], [Google Haskell guide][google-haddock].*

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

<a name="docs-examples"></a>
## Examples

Show how to use the main functions of a library with a short example in the docstring. Check each example in a test with [`#guard_msgs`](testing.md#tests-guard-msgs), so it stays correct.

*Sources: [Rust API guidelines][rust-example], [FPIL][fpil-examples].*

<a name="docs-module"></a>
## Module docstrings

Begin every file with a module docstring that has a `#` title and says what the file is for, as in the [file structure](layout.md#layout-file) example.

*Source: [Mathlib documentation][ml-doc].*

---

Previous: [Comments](comments.md) · [Contents](../README.md#rules) · Next: [Testing](testing.md)

[batteries-docs]: https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/lakefile.toml#L7
[cs-docs]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#documentation-comments
[ds-constants]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#constants
[fpil-examples]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L111
[google-haddock]: https://google.github.io/styleguide/haskellguide.html#haddock
[ml-doc]: https://leanprover-community.github.io/contribute/doc.html
[rust-example]: https://rust-lang.github.io/api-guidelines/documentation.html#c-example
