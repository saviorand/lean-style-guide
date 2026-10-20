# doc-gen4 documentation (README)

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/doc-gen4/blob/0656b7ebd305f089c8d6bd8684a0797f19414cc2/README.md |
| Author / org | leanprover (Lean FRO-hosted; original author Henrik Böving, **unverified** from these files) |
| Date / version | Repo commit `0656b7ebd305f089c8d6bd8684a0797f19414cc2` (2026-10-15); `lean-toolchain` = v4.36.0-rc1 |
| License | Apache 2.0 (`LICENSE`) |
| Scope & audience | Library authors generating HTML API documentation |
| Kind | descriptive (usage) |
| Lean version | Lean 4 |
| Raw copy | in repo `vendor/repos/doc-gen4` (not copied) |

## Summary
doc-gen4 has only a usage README. There is no `CONTRIBUTING.md`, no style guide, and no statement of how docstrings should be written. It does reveal practices the tool assumes: a nested `docbuild` project, building docs with `lake build YourLibrary:docs`, and keeping the library compiling in CI. It depends on `MD4Lean` (a Markdown parser), so docstrings are rendered as Markdown (inference from `lakefile.lean`).

## Rules / conventions found
Link base `https://github.com/leanprover/doc-gen4/blob/0656b7ebd305f089c8d6bd8684a0797f19414cc2/README.md`.
- Setup: create a `docbuild` subdirectory with its own `lakefile.toml` requiring `doc-gen4` and the parent project; run `lake build YourLibraryName:docs` (Usage section).
- "Note that we do not recommend this approach and suggest to instead make sure your projects always compile by using CI to prevent broken code from being added and `sorry`-ing out things that you intend to complete later." (about removing failing imports to get partial docs)
- Note that doc-gen4 "is perfectly capable of generating documentation for Lean code that contains `sorry`, just not for code that doesn't compile."
- Version pinning: use `rev = "main"`, or `v4.x` tag matching your Lean version ("keep in mind to update this field as you update your Lean version").
- Docs always include `Lean`, `Init`, `Lake`, `Std` in addition to your targets.
- Source links: `DOCGEN_SRC` = `github` (default), `file`, or `vscode`.
- Equation generation can be disabled with `DISABLE_EQUATIONS=1`.

## Reasons given
Only the CI/`sorry` recommendation has a stated rationale (avoid broken code landing).

## What transfers to general-purpose Lean
- Supports a guide point that API docs are a build target (`:docs` facet), docstrings are public-facing, and CI should keep the project compiling.
- The Lean Documentation Style Guide (`lean-core-doc-style`) names doc-gen as one of three contexts where docstrings are viewed.
- Nothing prescriptive on docstring content.

## Caveats and unverified items
- Which Markdown dialect doc-gen4 accepts, and whether it renders Verso docstrings, not verified.
