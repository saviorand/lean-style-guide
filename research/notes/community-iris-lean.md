# Iris-Lean style guide

| Field | Value |
|---|---|
| URL | https://github.com/leanprover-community/iris-lean/blob/0c3470534e1a66dbbc8a1443f3a3be888bddf4ec/Iris/style.md |
| Author / org | Iris-Lean contributors (leanprover-community) |
| Date / version | file last changed 2026-09-18, commit `0c3470534e1a66dbbc8a1443f3a3be888bddf4ec`; repo HEAD `81bc35088ba67d465db008f5261a9b341eb6cf6c` (2026-10-14) |
| License | Apache-2.0 (`gh api repos/leanprover-community/iris-lean/license`) |
| Scope & audience | Iris-Lean contributors (separation-logic framework port from Rocq) |
| Kind | normative (project) |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/community/community-iris-style.md` |

## Summary
A 123-line project guide that "follows the Mathlib style guide and the Mathlib naming convention wherever they apply" and adds: header format, a naming table, hypothesis-name capitalisation for two contexts, Rocq correspondence attributes, and a module-organisation rule (every directory has an entry-point `.lean` that transitively imports all modules; every module imports `Iris.Init`), mechanically checked in CI. The project also ships its own style linters (`Iris/Std/Linter/Style.lean`) whose docstrings say they follow Mathlib's guide.

## Rules
> Iris-Lean follows the Mathlib style guide and the Mathlib naming convention wherever they apply. ([style.md](https://github.com/leanprover-community/iris-lean/blob/0c3470534e1a66dbbc8a1443f3a3be888bddf4ec/Iris/style.md))

Naming table: types/structures/classes `UpperCamelCase`; definitions/abbreviations `lowerCamelCase`; theorems/lemmas `snake_case`; universe variables `u`, `v`.

> Type class instances are the exception: `lowerCamelCase` with a suffix separated by underscores (e.g. `elimInv_acc_with_close`).

> No double underscores: names such as `foo__bar` are rejected by the linter. No repeated namespace components: fully qualified names such as `Iris.BI.BI.foo` ... are flagged by the linter.

> Pure Lean hypotheses are lower-case: `h`, `h1`, `h2`, `hφ`... Iris hypotheses are capitalised: `H`, `H1`, `Hinv`... (domain-specific)

> every directory `Foo/` is accompanied by a module `Foo.lean` acting as its entry point ... These requirements are enforced by the CI. (`lake exe check-imports Iris`)

Linter docstrings (found by GitHub code search, not opened in full): "Following the Mathlib style guide, the 'λ' syntax is deprecated in Iris-Lean" (`Iris/IrisTest/Linter.lean`) and "definitions whose name contains an underscore: following Mathlib's style guide" (`Iris/Std/Linter/Style.lean`).

## Reasons given
Mostly mechanical enforcement; only the hypothesis-case rule has an implicit reason (two proof contexts must be distinguishable at a glance).

## What transfers to general-purpose Lean
- Another instance of downstream projects re-using Mathlib's guide and linter set rather than writing a general one.
- Useful precedent: entry-point-module-per-directory rule, `Init` module that sets options/linters for every file, CI-checked import structure; instance naming rule (`lowerCamelCase` plus `_suffix`) which Mathlib's naming page does not spell out in this form.
- Project-specific: hypothesis case, `rocq_alias`.

## Caveats and unverified items
- Only `style.md` was read in full; the linter files were seen via search snippets (unverified beyond the quoted lines).
