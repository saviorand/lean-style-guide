# Metaprogramming in Lean 4 (community book)

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/lean4-metaprogramming-book/ (source: https://github.com/leanprover-community/lean4-metaprogramming-book/tree/9bb0918b272015ad6e39e6db6220fec378a35d8a) |
| Author / org | leanprover-community contributors (repo created 2022-03-23; 316★) |
| Date / version | `9bb0918` (2026-10-15) |
| License | Apache-2.0 (`LICENSE` in repo) |
| Scope & audience | Lean users learning macros, elaborators, `MetaM` and tactics |
| Kind | descriptive (tutorial) with a few rules of thumb |
| Lean version | Lean 4 |
| Raw copy | source clone `vendor/repos/mpbook` |

## Summary
A tutorial on syntax, macros, elaboration, `MetaM` and tactic writing. I grepped it for advice words (should, prefer, recommend, idiomatic, avoid, style) and got 56 hits. Most describe internals, such as `mkAppM` versus `mkAppN`, which are out of scope for application code. Two of its rules of thumb come with reasons and apply to any library that defines notation.

## Rules
Base: `https://github.com/leanprover-community/lean4-metaprogramming-book/blob/9bb0918b272015ad6e39e6db6220fec378a35d8a/lean/main/`.

### Macro or elaborator
> the rule of thumb here is to only use `macro`s when the conversion is simple and truly feels elementary to the point of aliasing. As Henrik Böving puts it: "as soon as types or control flow is involved a macro is probably not reasonable anymore" ([02_overview.lean L153-L155](https://github.com/leanprover-community/lean4-metaprogramming-book/blob/9bb0918b272015ad6e39e6db6220fec378a35d8a/lean/main/02_overview.lean#L153-L155), citing a Zulip thread)

> So - use `macro`s for creating syntax sugars, notations, and shortcuts, and prefer `elab`s for writing out code with some programming logic, even if it's potentially implementable in a `macro`. (same file, L155)

### Overlapping `macro_rules`
> This capability is obviously *very* powerful! It should not be used lightly and without careful thinking since it can introduce weird behaviour while writing code later on. ([06_macros.lean L57-L59](https://github.com/leanprover-community/lean4-metaprogramming-book/blob/9bb0918b272015ad6e39e6db6220fec378a35d8a/lean/main/06_macros.lean#L57-L59))

The example is a second `macro_rules` for `LXOR` that matches only some inputs: `true LXOR true` uses the new rule, while `foo LXOR foo` silently falls back to the old one. The book says this "will be very confusing to whoever might be debugging an issue" (L72), and that macros are for "simple syntax to syntax translations" (L75-L78).

### Hygiene
Explained as semantics, not as advice (06_macros.lean, from L297): why `$e` cannot capture names, and how macro scopes avoid clashes.

## Reasons given
Debuggability: a reader cannot tell which rule fired. Fitness for purpose: logic that involves types or control flow belongs in an elaborator.

## What transfers to general-purpose Lean
- Source material for a short "Macros and notation" chapter: macros for pure syntax-to-syntax sugar; elaborators once types or control flow are involved; no partial overlapping `macro_rules` on existing syntax.
- Combine with core-style (an RFC for new public syntax; scoped syntax unless it must be public) and with the Reference's "Syntax extensions should be used in _output_ as well as in _input_" ([lean-reference](lean-reference.md#notation-and-ffi-read-2026-10-20)).
- Everything about `MetaM`, `Expr` and tactic internals is out of scope for a software style guide.

## Caveats and unverified items
- Only the advice-word lines and the two passages above were read. The rest of the book was not.
- The Böving quote is second-hand, from the book; the Zulip original was not opened.
