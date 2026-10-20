# Testing in Lean: mechanisms and practice (synthesis)

| Field | Value |
|---|---|
| URL | several; see each section (Reference, Lake README, Verso Errata, lean4 `tests/`, Plausible, GitHub code search) |
| Author / org | Lean FRO (Reference, Lake, Verso, lean4); leanprover-community (Plausible); sampled community repos |
| Date / version | Reference `400f168` (2026-10-15); lean4 `3a685e6` (2026-10-17); Verso `76c3f3c` (2026-10-15); Plausible `c2d7840` (2026-10-14); code search and sample run 2026-10-20 |
| License | Reference, lean4, Verso, Plausible: Apache-2.0; LSpec: MIT (repo metadata); sampled repos: various |
| Scope & audience | Library and application authors choosing how to test Lean code (Q21) |
| Kind | descriptive (no source states testing conventions; this note records mechanisms and measured practice) |
| Lean version | Lean 4 (4.34–4.37) |
| Raw copy | sampled lakefiles in `vendor/pages/testing/lakefiles/`, sample list `vendor/pages/testing/sample-repos.tsv`, classifier `scripts/classify-test-drivers.py` |

## Summary
No Lean source states testing conventions for libraries or applications. There is a clear de facto pattern anyway. Libraries put compile-time checks (`#guard_msgs`, `#guard`) in a separate `<Pkg>Test` library and name it as Lake's `testDriver`, so `lake test` builds it. Projects with runtime or IO tests use an executable driver instead. The Reference describes exactly this model. Property testing means Plausible, a leanprover-community package that Mathlib, Verso and Strata use. In 2026 the FRO built Errata, a full test framework, inside Verso. It is the clearest statement of what the FRO thinks Lean tests need, but it is not a standalone package.

## Rules and statements from sources

### Mechanisms (Reference, Lake)
> Together with the interaction commands in this section, it can be used to construct a file that will only elaborate if the output is as expected; such a file can be used as a test driver in Lake. ([Reference, Interaction.lean L552-L553](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L552-L553))

> As a result, modules that use `#guard_msgs` together with `#eval` to embed lightweight tests may elaborate successfully in the language server but fail during a build. To fix this, the definitions can be imported with `meta import` in the module that contains the test ([Interaction.lean L95-L96](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L95-L96))

> An executable driver will be built and then run, a script driver will just be run, and a library driver will just be built. ([Lake README L219-L226](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md#L219-L226))

`lake new` templates add no test driver ([Lake/CLI/Init.lean](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/CLI/Init.lean), grep for `testDriver` finds nothing), so every `testDriver` in the wild was added by hand.

### FRO practice
- **lean4 core:** library code contains no tests. Tests live in `tests/` piles with `.out.expected` golden files and a doc comment per test ([stdlib-survey §12](../stdlib-survey.md#12-tests)).
- **Std.Http / Std.Async (Sofia Rodrigues):** IO tests in `tests/elab` are written as `#eval runGroup "Basic dispatch" do check "…" (raw := …) (handler := …) (expect := …)`, with assertion helpers shipped in the library itself ([src/Std/Http/Test/Helpers.lean](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Http/Test/Helpers.lean); [tests/elab/async_http_dispatch.lean L1-L15](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/tests/elab/async_http_dispatch.lean#L1-L15)). There are fuzz tests too (`async_http_fuzz*.lean`).
- **lean4-cli (Marc Huisinga):** `testDriver = "CliTest"`, a library.
- **doc-gen4:** two shell scripts in `test/`, no Lean tests.
- **Verso (David Thrane Christiansen): Errata**, added in Verso 4.34.0:

  > Previously, Verso's tests were all essentially _ad hoc_ IO actions that were run in sequence or elaborations that would fail. [...] there were no universal conventions about output or failure reporting, and it could be difficult to see which test had actually failed at a glance. `Errata` unifies reporting and eliminates the need to plumb lists of tests through the system. ([TestFramework.lean L22-L25](https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/doc/UsersGuide/Releases/Entries/TestFramework.lean#L22-L25))

  Its features (same file, L27-L33): tests are marked `@[test]` and can be of any type with an `IsTest` instance. Docstrings and source ranges are kept for failure reports. Discovery runs every test in the package. Property tests can be rerun with a fixed seed, and golden files can be updated. It fails on warnings with `--wfail` and writes JUnit XML, JSON and Markdown reports. `#test_msgs` and `#test_guard` are compile-time variants of `#guard_msgs` and `#guard` whose outcomes are reported with the rest of the suite. Property tests use Plausible ([src/errata/Errata/Property.lean](https://github.com/leanprover/verso/blob/76c3f3ca87642bb8122843d791662b507abac369/src/errata/Errata/Property.lean)).

### Community libraries
- **Plausible** (leanprover-community, Apache-2.0, 117★, created 2024-10, successor to Mathlib's `slim_check`): "A property testing framework for Lean 4 that integrates into the tactic framework." It works as a tactic (`plausible`) on a goal, or at run time with `Plausible.Testable.check`. Custom types need `Repr`, `Shrinkable` and `SampleableExt`/`Arbitrary` instances ([README](https://github.com/leanprover-community/plausible/blob/c2d7840c65673533e15b499f25beecdc6227f7d8/README.md)).
- **LSpec** (argumentcomputer, MIT, 86★): a unit-test DSL with an executable runner. Adoption is smaller (counts below).

### Measured adoption (GitHub code search, 2026-10-20)
GitHub's `total_count` values are estimates, and they include forks and vendored copies.

| query | files |
|---|---|
| `"#guard_msgs"` in Lean files | 7,024 |
| `testDriver` in `lakefile.toml` / `lakefile.lean` | 1,382 / 106 |
| `"import Plausible"` | 110 |
| `"import LSpec"` | 73 |
| `plausible` in lakefile (toml / lean) | 97 / 81 |
| `lspec` in lakefile (toml / lean) | 32 / 59 |

**Sample:** I took the first 100 search hits for `testDriver` in `lakefile.toml`, kept non-forks with one repo each (34 repos), and classified the driver target:
- **25 are `lean_lib` (74%),** built only, so the tests are compile-time checks. Names follow `<Pkg>Test` in the large majority: `BatteriesTest`, `AesopTest`, `QqTest`, `CliTest`, `ParserTest`, `RegexTest`, `LeanSearchClientTest`, `GraphitiTest`, …
- **9 are `lean_exe`,** which run tests at run time: `repl`, `LSpec`, `Strata`, `malgo`, `json-schema-lean`, `LeanPlot`, `langlib`, `LeanSage`, `lean-eval`.
- 11 of the 34 depend on Mathlib.

Search ranking favours popular repos.

**Strata** (AWS, Apache-2.0 OR MIT, 279★, `431a7ec`, 2026-10-20) is the largest non-maths test suite in the sample, with 477 test files. Its tests are table-driven corpora (`Case` records with `name`, `outcome` and a `why` string), checked at compile time in module files that `meta import` the harness. That is the Reference's fix for `#eval` tests under the module system. A separate executable, `StrataTestMain`, runs the IO tests ([StrataLaurel/Tests/DynamicDispatchTest.lean](https://github.com/strata-org/Strata/blob/431a7ec72ff2e4759128f0e6faff1bbdea63c63e/StrataLaurel/Tests/DynamicDispatchTest.lean), [Scripts/StrataTestMain.lean](https://github.com/strata-org/Strata/blob/431a7ec72ff2e4759128f0e6faff1bbdea63c63e/Scripts/StrataTestMain.lean)).

### Earlier findings (cross-reference)
FPIL's principles are recorded in [fpil](fpil.md#tests-q21):
- types and proofs remove some tests;
- test before proving;
- test what proofs can't see in a built executable;
- `#eval` on `IO` reruns at unpredictable times.

lean-regex keeps `#guard` tests inside its library tree, unlike everyone else measured ([stdlib-survey §12](../stdlib-survey.md#12-tests)).

## Reasons given
- Reference: a test file that only elaborates when the output is right turns `lake build` into a test run. `meta import` is needed because the compiler, unlike the server, enforces phases.
- Errata: uniform failure reporting, and no hand-maintained lists of tests.
- FPIL: see the note.
- The `<Pkg>Test` library pattern is stated nowhere. It is only practised.

## What transfers to general-purpose Lean
- One pattern can be recommended with evidence behind it: a separate `<Pkg>Test` library of `#guard_msgs`/`#guard` files, named as `testDriver` so `lake test` builds it. Use an executable driver when tests must run IO at run time. FRO projects, Batteries, Mathlib and three quarters of the sample do this.
- Keep tests out of library modules: core has none in `src`. Std.Http's exception is that its test helpers are part of the public library.
- Under the module system, test files that `#eval` library code need `meta import`. The Reference names this trap, and Strata follows the fix.
- Plausible is the property-testing default, through both FRO (Verso) and community use. LSpec is a smaller alternative.
- Golden-output tests (`.out.expected`, Errata's golden files) are FRO practice for output-heavy code.
- Errata shows where the FRO's thinking is heading (discovery, `@[test]`, reports). The guide can mention it but cannot recommend it as a dependency until it is released on its own.

## Caveats and unverified items
- Code-search counts are estimates. The sample covers only `lakefile.toml` and the first 100 hits.
- "Library driver = compile-time tests" is inferred from Lake's semantics; test file contents were read only for Strata, Std.Http and lean4-cli.
- Whether Errata will be split out of Verso is unknown. The release note says nothing about it.
- LSpec was checked by metadata only. Its README and API were not read.
