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
| Q5 | Layout rules are stated now, and an official formatter overrides them once released. | The note at the top of the rules list |
| Q6 | 100 characters as a soft limit; operator at the end of the line; no padding to align `=>`. | `#layout-line-length`, `#layout-splitting`, `#layout-match` |
| Q7 | `where` helpers; `let rec` only when the helper needs a local variable from the body. | `#functions-helpers` |
| Q8 | `|>`, `|>.`, `<|` and `·`; no `$`. No rule on `∘` chains (dropped on 2026-10-21). | `#functions-pipelines` |
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
| Q23 | Avoid `variable`. No rule on `open` (dropped on 2026-10-21). | `#api-variable` |
| Q24 | No `@[inline]` or `@[specialize]` without a measurement; `@[csimp]` over `@[implemented_by]`. | `#perf-*` |
| Q25 | Built-in linters plus `linter.missingDocs` in libraries; `lake build --wfail` in CI; no `warningAsError` in a library's own configuration. | `#project-options`, `#project-warnings`, `#project-linters` |
| Q26 | bbatsov's format with stable `<a name>` anchors and compiled examples. Licence not chosen; CC BY 4.0 is proposed. | Contributing |
| Q27 | `autoImplicit = false`. | `#functions-auto-implicit`, `#project-options` |

## Not covered by the draft

- Unicode in identifiers and notation. Core prefers Unicode notation, but there's no rule yet for program APIs.
- Dependencies beyond pinning: semantic versioning, Reservoir, release process.
- `Async` and FFI beyond one rule each, and resource handling beyond `try … finally`.
- Errata, until it is released as a package of its own.

## Facts checked while drafting

All 127 checked examples compile with Lean 4.35.0 (`python3 tools/check_examples.py`). Behaviour that the text describes was checked separately with 4.35.0:
- A panic prints its message and the program continues with a default value; `LEAN_ABORT_ON_PANIC` makes it abort (`src/runtime/object.cpp`).
- `autoImplicit` is on by default.
- `where` helpers can use the outer function's parameters.
- `lake build --wfail` exists.
- `lake new` creates no `module` files and no test driver.
- Module files compile without experimental options.
- `scoped` notation needs a namespace, and `infixl` notation prints back as written.
- `def Port := Nat` blocks `OfNat Port`.
- `String.trim` no longer exists in 4.35; examples use `String.trimAscii`.
- A `Bool` parameter can be passed by name, as in `formatName "Ada" "Lovelace" (lastFirst := true)`, with or without a default.
- A macro whose expansion has a type error is accepted where it is defined and fails where it is used; the equivalent `def` fails where it is defined.

Measured on 2026-10-21 by grepping lean4 `3a685e6` (approximate counts):
- `Bool` binders such as `(quiet : Bool)` or `(quiet := false)`: about 200 in `src/Std` and 80 in `src/lake`. Lake passes `Bool` arguments by name at about 250 call sites, such as `(sync := true)`.
- Lines with two or more `∘`: 12 in `src/Std` and none in `src/lake`.
- `infix`, `infixl`, `infixr`, `prefix`, `postfix` and `notation` declarations: 21 in `src/Std` and none in `src/lake`.
- Docstrings saying "Panics if", "Throws if" or "Fails if" (any case, also "when"): about 80 in `src/Init` and `src/Std`.
- `catch _ =>`: 3 in `src/Std` and 8 in `src/lake`.

## Rules without a published source

Every rule has a source line since 2026-10-21. `collections-maps` cites only the `Std.HashMap` and `Std.TreeMap` docstrings, which describe the two maps but don't recommend one; no Lean document says when to use which. Three rules still rest on other languages alone, because no Lean source says the same: `data-illegal-states` (Minsky), `functions-exhaustive` and `errors-catch-all` (OCaml guidelines). Each holds in Lean as it does in OCaml.

## Citation changes on 2026-10-20

Haskell and primary sources replaced four of the seven Clojure citations:

- Consistency now cites PEP 8, where bbatsov's note comes from, and Kowainik.
- Existential cites Google's Haskell guide.
- Function size cites FPIL alone.
- Releasing resources cites `base`'s `bracket` documentation. The rule now asks for a `with…` helper built with `try … finally`.

The Clojure guide is still cited for the guiding principles, now alongside Simple Haskell and the Boring Haskell Manifesto. It is also still cited for parameter counts and for preferring functions to macros, where no Haskell guide says the same. Google's and Kowainik's guides were added as sources to twelve other rules ([haskell-google](notes/haskell-google.md), [haskell-kowainik](notes/haskell-kowainik.md)).

## Changes on 2026-10-21

The guide no longer cites the Clojure guide. Rules that came from other languages were checked against Lean documents and FRO code, using the measurements under [Facts checked while drafting](#facts-checked-while-drafting).

- The first two guiding principles cite PEP 8 and the OCaml guidelines, and Lean's `CONTRIBUTING.md` and Simple Haskell. `functions-options` cites `IO.Process.SpawnArgs`; its threshold of "about four parameters" has no source.
- Dropped `macros-functions-first`. It is correct in Lean, but no Lean source states it, and writing a macro where a function would do is a Lisp habit that Lean code rarely shows. `macros-macro-or-elab` keeps the part that matters in Lean: macros are for syntax sugar.
- Dropped `functions-point-free`. Its sources were Haskell and F# guides; Lean's core style warns against clever point-free expressions only in proofs, and FRO program code rarely chains `∘`.
- Dropped `api-open`. Its only source was the F# guide, and FRO code opens namespaces for a whole file about four times as often as it uses `open … in`.
- Rewrote `functions-bool-args`. It said to avoid `Bool` parameters, following the Rust API guidelines and Kowainik, but Std and Lake use them throughout and Lake passes them by name. It now asks for `Bool` arguments by name.
- Replaced other-language citations with Lean ones: `errors-types` (`IO.Error`, Lake's `CliError`), `errors-document` (standard library docstrings), `api-surface` (the Reference's note on rebuilds), `comments-invariants` (lean4 `AGENTS.md`), `macros-symbols` (core style on notation, and Lake defining no operators) and `project-formatting` (lean4 `CONTRIBUTING.md`).
- Added sources to `collections-maps` (the `Std.HashMap` and `Std.TreeMap` docstrings) and `project-dependencies` (the Lake README on `lake-manifest.json`).
