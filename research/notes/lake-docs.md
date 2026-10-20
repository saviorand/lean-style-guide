# Lake documentation (`src/lake/README.md` and the Reference's Lake chapter)

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md |
| Author / org | Lean FRO (Lake is maintained in the lean4 repo; original author Mac Malone, **unverified** from these files) |
| Date / version | lean4 commit `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` (2026-10-17). README states it describes "Lake relative to the current commit" |
| License | Apache 2.0 (lean4 `LICENSE`) |
| Scope & audience | Lake users and package authors; configuration reference, not style |
| Kind | descriptive |
| Lean version | Lean 4 |
| Raw copy | in repo `vendor/repos/lean4/src/lake/README.md` (not copied) |

## Summary
Lake has no contributor or style guide in the repo: `src/lake/` contains one README (600 lines), `schemas/`, and the sources; `find src/lake -name '*.md'` returns only the README. The README is a configuration reference (package, library, executable, target and dependency options) plus the project template. The Lean Language Reference has a fuller Lake chapter (`Manual/BuildTools/Lake/*.lean` in the reference-manual repo, see `lean-reference`) which was not read. Style-relevant material is limited to the project template, a few "conventionally" notes, and test/lint driver configuration.

## Rules / conventions found
Link base `https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md`.
- Config location: "Lake configurations can be written in Lean or TOML and are conventionally stored in a `lakefile` in the root directory of package." ([L4](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md#L4))
- Template layout produced by `lake new`/`lake init` ([L60-L72](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md#L60)): library sources in `Hello/` with `Hello/Basic.lean`, library root `Hello.lean` that imports standard modules, `Main.lean` with `def main : IO Unit`, `lakefile.toml`, `lean-toolchain`, `.gitignore`. (paraphrase of the template; no rule text)
- Package/executable lowercase, library uppercase is taught by FPIL, not by the Lake README (see `fpil`).
- Test/lint: "The CLI commands `lake test` and `lake lint` use definitions configured by the workspace's root package" via `@[test_driver]` / `@[lint_driver]` or `testDriver`/`lintDriver` options ([Test & Lint, L217-L227](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md#L217)).
- Dependencies: Lean `require` or TOML `[[require]]` from Reservoir, git or path; the README gives no advice on version pinning.
- FRO roadmap (y4-1) says new commands `lake check` and a `lake build` mode that skips kernel checks are planned ([roadmap](https://lean-lang.org/fro/roadmap/y4-1/)).

## Reasons given
None for the layout; it is a description of defaults.

## What transfers to general-purpose Lean
- The template is the de facto project skeleton (library + executable, root file importing submodules). Conventions about project layout, testing (`lake test`), linting (`lake lint`) can cite it.
- Nothing about code style; stdlib-style rules do not mention Lake layout.

## Caveats and unverified items
- The Lake chapter of the Reference, the `lake new --template` variants, and Lake's own source layout (`src/lake/Lake`) were not examined as style evidence.
- README is "relative to the current commit", so it may describe unreleased behaviour.
