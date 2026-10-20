# Zulip: naming conventions (Lean 3 to Lean 4 casing, program vs theorem names)

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/archive/ (threads cited individually) |
| Author / org | Lean Zulip participants |
| Date / version | Threads 2021-01-08 to 2023-09; archive clone `63dc76b4eb239e7814eb5e0cb421cb731b507301` (2026-10-02) |
| License | none stated for archive repo; messages remain authors' |
| Scope & audience | Mathlib/Lean core/Std participants |
| Kind | descriptive (history of decisions) |
| Lean version | Lean 3 flagged where relevant; mostly Lean 4 |
| Raw copy | `vendor/repos/zulip-archive/zulip_json/<stream>/<topic>.json` |

## Summary
The Lean 4 casing scheme was decided between 2021 and 2022 while porting Mathlib: Lean 4 core already used `lowerCamelCase`/`UpperCamelCase`, Mathlib 3 used `snake_case` everywhere, and the community settled on "follow Lean + core lib with definitions, but keep underscores in lemma names". The rules were then "codified by mathport" (the porting tool), and the Mathlib naming page was rewritten to match. I found no dedicated Zulip thread on the program-API suffixes `get?`/`get!`/`getD`; they surface only in passing. The programs-vs-theorems split is a direct result of this history, not of a separate decision about programs.

## Threads
- [what naming scheme to use in mathlib4 (lean4, 2021-01-08)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/what.20naming.20scheme.20to.20use.20in.20mathlib4.html): Kenny Lau starts a poll "camelCase and PascalCase / snake_case". Patrick Massot: "I would say we should follow Lean + core lib with definitions, but keep underscores in lemma names." Sebastian Ullrich says that is what he suggested the previous year. Heather Macbeth raises the `group`/`Group` clash from category theory. (Lean 3 mathlib context; poll results are an image, not in the archive text.) The same topic gains a 2022-08-27 tail: David Renshaw: "defs, namespaces, structures get capital camelcase. Theorems and lemmas get snake_case. Current conventions are codified by mathport". Michael Jam finds `List.Mem` vs `List.mem_...` confusing and "kind of dislike[s] that convention".
- [naming conventions (mathlib4, 2022-10-21, 301 messages)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/naming.20conventions.html): the working thread during the port. Mario Carneiro (2022-10-24): "the way I've been leaning toward combining our snake-casing theorem convention with capitalized definition names is to lowercase the definitions without going full snake case so that name components stay together ... liftRel_subrelation_lex." Also: "Name components in a theorem would only stay capitalized when this is needed to work around a name conflict, as in And_assoc". Jannis Limperg objects that so many exceptions suggest the convention is poor. Mario also notes coercion lemma names must no longer mention `coe` because "coercions are now unfolded at elaboration time" (a Lean 3 to 4 difference).
- [naming conventions: natCast vs nat_cast (mathlib4, 2023-03-17)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/naming.20conventions.3A.20natCast.20vs.20nat_cast.html): shows the unsettled corner of rule 5 -- how a dotted name such as `Nat.cast` appears inside a snake_case lemma name (`natCast` vs `nat_cast`); resolved in favor of `natCast` (current naming page example `map_natCast`, `Int.cast_natCast`).
- [Option.get! (lean4, 2021-12-19)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Option.2Eget!.html): about proving things with `panic!`-based `get!`; Marc Huisinga: "Ideally, in proofs, you ensure that the panic! case never occurs via preconditions"; the asker chooses `getD`. This is the only place I found `get!` and `getD` weighed against each other, and it is advice on usage, not on naming.
- [List.get? vs [_]? notation (new-members, 2023-08-08)](https://leanprover-community.github.io/archive/stream/113489-new-members/topic/List.2Eget.3F.20vs.20.5B_.5D.3F.20notation.html): Alex J. Best: "I suppose the intention is that you use get? more than getElem" (a guess, in 2023).
- Names for program-ish things: [Naming Question [RFC?] (lean4, 2022-07-01)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Naming.20Question.20.5BRFC.3F.5D.html) (Lake artifact naming), [[RFC] Attribute naming convention (2022-08-06)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/.5BRFC.5D.20Attribute.20naming.20convention.html), [tactic naming convention (2021-09-16)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/tactic.20naming.20convention.html) -- topic titles found by search, **bodies not read**.
- Lean 3 era threads, for provenance only: [naming conventions (general, 2018-09-14)](https://leanprover-community.github.io/archive/stream/113488-general/topic/naming.20conventions.html), [Noun/adjective/verb naming conventions for defs in mathlib (2020-08-12)](https://leanprover-community.github.io/archive/stream/113488-general/topic/Noun.2Fadjective.2Fverb.20naming.20conventions.20for.20defs.20in.20mathlib.html) and [naming defs (2022-02-09)](https://leanprover-community.github.io/archive/stream/113488-general/topic/naming.20defs.html). **Lean 3**; not read in detail.
- Primary document for the decision: [Mathlib4 Porting wiki, Naming convention](https://github.com/leanprover-community/mathlib4/wiki/Porting-wiki#naming-convention) (saved: `vendor/pages/community/mathlib-porting-wiki.md`), also reproduced in the [Lean 4 survival guide for Lean 3 users](https://github.com/leanprover-community/mathlib4/wiki/Lean-4-survival-guide-for-Lean-3-users) (saved: `mathlib-lean3-survival.md`), which also records "Function notation changed from `λ x, f x` to `fun x => f x` or `λ x => f x` or `fun x ↦ f x` or `λ x ↦ f x`".

## Rules
None in this note beyond those in `notes/mathlib-naming.md`; the threads record that they were decided by tool-assisted convention rather than a vote on programming-style principles.

## Reasons given
- Keep underscores in lemma names but camelCase in definitions: alignment with Lean core for definitions (Massot 2021) and readability of theorem names as sentences (see `notes/mathlib-naming.md`).
- Lowercasing definition components inside theorem names without snake-casing them "so that name components stay together" (Carneiro 2022).
- Objection recorded: many exceptions (`And_assoc`, intervals `Icc`) suggest the scheme is awkward (Limperg 2022; Jam 2022).

## What transfers to general-purpose Lean
- The casing scheme is a historical compromise between Lean-core code and Mathlib's snake_case; for a programs guide the question is only whether proof names inside program libraries follow the same scheme (they do in Lean core and Batteries).
- Edge cases a guide must settle if it names theorems about programs: how a dotted or camelCase function name appears in a lemma name (rule 5, `natCast`), conflicts requiring capitalised components.
- Nothing on program-variant suffixes; the guide cannot cite community deliberation for `?`/`!`/`D` -- only Lean core's `naming.md`.

## Caveats and unverified items
- Poll results and some quoted Zulip images were not recoverable.
- The `#naming and dot notation` (2021-07-19, 37 messages) and `Naming: eval vs apply` (2021-01-24) threads were not read.
- I did not read the full 301-message thread; quotes come from the first ~20 messages.
