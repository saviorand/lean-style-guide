# Mathlib's style linters, as documented

| Field | Value |
|---|---|
| URL | https://github.com/leanprover-community/mathlib4/tree/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter (docstrings); [`Mathlib/Init.lean`](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Init.lean#L83-L117); [`lakefile.lean`](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/lakefile.lean); [`scripts/README.md`](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/scripts/README.md#L230) |
| Author / org | Mathlib maintainers |
| Date / version | mathlib4 `7bb03b4c5313d552989ba5b1c6d3f0f436f65d73`, 2026-10-17, toolchain v4.36.0-rc1 |
| License | Apache-2.0 (file headers: "Released under Apache 2.0 license as described in the file LICENSE") |
| Scope & audience | Mathlib CI; downstream projects may opt in via `linter.mathlibStandardSet` |
| Kind | descriptive (documentation of enforcement) |
| Lean version | Lean 4 |
| Raw copy | none (read in place from `vendor/repos/mathlib4`) |

## Summary
Mathlib enforces part of its style guide mechanically through three families: syntax linters (Lean options `linter.*`, run in every `lake build`), text-based linters (`scripts/lint-style.lean`, run as `lake exe lint-style`), and environment linters (Batteries' `runLinter` via `lake lint`). The `Style.lean` docstring says of the style linters: "All of these linters are enabled in mathlib by default, but disabled globally since they enforce conventions which are inherently subjective." Counting linters in code is another track's job; this note records what each documents as its purpose.

## Rules (what is enforced, quoted from the linters' docstrings)
Enablement: `linter.mathlibStandardSet` bundles the on-by-default syntax linters ([`Init.lean` L83-L117](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Init.lean#L83-L117)): `auxLemma, flexible, hashCommand, oldObtain, privateModule, style.cases, style.induction, style.refine, style.cdot, style.docString, style.dollarSyntax, style.emptyLine, style.header, style.lambdaSyntax, style.longLine, style.longFile, style.multiGoal, style.native, style.openClassical, style.maxHeartbeats, style.missingEnd, style.setOption, style.show, style.whitespace, unusedDecidableInType, unusedFintypeInType`. [`lakefile.lean`](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/lakefile.lean) turns it on (as `weak.`) plus `style.header`, `checkInitImports`, `allScriptsDocumented`, `style.longFile 1500`, and sets `autoImplicit false` and `pp.unicode.fun true`. Not in the set: `haveLet` ("disabled by default due to crashes"), `ppRoundtrip` ("not mature enough"), `minImports` and `upstreamableDecl` (informational) ([`Init.lean` L62-L81](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Init.lean#L62-L81)). A weekly set (`linter.weeklyLintSet`) and a nightly regression set (tacticAnalysis) exist.

Layout and syntax preferences ([`Style.lean` header docstring](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/Style.lean#L18-L50)):
> the `cdotLinter` linter checks for focusing dots `·` which are typed using a `.` instead: this is allowed Lean syntax, but it is nicer to be uniform

> the `dollarSyntax` linter checks for use of the dollar sign `$` instead of the `<|` pipe operator: ... mathlib prefers `<|` for the symmetry with the `|>` symbol

> the `lambdaSyntax` linter checks for uses of the `λ` symbol for anonymous functions, instead of the `fun` keyword: mathlib prefers the latter for reasons of readability

> the `longFile` linter checks for files which have more than 1500 lines; the `longLine` linter checks for lines which have more than 100 characters

> the `missingEnd` linter checks for sections or namespaces which are not closed by the end of the file: enforcing this invariant makes minimising files or moving code between files easier

> the `nameCheck` linter checks for declarations whose names are in non-standard style, such as by containing a double underscore. The `defsWithUnderscore` environment linter checks for definitions whose name contains an underscore

Other syntax linters, with their documented purpose:
- `emptyLine`: "emits a warning on empty lines inside a command, but outside of a doc-string/module-doc" ([EmptyLine.lean](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/EmptyLine.lean)).
- `whitespace`: "emits a warning if either a command does not start at the beginning of a line; or the 'hypotheses segment' of a declaration does not coincide with its pretty-printed version" ([Whitespace.lean](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/Whitespace.lean)).
- `multiGoal`: "the mathlib style guide ask that goals be focused until there is only one active goal at a time" ([Multigoal.lean](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/Multigoal.lean)).
- `flexible`: a "rigid" tactic such as `rw` must not act on the output of a "flexible" one such as `simp` ([FlexibleLinter.lean](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/FlexibleLinter.lean)); this is the lint form of the "do not squeeze terminal simp" tradeoff.
- Deprecated-syntax linter: flags `refine'`, `cases'`, `induction'`, `admit`, `native_decide`, and `set_option maxHeartbeats` without an explanatory comment ([DeprecatedSyntaxLinter.lean](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/DeprecatedSyntaxLinter.lean)).
- `setOption`: "The `debug`, `pp`, `profiler` and `trace` options are good for debugging, but should not be used in production code" ([Style.lean L81+](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/Style.lean#L81)).
- `hashCommand`: no `#`-commands in Mathlib except an allow-list. `auxLemma`: warns on references to auto-generated names (`_proof_1`, `match_1`), "not stable across refactors". `docPrime`: a declaration whose name ends in `'` needs a doc-string. `overlappingInstances`: local instance diamonds. `unusedTactic`: "every tactic call actually changes *something*". `directoryDependency`: keeps listed directories independent for modularity. `docString`/`docStringVerso`: doc-string syntax checks (Verso parse errors).
- Text-based ([TextBased.lean header](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Tactic/Linter/TextBased.lean#L22-L36)): adaptation-note usage, Windows line endings, trailing whitespace, module names in upper camel case, module names valid on Windows, Unicode allow-list, variant selectors; space before `;`.
- Environment linters (Batteries, via `lake lint`): `simpNF`, `simpComm`, `unusedArguments`, `docBlame`, `checkType`, `synTaut`, `unusedHavesSuffices`, `impossibleInstance`, `nonClassInstance` ([Batteries `Lint/`](https://github.com/leanprover-community/batteries/tree/4453b52d2468f4c346a8711d728c0742e7483c9b/Batteries/Tactic/Lint)). Mathlib's `nolints.json` holds exceptions.

CI: `.github/workflows/build_template.yml` runs `lake lint` (L644, retried, 10 minute timeout) and `lint-style-action` (L1135) after the build; text/style failures fail the PR.

## Reasons given
- Purely stylistic ones state "both symbols have the same meaning" and give uniformity, readability, or symmetry as reason (quotes above); `Style.lean` calls them "inherently subjective".
- Maintenance/robustness reasons: `auxLemma` (names unstable), `missingEnd` (move code between files), `setOption` (debug options not for production), `flexible` (fragile `simp` interplay), `directoryDependency` (modularity).
- Emphasis on tooling over prose: the `Whitespace` linter compares source against the pretty-printer, which is why Mathlib's layout follows `ppRoundtrip`-like output.

## What transfers to general-purpose Lean
- The `mathlibStandardSet` option is explicitly designed for downstream use ("Projects depending on mathlib can use `set_option linter.mathlibStandardSet true`"), so a program project can adopt layout lints without the math ones; CSLib and Iris-Lean do exactly that (`notes/community-cslib.md`, `notes/community-iris-lean.md`).
- General: `cdot`, `dollarSyntax`, `lambdaSyntax`, `longLine`, `emptyLine`, `whitespace`, `missingEnd`, `setOption`, `hashCommand`, `auxLemma`, `unusedTactic`, text linters, `docBlame`, `unusedArguments`, `unusedHavesSuffices`.
- Math/proof-specific: `simpNF`, `simpComm`, `flexible`, `multiGoal`, `haveLet`, Decidable/Fintype lints, `upstreamableDecl`.
- No linter documented here checks program-style concerns (partial functions, panics, error-handling shape, naming of `?`/`!` variants).

## Caveats and unverified items
- Option list copied from `Init.lean`; the standard set changes often.
- I did not verify which linters are active in the default build beyond the `lakefile.lean` options.
- Quotes of the `Style.lean` lines are from the file header; line numbers are approximate to the permalink SHA.
