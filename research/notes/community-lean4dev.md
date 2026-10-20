# lean4.dev "Best Practices - Writing Idiomatic Lean 4 Code"

| Field | Value |
|---|---|
| URL | https://lean4.dev/language/best-practices |
| Author / org | "Lean 4 Dev Editorial Team" (anonymous site publisher; `<meta name="author">`); not affiliated with the Lean FRO as far as the page shows (unverified) |
| Date / version | undated; fetched 2026-10-17 |
| License | none stated (looked at page source for author/publisher only; no licence found) |
| Scope & audience | Learners writing Lean 4 programs |
| Kind | community advice (secondary source) |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/community/community-lean4dev-best-practices.md` |

## Summary
A 123-line page that claims to describe "the conventions the Lean community follows for naming, layout and style, so that your code reads like the standard library and Mathlib". It restates casing rules, theorem-name vocabulary, suffix meanings, explicit types on top-level signatures, `do` notation, avoiding `partial`, structure-vs-class and pattern-matching tips. It is the only web page found that aims at programs, but it is anonymous, undated, cites no sources, and contains at least one error, so it should be treated as a lead, not evidence.

## Rules
> Suffix conventions worth knowing: `'` marks a variant of an existing lemma (`add_comm'`); `?` marks a function returning `Option` (`head?`); `!` marks one that panics (`head!`); and `D` marks one taking a default (`getD`). ([Naming Theorems](https://lean4.dev/language/best-practices))

> Do Type: Top-level function signatures (always!), Structure fields, Ambiguous literals ... Don't Type: Local variables where type is obvious; Match arms where patterns imply types.

> Use `do` notation for monadic code (`IO`, `Option`, etc.). Avoid raw `bind` (`>>=`) operators unless the pipeline is very short (1-2 steps).

> Avoid `partial` unless absolutely necessary. `partial` functions cannot be used in proofs and can hide infinite loops. Try to use structural recursion or `termination_by` first.

> Before writing a helper function, check `List`, `Array`, and `String` namespaces.

Casing: UpperCamelCase types/structures/classes/namespaces/modules; lowerCamelCase functions/definitions/locals; snake_case theorems ("not legacy: it is current practice in both Lean core and Mathlib").

## Reasons given
Short, informal: readability ("a reader cannot see what [inference] inferred"), `partial` blocks proofs, theorem names "are read as sentences".

## What transfers to general-purpose Lean
- The topics it lists (explicit top-level types, `do` over `>>=`, `partial` avoidance, structure vs class) are program-style questions Mathlib's guide ignores; they are candidates for the guide's topic list, to be sourced from primary material.
- The suffix list matches Lean core `doc/std/naming.md` line 69 for `?`/`!`; the `D` and `'` meanings are not verified against a primary source here.

## Caveats and unverified items
- Secondary and anonymous; do not cite as a primary source.
- Contains a muddled claim: the pattern-matching section says "Prefer the dot syntax `match x with` or the function match shorthand", but `match x with` is not dot syntax; reason to doubt other claims. Its comment that `def add' x y := x + y` "does not even compile" is the page's own remark; not tested here.
- Two search-result near-misses: "Write Lean Code" (cboone/agent-harness-plugins, an AI-agent skill derived from Mathlib docs) and `solana-foundation/leanprover-solanalib` `skills/lean-best-practices/SKILL.md` (URL returned 404 at fetch). Both are derivative of Mathlib, not original guidance.
