# Batteries contributor documentation

| Field | Value |
|---|---|
| URL | https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/README.md |
| Author / org | leanprover-community (Batteries; formerly Std4) |
| Date / version | commit `4453b52d2468f4c346a8711d728c0742e7483c9b`, 2026-10-14, toolchain v4.36.0-rc1 |
| License | Apache-2.0 (`LICENSE` file, vendored) |
| Scope & audience | Batteries contributors ("data structures and tactics intended for use by both computer-science applications and mathematics applications of Lean 4") |
| Kind | descriptive (process); there is no style guide |
| Lean version | Lean 4 |
| Raw copy | none (read in place at `vendor/repos/batteries`) |

## Summary
Batteries has no written style or naming guide. Searching `README.md`, `docs/README.md`, `.github/`, `scripts/` and `lakefile.toml` for "style" gives no hit. Its README covers build/test/lint commands, PR status labels and the duty to adapt Mathlib; style is enforced by `linter.missingDocs = true`, the environment linter (`lake lint` running `runLinter`), and a trailing-whitespace/final-newline shell script. For style questions Batteries implicitly defers to Mathlib's guide and Lean core's. A 2024 Zulip thread (`notes/zulip-style-misc.md`, "style guide for comments?") discusses a proposed comment/docstring convention for Lean and Batteries, but whether it was adopted is unverified.

## Rules
> To run the environment linter, run `lake lint`. ([README, Build instructions](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/README.md#L21-L35))

> Every pull request should have exactly one of the status labels `awaiting-review`, `awaiting-author` or `WIP` ([README, Contributing](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/README.md#L54-L70))

> When necessary, Batteries contributors are expected to either create an adaptation PR, or ask for assistance for and to collaborate with this necessary process. ([Mathlib Adaptations](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/README.md#L72))

> One of the easiest ways to contribute is to find a missing proof ... The `proof_wanted` declaration documents statements that have been identified as being useful, but that have not yet been proven.

Enforced mechanically:
- [`lakefile.toml` L6-L7](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/lakefile.toml#L6-L7): `linter.missingDocs = true` for the library (off for tests) -- every public declaration needs a docstring.
- [`scripts/lintWhitespace.sh`](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/scripts/lintWhitespace.sh): fails on trailing whitespace and a missing final newline; run in CI ([`build.yml` L53-L56](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/.github/workflows/build.yml#L53-L56)).
- Environment linters in `Batteries/Tactic/Lint/`: `simpNF`, `simpComm`, `unusedArguments`, `docBlame`, `checkType`, `synTaut`, `unusedHavesSuffices`, `impossibleInstance`, `nonClassInstance`.
- `scripts/updateBatteries.sh` regenerates `Batteries.lean` imports when a file is added.

## Reasons given
Only process reasons (triage labels; Mathlib must adapt promptly because "Batteries PRs often affect Mathlib, a key component of the Lean ecosystem"). No stylistic justification anywhere.

## What transfers to general-purpose Lean
- Batteries is the nearest "general library, not math" community codebase, yet documents no style rules: any rules must be inferred from its code (another track surveys the code). 
- Transferable tooling idea: `missingDocs` + env linters + whitespace script as a minimal enforcement set; Mathlib's text-based linters also check trailing whitespace (`notes/mathlib-linters.md`).
- The README's audience statement shows the intended scope is both CS and math, which makes Mathlib's math-biased guide an imperfect fit.

## Caveats and unverified items
- Absence of a style doc is based on grepping the shallow clone; a wiki or Zulip-only conventions page could exist (unverified).
- Batteries was previously `std4`; pre-2023 Std4 contributor notes not checked.
