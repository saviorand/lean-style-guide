# CSLib: Principles and Coding Style

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md (plus `CONTRIBUTING.md`) |
| Author / org | Fabrizio Montesi (file header) / CSLib, under the `leanprover` GitHub org |
| Date / version | `CODESTYLE.md` last changed 2026-10-09, commit `71a06970be8401b2ad6fe3e3fedeca8db97de9ce`; repo HEAD at fetch `530b49b6329ba25a0ae217fe0679aea136e42a37` (2026-10-17) |
| License | Apache-2.0 (`gh api repos/leanprover/cslib/license`; file header repeats "Released under Apache 2.0") |
| Scope & audience | CSLib contributors and reviewers (a Lean library for computer science: transition systems, automata, process calculi, logics) |
| Kind | normative (for CSLib) |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/community/community-cslib-codestyle.md`, `community-cslib-contributing.md` |

## Summary
A 95-line document of principles that explicitly defers to Mathlib: "In the absence of more specific guidelines here, we generally follow the Mathlib style guidelines." It is the closest thing found to a Lean style document from a non-Mathlib, computer-science library, but it concerns library design (API reuse, automation, readable proofs) rather than program-writing style. `CONTRIBUTING.md` adds PR-title prefixes and the linter setup.

## Rules
> Whenever possible, prefer writing definitions (`def`s) directly as terms rather than using `by` blocks. ([Definitions: Terms vs Tactic Mode](https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md#definitions-terms-vs-tactic-mode))

> In general, we want the computational content of definitions to be explicit and reasonably easy to inspect.

> New developments should reuse existing abstractions whenever appropriate. ([API Design](https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md#api-design))

> We consider proof automation an important part of API design in CSLib. ... When developing automation, consider predictability and performance. Not every theorem should be registered for automatic use. ([Automation as an API](https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md#automation-as-an-api))

> Avoid using `simp` in the middle of proofs, unless it is in the `simp only` form. Avoid large terminal `simpa` calls that hide substantial reasoning. ([Proofs](https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md#proofs))

> Feel free to use variable names that make sense in the domain that you are dealing with. For example, in the `LTS` library, `State` is used for types of states and `μ` is used as variable name for transition labels. ([Variable names](https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md#variable-names))

> If you define new notation that in principle can apply to different types ... keep it locally scoped or create a new typeclass. ([Notation](https://github.com/leanprover/cslib/blob/71a06970be8401b2ad6fe3e3fedeca8db97de9ce/CODESTYLE.md#notation))

> Document your definitions and theorems to ease both use and reviewing. When formalising a concept that is explained in a published resource, please reference the resource in your documentation.

`CONTRIBUTING.md`: PR titles must start with `feat|fix|doc|style|refactor|test|chore|perf`; "CSLib uses a number of linters, mostly inherited from Batteries and Mathlib" (syntax linters, `lake lint`, `lake exe lint-style --fix`); all files must import `Cslib.Init` ("sets up some default linting and tactics"); import minimisation by `lake shake`; `lake exe mk_all` ([Linting](https://github.com/leanprover/cslib/blob/530b49b6329ba25a0ae217fe0679aea136e42a37/CONTRIBUTING.md#linting)).

## Reasons given
- Principle 0 ("Guidelines, Not Absolutes"): "Library development is often exploratory ... we do not expect every contribution to arrive with its final, long-term design already worked out."
- Terms over `by` for definitions: computational content should be inspectable.
- Mid-proof `simp`: readability of the logical progression ("Keep the logical progression of a proof visible").

## What transfers to general-purpose Lean
- Evidence that a non-math library (CS, with `Cslib.Init` enabling Mathlib-family linters) adopts Mathlib style wholesale and only adds design principles. Relevant to the question "does any guide target general-purpose Lean": no, this one still defers to Mathlib.
- Transferable principles: prefer term-mode definitions over `by` for computational content; domain variable names allowed (contradicts Mathlib's variable table); locally scoped notation; automation as part of API.
- Not covered: formatting, naming, error handling, effects, tests, docstring form.

## Caveats and unverified items
- I did not read all of `CONTRIBUTING.md` (297 lines), only the style/linting parts.
- `Cslib/Init.lean` and which linter options it actually sets were not inspected (unverified).
