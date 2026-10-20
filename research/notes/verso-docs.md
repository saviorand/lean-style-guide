# Verso documentation (README, User's Guide, release-note process)

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/README.md |
| Author / org | Lean FRO; lead David Thrane Christiansen (README names him as the contact for contributions) |
| Date / version | Repo commit `76c3f3ca87642bb8122843d791662b507abac369` (2026-10-15); `lean-toolchain` = v4.36.0-rc1 |
| License | Apache 2.0 (`LICENSE`) |
| Scope & audience | Authors of Lean documentation (books, API docs, websites) and Verso contributors |
| Kind | descriptive; some contributor process |
| Lean version | Lean 4 |
| Raw copy | in repo `vendor/repos/verso` (not copied) |

## Summary
Verso is the FRO's documentation authoring tool; the Lean Reference, FPIL and TPIL are built with it, and `doc/style.md` in lean4 says docstring conventions should "facilitate an automated migration from Markdown to Verso". The repo has no coding style guide and no `CONTRIBUTING.md`; its README contains contribution process (talk first, branch/tag scheme matching Lean releases, release-note entries). The User's Guide (`doc/UsersGuide/*.lean`) documents the markup language, including a short "Design Principles" section. Nothing in these files prescribes how ordinary Lean programs should look.

## Rules / conventions found
Link base `https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/`.
- Contributions: "If you'd like to contribute, please get in touch with David Thrane Christiansen and discuss your plans ahead of time, as there is not presently much extra time to onboard and supervise new contributors." ([README L92-L98](https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/README.md#L92))
- Extensibility goal: "users should be able to implement their own extensions without needing to modify the Verso libraries." (same section)
- Release notes: "Significant pull requests should describe their changes in the Verso manual's release notes. CI will check that this has been done." Entry modules use `release_note` metadata and `public import` in `Entries.lean` ([README L108-L165](https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/README.md#L108)). Shows `module` / `public import` usage in practice.
- Branches/tags: tag `vX.Y.Z` of Verso matches Lean `vX.Y.Z`; `main` and `nightly-testing` branches (README L68-L90).
- Markup design principles ([Markup.lean L378-L402](https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/doc/UsersGuide/Markup.lean#L378)): "Fail fast rather than producing unexpected output or having complicated rules"; "Assume Unicode ... no need to support alternative textual syntaxes for characters not on keyboards".
- Docstring-related: UsersGuide has an entry on "Labeled Groups in Rendered Docstrings" and `Markup.lean` imports `Lean.DocString.Syntax`; the Verso markup for docstrings is therefore defined here, but no authoring recommendations were found.

## Reasons given
Design-principle reasons are given inline (above); the contributor rules are justified by limited maintainer time.

## What transfers to general-purpose Lean
- Evidence for tooling direction: docstrings are moving toward Verso syntax (checked cross-references and examples). A guide on docstrings should keep Markdown-compatible, simple formatting to ease migration (observation, not source text).
- `module`/`public import` style in a real FRO project is a usable example.
- Nothing on naming, structure, errors or tests.

## Caveats and unverified items
- `doc/UsersGuide/` was only sampled by grep (docstring, convention, style).
- Verso is moving fast ("rapid pace"); the docstring syntax may change.
