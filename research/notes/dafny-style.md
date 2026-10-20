# Dafny style guide

| Field | Value |
|---|---|
| URL | https://dafny.org/dafny/StyleGuide/Style-Guide (source: https://github.com/dafny-lang/dafny/blob/b6966c8d9e00e0665bb979ccab4926888963df02/docs/StyleGuide/Style-Guide.md) |
| Author / org | Dafny team / community (Microsoft Research origin; the repo is dafny-lang) |
| Date / version | source file last changed in commit `b6966c8d9e00e0665bb979ccab4926888963df02`, 2024-02-22 |
| License | MIT ("MIT License", Copyright (c) Microsoft Corporation, `LICENSE.txt`; `vendor/pages/proof-assistants/dafny-LICENSE`). GitHub API reports NOASSERTION. |
| Scope & audience | Dafny programmers (verification-aware imperative/functional language) |
| Kind | community advice ("still in progress. Please feel free to add more suggestions") |
| Lean version | n/a (Dafny) |
| Raw copy | `vendor/pages/proof-assistants/dafny-style.md` (defuddle) and `dafny-style.html` |

## Summary
A short guide on naming, braces, imports, layout and a handful of content conventions. Of interest for Lean: lemma and function naming, "predicates not Bool functions", "make the base case of inductive proofs explicit", dependency ordering in a file, and a list of questions to ask before designing a program. It says nothing on how much to verify.

## Rules
Naming:
> Any **lemmas**, **predicates**, **functions**, **methods**, **classes**, **modules**, **datatypes**, and **newtypes** are named with `PascalCase`.
([Naming Convention](https://github.com/dafny-lang/dafny/blob/b6966c8d9e00e0665bb979ccab4926888963df02/docs/StyleGuide/Style-Guide.md))

Avoid redundant names: name the method `ToString` so that the call is `Integer.ToString(i)` rather than `Integer.IntegerToString(i)` ("Method Prefix").

Order:
> Functions, predicates, and methods within a file should be sorted topologically, meaning that everything `method M` depends on should be above `M` in the file.
("Order")

Predicates:
> Predicates should be used instead of functions that return a `bool` value.
("Predicates")

Lemmas:
> When writing inductive proofs, contributors are strongly encouraged to make the base case explicit.
("Lemmas"; the example contrasts `if |a| == 1 { } else { ... }` (YES) with `if |a| > 1 { ... }` (NO))

Signature shape: a method lists `requires`, `modifies`, `ensures`, `decreases` after the signature ("Functions, Methods, Predicates, and Lemmas").

Questions to ask before designing:
> Is this variable name / function name `X` a good name? Is its purpose intuitively clear from the name? / Does it make sense that this method `M` is in module `X`? [...] Is `X.dfy` a good filename, that is, is its intended use clear from the name?
("Things to Consider")

## Reasons given
None for the rules above; the guide is prescriptive without rationale.

## What transfers to general-purpose Lean
- "Predicate vs Bool function" is the Dafny version of Lean's Prop vs Bool (`Decidable`) choice; the rule here is stated for Dafny's ghost/compiled split and does not carry over directly. A Lean guide would need its own position.
- Explicit base cases in inductive proofs: Lean's `induction ... with` already forces them.
- The `requires`/`ensures`/`decreases` triple is Dafny's way of putting contracts next to code; the Lean analogues are hypotheses, subtypes and `termination_by`.
- Topological ordering is imposed by Lean already.

## Caveats and unverified items
- The rendered page and source can differ; the rendered text was used (defuddle). Line anchors not recorded.
