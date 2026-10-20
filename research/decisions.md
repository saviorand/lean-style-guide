# Decisions taken in the first draft

The first draft (2026-10-20) had to answer the questions in [open-questions.md](open-questions.md). Its rules are listed in [README.md](../README.md#rules) and explained in the chapter pages in [guide/](../guide/). Each line below gives the answer the draft uses and the anchor of the rule that states it. All of them are open to revision.

| Q | Decision in the draft | Rule |
|---|---|---|
| Q0 | Core `doc/std` style and naming are the base. FRO practice across authors confirms or overrides them. Mathlib rules are used only where they aren't about mathematics. | Introduction |
| Q0b | One short chapter on proofs about programs. For general proof style, the draft defers to core-style and Mathlib. | `#proofs-*` |
| Q0c | Evidence order: Lean documents, then FRO practice across authors, then Mathlib and Batteries, then other languages. | Introduction |
| Q1 | `?` for Option, `!` for panics, `D` for a default, no suffix for the total or proof-taking version. Every `!` gets a `?` twin. | `#naming-failure` |
| Q2 | Anonymous instances; constructors in lowerCamelCase; `ofX`/`toX` (not `fromX`); `M` suffix; recursive helpers named `go`. | `#naming-instances`, `#naming-conversions`, `#naming-monadic`, `#functions-helpers` |
| Q3 | `isX` for `Bool`, `IsX` for `Prop`; prefer `Bool` in program code. | `#naming-predicates` |
| Q4 | `fun x =>`. | `#functions-lambdas` |
| Q5 | Layout rules are stated now, and an official formatter overrides them once released. | Introduction, "Rule format" |
| Q6 | 100 characters as a soft limit; operator at the end of the line; no padding to align `=>`. | `#layout-line-length`, `#layout-splitting`, `#layout-match` |
| Q7 | `where` helpers; `let rec` only when the helper needs a local variable from the body. | `#functions-helpers` |
| Q8 | `|>`, `|>.`, `<|` and `·`; no `$`; at most two functions in a `∘` chain. | `#functions-pipelines`, `#functions-point-free` |
| Q9 | Check at the boundary and pass a type that carries the proof; no proof obligations for API users; no indexed families in APIs. | `#data-boundary`, `#data-indexed-families` |
| Q10 | `abbrev` for shorthand such as monad stacks, `structure` for domain types, no `def` type synonyms. | `#data-abbrev`, `#data-wrappers` |
| Q11 | Derive rather than hand-write; `Repr` on every data type; `Hashable` together with `BEq`. | `#data-deriving` |
| Q12 | `Option` for one obvious failure, `Except` when callers need the reason; `IO` code throws; `IO.ofExcept` where pure code meets `IO`. | `#errors-option-except`, `#errors-io` |
| Q13 | Inductive error types with `ToString`; panics only for bugs; document failure in docstrings; no catch-all handlers. | `#errors-types`, `#errors-panics`, `#errors-document`, `#errors-catch-all` |
| Q14 | `ReaderT` for configuration; `abbrev` for the application monad; `modify`; `try … finally`; `IO`, `Task` or `Async` as the Reference says. | `#effects-*` |
| Q15 | Structural recursion first, then `termination_by`; `partial` is fine with a comment; loops in `do` instead of recursive loop helpers. | `#recursion-*` |
| Q16 | FPIL's cost argument; test before proving; keep executable specifications. | `#proofs-cost`, `#proofs-spec` |
| Q17 | Short lemmas next to definitions; separate `Lemmas` modules once proofs grow. | `#proofs-location` |
| Q18 | Strong automation; non-terminal `simp` squeezed to `simp only`. | `#proofs-automation` |
| Q19 | A verb in the third person for functions, a noun phrase for types and constants. | `#docs-summary` |
| Q20 | Docstrings on every public declaration in libraries; failure behaviour in docstrings; examples checked by tests. | `#docs-public`, `#errors-document`, `#docs-examples` |
| Q21 | A `<Pkg>Test` library as `testDriver`; `#guard_msgs` and `#guard`; `meta import` in module tests; an executable driver for `IO` tests; Plausible for properties. | `#tests-*` |
| Q22 | The module system for libraries with `public section`; `private` helpers; an `Internal` namespace; `protected` for clashing names. | `#api-modules`, `#api-private`, `#api-protected` |
| Q23 | `open … in` for single declarations; avoid `variable`. | `#api-open`, `#api-variable` |
| Q24 | No `@[inline]` or `@[specialize]` without a measurement; `@[csimp]` over `@[implemented_by]`. | `#perf-*` |
| Q25 | Built-in linters plus `linter.missingDocs` in libraries; `lake build --wfail` in CI; no `warningAsError` in a library's own configuration. | `#project-options`, `#project-warnings`, `#project-linters` |
| Q26 | bbatsov's format with stable `<a name>` anchors and compiled examples. Licence not chosen; CC BY 4.0 is proposed. | Rule format, Contributing |
| Q27 | `autoImplicit = false`. | `#functions-auto-implicit`, `#project-options` |

## Not covered by the draft

- Unicode in identifiers and notation. Core prefers Unicode notation, but there's no rule yet for program APIs.
- Dependencies beyond pinning: semantic versioning, Reservoir, release process.
- `Async` and FFI beyond one rule each, and resource handling beyond `try … finally`.
- Errata, until it is released as a package of its own.

## Facts checked while drafting

All 129 checked examples compile with Lean 4.35.0 (`python3 tools/check_examples.py`). Behaviour that the text describes was checked separately with 4.35.0:
- A panic prints its message and the program continues with a default value; `LEAN_ABORT_ON_PANIC` makes it abort (`src/runtime/object.cpp`).
- `autoImplicit` is on by default.
- `where` helpers can use the outer function's parameters.
- `lake build --wfail` exists.
- `lake new` creates no `module` files and no test driver.
- Module files compile without experimental options.
- `scoped` notation needs a namespace, and `infixl` notation prints back as written.
- `def Port := Nat` blocks `OfNat Port`.
- `String.trim` no longer exists in 4.35; examples use `String.trimAscii`.

## Rules without a published source

Two rules have no source line: `collections-maps` and `project-dependencies`. Each needs a source or a decision to keep it as the editors' own advice. `project-formatting` gained a source on 2026-10-20 (Kowainik's rule on existing code).

## Citation changes on 2026-10-20

Haskell and primary sources replaced four of the seven Clojure citations:

- Consistency now cites PEP 8, where bbatsov's note comes from, and Kowainik.
- Existential cites Google's Haskell guide.
- Function size cites FPIL alone.
- Releasing resources cites `base`'s `bracket` documentation. The rule now asks for a `with…` helper built with `try … finally`.

The Clojure guide is still cited for the guiding principles, now alongside Simple Haskell and the Boring Haskell Manifesto. It is also still cited for parameter counts and for preferring functions to macros, where no Haskell guide says the same. Google's and Kowainik's guides were added as sources to twelve other rules ([haskell-google](notes/haskell-google.md), [haskell-kowainik](notes/haskell-kowainik.md)).
