# Lean core contributor docs: CONTRIBUTING.md, AGENTS.md, commit convention, tests

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/CONTRIBUTING.md (also `AGENTS.md`, `.claude/CLAUDE.md` (identical copy, 169 lines), `doc/dev/commit_convention.md`, `tests/README.md`) |
| Author / org | Lean FRO / leanprover/lean4 maintainers |
| Date / version | commit `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` (2026-10-17) |
| License | Apache 2.0 (lean4 `LICENSE`) |
| Scope & audience | Contributors to the lean4 repo (compiler, core, stdlib, Lake) |
| Kind | normative (process); only a few code-level rules |
| Lean version | Lean 4 (4.37.0 pre-release) |
| Raw copy | `vendor/pages/lean-official/lean-core-contributing.md`, `lean-core-agents.md` |

## Summary
The general contributor docs say almost nothing about how code should look. `CONTRIBUTING.md` defers to "the established coding style of the project". The only code-level conventions found are in `AGENTS.md` (which holds guidance for coding agents but reads as maintainers' rules): comment policy, `module`/`prelude` requirement in `src/`, copyright headers, test-file docstrings, and a test-first workflow. `doc/dev/` (bootstrap, debugging, FFI, release, LLVM) contains no style material; `doc/dev/commit_convention.md` is about commit messages. A separate 1250-line documentation style guide lives at `doc/style.md` (see `lean-core-doc-style`).

## Rules
Base: `https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/`

From `CONTRIBUTING.md` ([Coding Standards](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/CONTRIBUTING.md#L33)):
> **Follow the Code Style**: Ensure that your code follows the established coding style of the project.
> **Lean on Lean**: Use Lean's built-in features and libraries effectively, avoiding reinventions.
> **Performance**: Make sure that your changes do not introduce performance regressions.
> **Write Tests**: Every new feature or bug fix should come with relevant tests.
> **Documentation**: Update relevant documentation, including comments in the code, to explain the logic and reasoning behind your changes.

From `AGENTS.md` ([Comments](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md#L75)):
> Inline comments should be concise. Use them for important, non-obvious facts about the code at hand. Avoid comments that: restate the code, repeat a type signature, or describe a general API contract; document old behavior, rejected alternatives, or the history of the change (that belongs in the PR body or commit message); explain API usage that belongs with the API definition instead of this call site.
> Rewrite a stale comment instead of adding a new one beside it. If a fact applies generally, document it at the definition.

([Module system, L142](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md#L142)):
> Files in `src/Lean/`, `src/Std/`, and `src/lake/Lake/` must have both `module` and `prelude` [...] Files outside these directories (e.g. `tests/`, `script/`) use just `module`.

([Copyright, L157](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md#L157)): new files need a copyright header; tests do not.

([Test docstrings, L163](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md#L163)):
> Every test `.lean` file must include a module docstring (`/-! ... -/`) briefly explaining what the file tests. For regression tests, reference the issue

([New features, L68](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md#L68)): "write comprehensive tests first (expecting that these will initially fail) and then iterate on the implementation until the tests pass."

Tests (`tests/README.md`, descriptive): tests are directories or "piles" of `.lean` files with `.out.expected` files; compile tests run the binary and compare output; benchmarks scale problem size with `TEST_BENCH`. This is the compiler's own harness, not a recommendation for library tests.

Commit convention (`doc/dev/commit_convention.md`): `<type>: <subject>` with types `feat`, `fix`, `doc`, `style`, `refactor`, `test`, `chore`, `perf`; PR body's first paragraph "must start with 'This PR'" (AGENTS.md L114).

## Reasons given
- Comments: keep history in PR/commit text, keep API contracts at the definition (stated in the list above).
- Process rules: "This practice produced hard to maintain code, performance problems, and bugs" (CONTRIBUTING intro, about accepting most PRs in the past).
- Module/prelude, copyright: no reason given.

## What transfers to general-purpose Lean
- Comment policy (non-obvious facts only; do not restate signatures; no change history) is language-agnostic and fits Lean projects.
- Module docstring at the top of each test file, and tests-first workflow, are cheap general conventions.
- `module` keyword in new files is evidence of where the module system is heading (see `lean-reference`).
- `prelude`, copyright headers, commit types and changelog labels are repo-specific.

## Caveats and unverified items
- `AGENTS.md` / `.claude/CLAUDE.md` are instructions to coding agents; whether maintainers regard them as binding style is **unverified**.
- No line-length setting found (`.editorconfig` absent at depth 3; **unverified** if the formatter enforces any).
- The FRO roadmap says a code formatter will ship ([roadmap y4-1](https://lean-lang.org/fro/roadmap/y4-1/)); see `fro-blog`.
