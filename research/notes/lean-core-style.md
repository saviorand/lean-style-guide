# Lean standard library style guide (`doc/std/style.md`)

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md |
| Author / org | Lean FRO / lean4 stdlib maintainer team (per-file authorship not recorded; clone is shallow) |
| Date / version | lean4 commit `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` (2026-10-17), Lean 4.37.0 pre-release |
| License | Apache 2.0 (`LICENSE` at lean4 repo root) |
| Scope & audience | Contributors to the Lean standard library. Self-declared: "this style guide only applies to the Lean standard library" |
| Kind | normative (for the stdlib only) |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/lean-official/lean-core-style.md` |

## Summary
The only official, prescriptive code-formatting guide for Lean 4. It is almost entirely about layout: whitespace, line splitting, indentation of declarations, `where`, `termination_by`, `deriving`, match arms, structure instances, plus short sections on tactic proofs and `do` notation. It says nothing about naming (see `lean-core-naming`), module/API design, error handling, type class design, `partial`, Array vs List, or tests. Two sections flag differences from the Mathlib style ("Note to external contributors"). About half of the examples are theorem statements, not programs.

## Rules
Base URL for links: `https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md`

### Scope
> Note that this style guide only applies to the Lean standard library, even though some examples in the guide are taken from other parts of the Lean code base. ([L11](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L11))

### Whitespace ([L13](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L13))
> Syntactic elements (like `:`, `:=`, `|`, `::`) are surrounded by single spaces, with the exception of `,` and `;`, which are followed by a space but not preceded by one. Delimiters (like `()`, `{}`) do not have spaces on the inside, with the exceptions of subtype notation and structure instance notation.

### Splitting terms ([L37](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L37))
> When splitting a term across multiple lines, increase indentation by two spaces starting from the second line. When splitting a function application, try to split at argument boundaries.

> When splitting at an infix operator, the operator goes at the end of the first line, not at the beginning of the second line.

> When splitting an `if`-`then`-`else` expression, the `then` keyword wants to stay with the condition and the `else` keyword wants to stay with the alternative term.

> Do not orphan parentheses.

No line-length number is stated in this file (the docstring section of `lean-core-doc-style` refers to "the line length limit" without giving it; **unverified** what it is; examples reach ~100 columns).

### File structure ([L121](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L121))
> Every file should start with a copyright header, imports (in the standard library, this always includes a `prelude` declaration) and a module documentation string. There should not be a blank line between the copyright header and the imports. There should be a blank line between the imports and the module documentation string.

> If you explicitly declare universe variables, do so at the top of the file, after the module documentation.

> Syntax that is not supposed to be user-facing must be scoped. New public syntax must always be discussed explicitly in an RFC.

(Stdlib-specific: `prelude`, copyright header. The example shows no `module` keyword, yet `AGENTS.md` at the same commit requires `module` + `prelude`; see `lean-core-contributing`.)

### Declarations ([L148](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L148))
> All top-level commands are unindented. Sectioning commands like `section` and `namespace` do not increase the indentation level.

> Attributes may be placed on the same line as the rest of the command or on a separate line.

> Multi-line declaration headers are indented by four spaces starting from the second line. The colon that indicates the type of a declaration may not be placed at the start of a line or on its own line.

> Declaration bodies are indented by two spaces. Short declaration bodies may be placed on the same line as the declaration type.

### Docstrings ([L179](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L179))
> Declarations should be documented as required by the `docBlame` linter, which may be activated in a file using `set_option linter.missingDocs true` (we allow these to stay in the file).

> Single-line documentation comments should go on the same line as `/--`/`-/`, while multi-line documentation strings should have these delimiters on their own line, with the documentation comment itself unindented.

> Documentation comments must be written in the indicative mood. Use American orthography.

(Flagged as differing from Mathlib. Fuller docstring rules are in `lean-core-doc-style`.)

### `where`, termination, deriving ([L208](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L208), [L228](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L228), [L280](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L280))
> The `where` keyword should be unindented, and all declarations bound by it should be indented with two spaces.

> The `termination_by`, `decreasing_by`, `partial_fixpoint` keywords should be unindented. The associated terms should be indented like declaration bodies.

> The `deriving` clause should be unindented.

(The termination example puts `termination_by`/`decreasing_by` at the indentation of `where` helpers' bodies when inside a `where` function; paraphrase.)

### Notation ([L292](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L292))
> We generally prefer to use notation as available. We usually prefer the Unicode versions of notations over non-Unicode alternatives.

> Sigma types: use `(a : α) × β a` instead of `Σ a, β a` or `Sigma β`.
> Function arrows: use `fun a => f x` instead of `fun x ↦ f x` or `λ x => f x` or any other variant.

### Match arms ([L303](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L303))
> Match arms are indented at the indentation level that the match statement would have if it was on its own line. [...] The content of match arms is indented two spaces, so that it appears on the same level as the match pattern.

> Aligning match arms is allowed, but not required.

### Structures ([L373](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L373), [L420](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L420))
> When using structure instance syntax over multiple lines, the opening brace should go on the preceding line, while the closing brace should go on its own line. The rest of the syntax should be indented by one level. During structure updates, the `with` clause goes on the same line as the opening brace.

> When defining structure types, do not parenthesize structure fields.

> When declaring a structure type with a custom constructor name, put the custom name on its own line, indented like the structure fields, and add a documentation comment.

### Tactic proofs ([L449](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L449))
> Tactic proofs are the most common thing to break during any kind of upgrade, so it is important to write them in a way that minimizes the likelihood of proofs breaking and that makes it easy to debug breakages if they do occur.

> Squeeze non-terminal `simp`s [...]. Squeezing terminal `simp`s is generally discouraged

> Do not over-golf proofs [...]. Do not under-golf proofs: for routine tasks, use the most powerful tactics available.

> Do not use `erw`. Avoid using `rfl` after `simp` or `rw` [...] Use `refine` instead of `refine’`. Use `haveI` and `letI` only if they are actually required.

> Prefer highly automated tactics (like `grind` and `omega`) over low-level proofs, unless the automated tactic requires unacceptable additional imports or has bad performance. If you decide against using a highly automated tactic, leave a comment explaining the decision.

### `do` notation ([L467](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L467))
> The `do` keyword goes on the same line as the corresponding `:=` (or `=>`, or similar). `Id.run do` should be treated as if it was a bare `do`.

> Use early `return` statements to reduce nesting depth and make the non-exceptional control flow of a function easier to see.

> Alternatives for `let` matches may be placed in the same line or in the next line, indented by two spaces.

Examples show `let some decl ← findFunDecl? fvarId | throwError "..."`, `let mut`, `for ... in`, and `Id.run do` with `let mut` (implicit idioms; paraphrase).

## Reasons given
- Whole-guide: formatting "reflects the same level of precision and care required to meet the deeper standards of the Lean 4 standard library"; consistent formatting "is much easier for others to read and maintain" ([intro](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#L1-L9)).
- Tactic proofs: robustness under upgrades and ease of debugging (quoted above).
- Early `return`: reduces nesting depth, makes non-exceptional control flow easier to see.
- Almost every formatting rule gives no reason (stated as prescriptions).

## What transfers to general-purpose Lean
- Whitespace, line-splitting, indentation, `where`/`termination_by`/`deriving` placement, match-arm layout, structure-instance layout: all syntax-level and apply to any Lean code.
- Unicode/`fun a =>` notation rules apply broadly.
- `do` notation guidance (early return, `let some x ← e | alt`) is the only program-level guidance and is general.
- Does not transfer: `prelude`, copyright header, `docBlame` enforcement, RFC for public syntax, theorem-heavy examples, `simp`/`grind` rules (proof-oriented).

## Caveats and unverified items
- The guide declares itself stdlib-only; its use outside the stdlib is a community choice.
- Says nothing on line length, naming, API design, `partial`, `Array` vs `List`, error handling, type classes, tests.
- Authorship/change history unavailable (shallow clone).
