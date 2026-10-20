# Topic map

The backbone for the draft. Each topic covers five things:

- **Lean sources:** official and community Lean documents.
- **Stdlib:** measured practice, in [stdlib-survey.md](stdlib-survey.md).
- **Other languages:** guides for FP languages and proof assistants.
- **Agree:** points where the sources agree.
- **Conflict:** points where they disagree.

Every claim points to a note in `notes/`, and the notes carry the primary links. Open decisions are collected in [open-questions.md](open-questions.md) (`Q#` below).

Abbreviations:

- **core-style**: [lean-core-style](notes/lean-core-style.md), `doc/std/style.md`. It covers the stdlib only.
- **core-naming**: [lean-core-naming](notes/lean-core-naming.md), `doc/std/naming.md`.
- **doc-style**: [lean-core-doc-style](notes/lean-core-doc-style.md), `doc/style.md`.
- **FPIL**: [fpil](notes/fpil.md).
- **Mathlib**: [mathlib-style](notes/mathlib-style.md), [mathlib-naming](notes/mathlib-naming.md), [mathlib-doc](notes/mathlib-doc.md) and [mathlib-linters](notes/mathlib-linters.md).

Starting point: no existing guide targets general-purpose Lean code. Lean core's documents say they apply only to the stdlib ([core-style L11](notes/lean-core-style.md)), and Batteries has none ([batteries-contributing](notes/batteries-contributing.md)). CSLib and Iris-Lean defer to Mathlib ([community-cslib](notes/community-cslib.md), [community-iris-lean](notes/community-iris-lean.md)). On Zulip, Mario Carneiro said in 2023 that "lean4 repo does not maintain a style guide" ([zulip-style-misc](notes/zulip-style-misc.md)).

**Stdlib headline numbers.** From [stdlib-survey.md](stdlib-survey.md#ten-notable-measurements), which has the commands and permalinks.

- **Most of Init and Std is proofs.** Init has 5.5 theorems per def and Std has 4.6. Lake and src/Lean have almost none, and `do` is 30–50 times denser there. Program style is mostly visible in Lake and src/Lean, which affects how Q0 should rank evidence.
- **Lambdas.** Core writes `fun x =>` 97–99% of the time. Mathlib splits 51/49 between `=>` and `↦` (Q4).
- **Failure variants.** `?`/`!`/`D` is a Std idiom, with 105 full `X`/`X?`/`X!`/`XD` quadruples. In src/Lean only 9 of 1,149 `X?` defs have a `!` twin, so there `?` just means "returns `Option`" (Q1).
- **Lake's layout differs.** Its `|` arms sit at column 0. Signature continuations are indented by 2 rather than 4. In 202 headers the `:` starts a line, which style.md forbids. Lake also marks declarations `public` one by one rather than using a `public section` (Q0, Q6, Q22).
- **Line length.** p95 is 86–99 columns everywhere. Init has 3.9% of lines over 100 and Std 1.9%; Batteries and Mathlib enforce 100 (Q6).
- **Docstrings.** Public defs are documented at 73% in Init, 71% in Std, 56% in Lake, 39% in src/Lean, and 97% in Batteries and Mathlib. In Init and Std the first word is a third-person verb ("Returns") (Q19).
- **Termination.** `partial` is on 0.7–1.0% of defs in Init and Std but 7.7% in src/Lean. `partial_fixpoint` appears in no library file (Q15).
- **Proofs.** They live in separate `Lemmas.lean` files. The bundled type is `structure DHashMap where inner : Raw α β; wf : inner.WF` (Q9, Q17).

**Cross-author check.** From [author-survey.md](author-survey.md), which splits 395k lines of FRO program code into nine columns by first author. One author wrote 41% of it, and six others wrote most of the rest. The directory columns above mix authors, while Lake and Std.Http each come mostly from a single author.

- **Conventions across all, or all but one, of the nine columns:**
  - `fun x =>` (93.6–99.4%);
  - +2 indentation;
  - match arms at the `match` column;
  - split headers continued at +4 (Lake is the exception);
  - `where go` helpers;
  - anonymous instances;
  - `partial` in program code (1.3–8% of defs);
  - p95 line length 84–100, with every author putting 1–5% of lines over 100.
- **Author-dependent:**
  - `@[inline]`, from 0.13 to 36 per thousand lines;
  - docstring coverage, 34–57% for every column except one at 98.5%;
  - verb or noun-phrase docstrings;
  - let-else;
  - `private` and per-declaration `public`.

---

## 1. Naming

**Lean sources**
- Casing by kind: `UpperCamelCase` for types (codomain `Sort u`), `lowerCamelCase` for data, `snake_case` for theorems. Projections are named by their fields ([core-naming](notes/lean-core-naming.md)). Mathlib's rules 1–7 match ([mathlib-naming](notes/mathlib-naming.md)). The scheme dates from the 2021–22 Lean 4 port ("follow Lean + core lib with definitions, but keep underscores in lemma names"); Lean 3 used snake_case everywhere ([zulip-naming](notes/zulip-naming.md)).
- Predicates take an `Is` prefix, with stated exceptions. Each type gets a namespace so dot notation works, and declarations in the root namespace are rare ([core-naming](notes/lean-core-naming.md)).
- Failure variants: `?` returns `Option`, `!` may panic, and there may be a third variant that takes a proof ([core-naming](notes/lean-core-naming.md)). FPIL adds `D` for a default-returning variant and makes the unsuffixed name the proof-taking one. It also gives `-Of` for the non-outParam variant of a class, and lowercase package and executable names ([fpil](notes/fpil.md)). The Reference adds the `T.Raw`/`T.Raw.WF` and `Coll.iter` patterns ([lean-reference](notes/lean-reference.md)).
- FPIL's local-name conventions: Greek letters for type arguments "when no more specific name suggests itself"; `u v w` for universes; `ρ` for environments; `xs`/`ys` for lists; primes for related locals (`k'`). Argument names matter less than field names, which "form [a larger] part of the API" ([fpil](notes/fpil.md)).
- FPIL's own code (opt-in survey column): instances are always anonymous (0 of 133 named). Theorem names mix snake_case, snake+camel and lowerCamel, and `insertSorted` becomes `insert_sorted_size_eq`, against core-naming's rule. It has `Many.fromList` where the stdlib uses `ofList` ([fpil](notes/fpil.md#naming)).
- Other rules: no primed variants (pair `sshiftRightNat`/`sshiftRight` instead); acronyms of three letters or fewer keep one case (`IO`), longer ones are capitalized as words (`Json`); there are recommended variable names (`xs` for arrays, `l` for lists, `acc`, `i j k`, `n m`) ([core-naming](notes/lean-core-naming.md)).
- The stated value is guessability: names users can guess are faster to find than search tools ([core-naming](notes/lean-core-naming.md)).
- Gaps in every Lean source: names for instances, constructors, modules and files, `ofX`/`toX` conversions, monadic `M` variants, and private helpers. No Zulip thread on `get?`/`get!`/`getD` was found ([zulip-naming](notes/zulip-naming.md)). Iris-Lean documents instance names as `lowerCamelCase_suffix` ([community-iris-lean](notes/community-iris-lean.md)).

**Stdlib:** survey §1 has casing per declaration kind, primed names, suffix families and helper names.

**Other languages**
- Acronyms are treated as words (Tibell, Kowainik, Rust, F#).
- Abbreviations are avoided in public names (OCaml, F#, Scala).
- Predicates are marked: `?` in Clojure and Ruby (Ruby forbids `is_`), `Is`/`Can` in F#.
- Partial/total accessor pairs split: Rust uses `get` returning `Option`, `_unchecked`, and `as_`/`to_`/`into_` to signal cost; Ruby uses `!` only when a safe twin exists; Clojure's `!` marks side effects; Jane Street uses `_exn`; OCaml discourages `hd`/`tl` outright.
- The same parameter gets the same name everywhere (OCaml). Clojure has a table of idiomatic local names.

Sources: [rust-api-guidelines](notes/rust-api-guidelines.md), [bbatsov-ruby](notes/bbatsov-ruby.md), [bbatsov-clojure](notes/bbatsov-clojure.md), [ocaml-guidelines](notes/ocaml-guidelines.md), [fsharp-component-design](notes/fsharp-component-design.md).

Lemma-naming grammars in MathComp, agda-stdlib, Iris and F* serve as comparators only ([mathcomp-contributing](notes/mathcomp-contributing.md), [agda-stdlib-style](notes/agda-stdlib-style.md), [iris-style](notes/iris-style.md), [fstar-style](notes/fstar-style.md)).

**Agree:** casing fixed by kind, acronyms as words, no primes, a marker for partial variants.

**Conflict**
- `!` means "panics" in Lean, "dangerous or side-effecting" in Ruby and Clojure, and Rust has no marker.
- Predicate prefix: Ruby forbids `is_`, while Lean and F# use it.
- How a camelCase name embeds in a snake_case lemma name (`natCast` vs `nat_cast`) ([zulip-naming](notes/zulip-naming.md)). FPIL converts it to snake (`insert_sorted_size_eq`), and core-naming keeps lowerCamel.
- Open: Q1, Q2, Q3.

## 2. Layout and formatting

**Lean sources**
- core-style is the only official layout guide, and it is stdlib-only ([lean-core-style](notes/lean-core-style.md)):
  - Spacing rules for punctuation; continuation lines indented 2 spaces; operators at the end of a line; `then` stays with the condition; no orphaned parentheses.
  - Top level unindented, and `namespace`/`section` don't indent. Multi-line headers indent 4, with no `:` at the start of a line; bodies indent 2.
  - `where`, `termination_by` and `deriving` are unindented.
  - Match arms sit at the `match` column; alignment is "allowed, but not required".
  - Structure-instance braces: `{` on the preceding line, `}` alone.
- Mathlib ([mathlib-style](notes/mathlib-style.md), [mathlib-linters](notes/mathlib-linters.md)):
  - 100 columns, linted.
  - Top level and namespaces flush left; 4-space continuation and 2-space body indent; `by` at the end of a line; operators before the break.
  - No empty lines inside declarations (linted), `<|` rather than `$`, `fun` rather than `λ`.
- Line length: core states no number, Mathlib uses 100, and leanfmt uses 90 with leading operators, departing from community guidance ([community-leanfmt](notes/community-leanfmt.md)).
- Lambdas: core says "use `fun a => f x` instead of `fun x ↦ f x`", while Mathlib "slightly prefer[s]" `↦`. A 2025-08 attempt to mandate `↦` across Mathlib ended in "general disagreement" ([zulip-style-misc](notes/zulip-style-misc.md)).
- There is no released official formatter. It is on the FRO roadmap ([fro-blog](notes/fro-blog.md)), and on 2026-07-07 the status was "Still making progress but not released yet" ([zulip-formatter](notes/zulip-formatter.md)).
- FPIL: each `do` statement "is expected to start on its own line, and they should all have the same indentation", and "Idiomatic Lean code uses curly braces with `do` very rarely". Its code follows core-style's numbers rather than Lake's: split headers at +4 (92.5%), arms at the `match` column, no `↦`. It does use blank lines inside `do` blocks to separate phases ([fpil](notes/fpil.md#layout)).

**Stdlib:** survey §2 (lambda syntax), §4 (match layout, line-length distribution, indentation, splitting) and §14 (Unicode). The FPIL note has the same measures for the book's example code.

**Other languages**
- Line limits are soft, between 80 and 100.
- Strong agreement that layout should not depend on name length: block indent rather than visual alignment (Elm, F#, Rust). Tibell and Kowainik still align.
- A type signature on every top-level definition.
- Formatter stances vary:
  - Ormolu: no configuration.
  - ocamlformat: configurable, but recommends a pinned profile and version.
  - Fourmolu: about 28 options.
  - Rust: the default style is "recommended" and the formatter implements the guide.
- Guides that have a formatter say little about layout in prose.

Sources: [elm-style](notes/elm-style.md), [fsharp-style](notes/fsharp-style.md), [rust-style-guide](notes/rust-style-guide.md), [haskell-ormolu-fourmolu](notes/haskell-ormolu-fourmolu.md), [ocaml-ocamlformat](notes/ocaml-ocamlformat.md).

**Agree:** indentation numbers (2 for bodies, 4 for headers), flush-left top level, operator at the end of the line (core and Mathlib).

**Conflict**
- `=>` vs `↦`.
- Line limit: none (core), 100 (Mathlib), 90 (leanfmt).
- Operator position (leanfmt vs core and Mathlib).
- Alignment of match arms (core allows it; other languages forbid name-length-dependent layout).
- Blank lines inside declarations: FPIL uses them in long `do` blocks, and Mathlib lints them (`emptyLine`).
- Open: Q4, Q5, Q6.

## 3. Functions and expressions

**Lean sources**
- Use early `return` to reduce nesting, and `let some x ← e | alt` ([lean-core-style](notes/lean-core-style.md)).
- Nested actions are "often good style", lifting repetitive segments into helpers is good style, and braces with `do` are rare ([fpil](notes/fpil.md)).
- Accumulator-passing style is faster but "can also make it more difficult to understand" ([fpil](notes/fpil.md)).
- FPIL on functions ([fpil](notes/fpil.md#functions-and-expressions)):
  - "err on the side of too many, rather than too few, type annotations", for four stated reasons: readers, error localisation, the type as specification, and best-effort inference;
  - make type arguments implicit when later arguments determine them;
  - match a recursive function's arguments simultaneously, not as a pair (termination);
  - name intermediate values that are concepts or used twice;
  - split functions that mix two concerns;
  - use `_` for ignored input, and or-patterns "with care";
  - leading-dot constructors cost readability "in contexts like code review tools".
- FPIL on pipelines and sections: `|>` when "an input [...] is successively refined"; `<|` "where many nested parentheses pose a challenge"; `(· + 1)` for "very simple" lambdas; `pure f <*> E` is "overkill" for `f <$> E`.
- `where` vs `let rec`: FPIL's code uses `let rec` 15 times and `where` once. FRO code prefers `where` helpers named `go` in eight of nine author columns, and the largest contributor's code moved from `let rec loop` before 2024 to `where go` after ([author-survey](author-survey.md#consistent-across-authors)). Point-free style is still uncovered. CSLib prefers term-mode definitions over `by` ([community-cslib](notes/community-cslib.md)).

**Stdlib:** survey §3 (local helpers) and §5 (`do` notation).

**Other languages**
- Prefer pattern matching to partial projections, and avoid catch-all cases on types that can grow (OCaml, Scala, Tibell).
- Don't overuse point-free style (Tibell, Kowainik, F#, Clojure). hlint, by contrast, suggests eta reduction.
- Keep parameter lists short, preferring an options record (Clojure); avoid `bool` arguments in favour of custom types (Rust `C-CUSTOM-TYPE`).
- Avoid custom symbolic operators (F#, Kowainik, Databricks).
- Only Databricks and Clojure set numeric length limits.

Sources: [ocaml-guidelines](notes/ocaml-guidelines.md), [haskell-tibell](notes/haskell-tibell.md), [rust-api-guidelines](notes/rust-api-guidelines.md), [fsharp-component-design](notes/fsharp-component-design.md).

Proof assistants: agda-stdlib makes an argument implicit if it is "almost always" inferable, and Iris if it is inferable by unification in all intended uses ([agda-stdlib-style](notes/agda-stdlib-style.md), [iris-style](notes/iris-style.md)).

**Agree:** early exit over nesting, restraint with notation, short helpers.

**Conflict**
- Auto-bound implicits: FPIL relies on them throughout and calls them a convenience. Mathlib sets `autoImplicit false`, Std sets it in 70 of 499 files, and core's default is `true` ([fpil](notes/fpil.md#functions-and-expressions), [mathlib-linters](notes/mathlib-linters.md)).
- Other languages split on numeric vs qualitative limits.
- Open: Q7, Q8, Q27.

## 4. Data modelling

**Lean sources**
- `structure` for products and `inductive` for sums.
- Prefer a custom inductive with informative constructor names over `Sum`.
- Indexed families are rare; invariants are enforced with subtypes and explicit propositions.
- Positional `Point.mk` "not generally considered to be good Lean style".
- Instances use the `where` syntax.
- These come from FPIL and are hedged with "typically" ([fpil](notes/fpil.md)).
- FPIL's reasoned data-modelling rules ([fpil](notes/fpil.md#data-modelling)):
  - Use `{ p with … }` rather than copying fields by hand (three reasons: new fields, swapped same-typed fields, bureaucracy).
  - Use your own structures over `Prod` "because using domain terminology can make it easier to read the code" and catches mix-ups. Single-field wrappers cost nothing at run time.
  - Precise types need convenient APIs ("a trade-off between precise types and convenient APIs means that the precise types become less useful").
  - Subtypes are "a two-edged sword": "use them internally to a library, providing an API to users that automatically ensures that all invariants are satisfied".
  - Indexed families: rare, with four drawbacks argued (implementations leak into interfaces, slow definitional equality, poor errors, brittleness). Frequent `▸` casts to unstick them are "typically a code smell". They suit APIs that "resemble some other language".
  - `extends` is for "a clear taxonomic relationship". If a child must not deviate from its parent: document the relationship, require evidence, or drop inheritance.
  - Derive instances: it is less tedious, and "instances are updated as the definitions of types evolve", which keeps diffs reviewable. A hand-written `Ord` is fine.
  - `abbrev` for propositions that tactics must unfold, for monad stacks (so `ReaderT`'s features stay visible), and so dot notation sees through.
  - Parameters before indices, named explicitly; universe guidelines (separate variables, smallest universe).
- A custom constructor name needs a docstring ([lean-core-style](notes/lean-core-style.md)).
- Mathlib: one normal form, and wrapper structures instead of `irreducible` ([mathlib-style](notes/mathlib-style.md)).
- `Std.DHashMap` bundles its well-formedness proof. `Raw` + `WF` exists only for nested inductives, and the docs say "When in doubt, prefer `DHashMap`" ([bundled-unbundled](notes/bundled-unbundled.md)).

**Stdlib:** survey §8 (structure, inductive, class, deriving, instance naming, `abbrev`) and §13 (bundled invariants).

**Other languages and type-driven development**
- Make illegal states unrepresentable: split a record of options into a sum of per-state records (Minsky).
- Use the most precise type you reasonably can, push proof to the boundary, and use a smart constructor when full precision is impractical (King).
- Sources: [correct-by-construction](notes/correct-by-construction.md).
- Wrap primitives in named types (Kowainik, PureScript, Rust `C-NEWTYPE`).
- Hide representations that may change (F#, Rust `C-STRUCT-PRIVATE`).
- Prefer ADTs to class hierarchies.
- Immutable by default, with mutation behind pure interfaces.
- Sources: [haskell-kowainik](notes/haskell-kowainik.md), [rust-api-guidelines](notes/rust-api-guidelines.md), [fsharp-component-design](notes/fsharp-component-design.md).

**Agree:** sums for alternatives, named wrapper types, hidden representations, invariants in types where cheap.

**Conflict**
- Type aliases for domain types: Cornell encourages them, F# warns against them. In Lean this maps to `abbrev` vs `def` vs `structure`. FPIL gives reasons for `abbrev` in three specific cases but no general rule for domain types.
- Bundled vs unbundled invariants: Spitters and van der Weegen say bundling "comes at a substantial cost in flexibility"; Garillot et al. say full unbundling explodes argument lists ([bundled-unbundled](notes/bundled-unbundled.md)).
- Open: Q9, Q10, Q11.

## 5. Error handling

**Lean sources**
- The Reference describes the mechanisms without ranking them: `IO` throws or returns, plus `Except`, `MonadExcept`, `Option` and the `!`/`D` variants ([lean-reference](notes/lean-reference.md)).
- FPIL ranks some of them ([fpil](notes/fpil.md#error-handling)):
  - For indexing, take evidence as an argument first. Fall back to `?` "In cases where it's not practical to prove", with `!` last (its code has no `panic!`, `get!` or `getD`).
  - Use `Except` when callers need to know what failed.
  - Use `MonadExcept` so code is not tied to one encoding of exceptions.
  - For user input, return all errors at once (`Validate`, an applicative) and a specific result type, because exceptions "terminate the program at the first error".
  - Its division service throws an inductive `Err` from the backend and renders "a friendly string error" in the frontend. No stated policy.
- core-naming: "If your function may panic, consider adding `!`" ([lean-core-naming](notes/lean-core-naming.md)).
- The only community statement is a Zulip aside: don't reason about `panic!`, use `getD` ([zulip-naming](notes/zulip-naming.md)).
- No source has a policy on `panic!` in libraries, error types as inductives vs `String`, or catch-all handlers.

**Stdlib:** survey §6 (`Except`, `EIO`/`IO`, `Option`, `!`, `panic!`, `unreachable!`, and where each appears).

**Other languages**
- This is the biggest split among them.
- Errors in the type: Effective Scala, Rust `Result`/`C-GOOD-ERR`, F#'s first preference.
- Pushback on monadic errors: F# says "Do not use monadic error handling to replace exceptions"; Databricks says do not return `Try` from APIs.
- Everyone agrees: never catch everything, document failure modes (Rust "Errors"/"Panics" sections), and use specific error types.

Sources: [scala-effective](notes/scala-effective.md), [fsharp-style](notes/fsharp-style.md), [scala-databricks](notes/scala-databricks.md), [ocaml-guidelines](notes/ocaml-guidelines.md), [rust-api-guidelines](notes/rust-api-guidelines.md).

Type-driven development: "strengthen the argument, don't weaken the result" (King), and let callers choose how to discharge preconditions (Noonan). These map onto Lean's proof-argument / `?` / `!` triple ([correct-by-construction](notes/correct-by-construction.md)).

**Agree:** failure visible in the name or the type; documented failure modes; no blanket catches.

**Conflict:** `Except` vs `IO` exceptions as the default for library APIs; `!` in application code. Open: Q12, Q13.

## 6. Effects, IO and `do`

**Lean sources**
- `do` goes on the `:=` line, `Id.run do` counts as a bare `do`, and early `return` is used ([lean-core-style](notes/lean-core-style.md)).
- FPIL teaches `Id.run do` with `let mut`, `ReaderT`/`StateT` stacks and the `MonadReader` classes, and warns against a `Monad List` instance ([fpil](notes/fpil.md)).
- FPIL chapter 6 is the only Lean material on application structure ([fpil](notes/fpil.md#do-notation-and-effects)):
  - "a core set of easily testable functions written without monads paired with an outer wrapper", and a thin `Main.lean`;
  - a reader for configuration, because passing it by hand "is verbose and error-prone";
  - monad stacks as `abbrev`s of stdlib transformers, with three stated long-term benefits;
  - effect classes "to express [...] requirements", but a signature can be "more polymorphic than it should be", because transformer order changes meaning;
  - `modify` over `get`/`set`, against both a bug and a slowdown;
  - implement `Of` classes first.
- FPIL on `do` style: prefer `do` to `>>=` ("significantly more readable"); early return for CLI validation, to avoid nesting; `for … break` over `OptionT` tricks; `continue` called "confusing"; `let mut` "easier to read than an explicit local use of `StateT`"; `repeat`/`while` instead of `partial` loops.
- The book's code ends blocks with `pure` (226 vs 17 `return`), where stdlib program code prefers `return`. It never uses let-else.
- The Reference documents `do` semantics (mutable variables, `for`, `try`/`catch`/`finally`) without advice ([lean-reference](notes/lean-reference.md)).
- lean4.dev says to prefer `do` over `>>=`, but that source is unreliable ([community-lean4dev](notes/community-lean4dev.md)).

**Stdlib:** survey §5.

**Other languages:** wrap mutation in pure interfaces (F#, OCaml, Clojure); avoid global mutable state (Cornell, Databricks); release resources with `with-open`-style scoping rather than `finally` (Clojure) ([fsharp-style](notes/fsharp-style.md), [bbatsov-clojure](notes/bbatsov-clojure.md)).

**Agree:** local mutation via `let mut` inside a pure function is the idiomatic Lean form of "mutation behind a pure interface".

**Gap:** FPIL now covers monad-stack design. No Lean source covers resource handling (`IO.FS.withFile`, `try … finally`); FPIL relies on finalizers. The Reference gives the only concurrency rule ([lean-reference](notes/lean-reference.md#concurrency-read-2026-10-20)):

> sequential programs that interact with the operating system can use `IO` alone. Parallel programs should use `Task`s. `Async` is most appropriate when a program may spend a significant amount of time waiting on external events or I/O.

It adds `IO.checkCanceled` in impure tasks. The cookbook warns about deadlocking the task pool ([mprecipes](notes/mprecipes.md)). Open: Q14.

## 7. Termination

**Lean sources**
- FPIL: `partial` when "there is no alternative", for example loops over streams. Partial functions are "much less amenable to proofs". Partiality does not infect callers. Array loops use `termination_by arr.size - i` ([fpil](notes/fpil.md)).
- FPIL's recommended workflow ([fpil](notes/fpil.md#termination-and-recursion-q15)):
  - Declare the function `partial` and test it.
  - Replace `partial` with `termination_by` and state each needed fact as `have … := by sorry`.
  - Re-test, then prove. "This approach can prevent wasting time on proving that a buggy program terminates."
  - `partial` is acceptable where an application "doesn't need to mathematically reason about the process". Otherwise proving termination "removes one more potential source of bugs".
  - `repeat`/`while` and folds avoid the need for `partial`. "`let` [names] interesting values, while `have` is used to locally prove propositions".
- Joachim Breitner (FRO, 2024): structural recursion is "most pleasant" if you plan to prove theorems ([fro-blog](notes/fro-blog.md)).
- The Reference: `partial` is opaque to the logic, `partial_fixpoint` is an alternative, and `implemented_by` is "risky" ([lean-reference](notes/lean-reference.md)).
- core-style covers only the layout of `termination_by` and `decreasing_by`.

**Stdlib:** survey §7.

**Proof assistants:** Idris is covering by default and says `partial` is "not advisable" outside development and debugging ([idris2-docs](notes/idris2-docs.md)); Dafny puts `decreases` in the signature ([dafny-style](notes/dafny-style.md)). Other FP languages have nothing on this.

**Agree:** `partial` loses provability, and total is preferable when proofs are planned.

**Conflict:** none stated. FPIL gives a workflow and a criterion for `partial`, but no source gives a decision rule that covers fuel or `partial_fixpoint` for ordinary programs. Open: Q15.

## 8. Proofs about programs

**Lean sources**
- core-style's tactic section (stdlib):
  - Squeeze non-terminal `simp`.
  - Prefer `grind` and `omega`, with a comment explaining any decision not to use them.
  - No `erw`; don't over-golf or under-golf.
  - Its stated reason is robustness under upgrades ([lean-core-style](notes/lean-core-style.md)).
- FPIL: declare proofs with `theorem`, and clear simple cases with `simp` ([fpil](notes/fpil.md)).
- FPIL on the cost of proving ([fpil](notes/fpil.md#invariants-and-proofs-about-programs-q0b-q16-q18)):
  - Proofs "render many tests unnecessary", but "proving theorems about programs can be time consuming and expensive, so other tools are often more economical".
  - Keep the slow, clear version as "an executable specification" for the fast one, and test both before proving them equal.
- FPIL on proof style: "Each style of proof can be appropriate". Detailed scripts suit beginners or insight; short automated scripts are "typically easier to maintain"; recursive-function proofs are harder to read and maintain. `exact ih` "is somewhat fragile". Final forms use `fun_induction … <;> grind`.
- core-vision: stdlib components "will be verified" ([lean-core-vision](notes/lean-core-vision.md)).
- CSLib: no mid-proof `simp` unless it is `simp only` ([community-cslib](notes/community-cslib.md)).

**Stdlib:** survey §13 (same file vs `Lemmas.lean`, subtypes vs separate lemmas). Std splits `Basic`/`Lemmas` for HashMap ([bundled-unbundled](notes/bundled-unbundled.md)).

**Proof assistants and type-driven development**
- Proofs sit beside the code in every system read. agda-stdlib separates definitions (Base, Core) from Properties at module level ([agda-stdlib-style](notes/agda-stdlib-style.md), [cpdt-lean](notes/cpdt-lean.md)).
- CPDT shows intrinsic (indexed families) and extrinsic (plain data, a relation and theorems) side by side, and argues for heavy automation ([cpdt-lean](notes/cpdt-lean.md)).
- When not to prove: no source states a rule. FPIL's "other tools are often more economical" is the nearest Lean statement. The nearest points elsewhere are below ([correct-by-construction](notes/correct-by-construction.md), [proof-engineering](notes/proof-engineering.md)):
  - King: don't refactor a whole app to remove one `error "impossible"`; document the invariant in a comment.
  - AWS found model checking worth the cost where full proof was assumed too costly.
  - seL4: effort tracks proof size.

**Agree:** proofs live near the code; automation over brittle scripts; proofs convey why.

**Conflict**
- CPDT's custom automation vs the stock-tactics stance of Lean core and Mathlib.
- FPIL's intermediate proofs run unsqueezed `simp […]` followed by `rw`, which core-style ("Squeeze non-terminal `simp`") and Mathlib's `flexible` linter reject. Its final forms are terminal.
- Where in the stdlib proofs leave the definition file is a survey question.
- Open: Q16, Q17, Q18.

## 9. Documentation

**Lean sources**
- doc-style: docstrings open with a 1–3 sentence summary written as a present-tense fragment or noun phrase, then details, then examples. They are self-contained and may name parameters ([lean-core-doc-style](notes/lean-core-doc-style.md)).
- core-style: docstrings as required by `docBlame`, written in the "indicative mood", American spelling. Single-line delimiters stay on the same line; multi-line delimiters go on their own lines ([lean-core-style](notes/lean-core-style.md)).
- Lean core comments: concise, non-obvious only, no history ([lean-core-contributing](notes/lean-core-contributing.md)).
- Mathlib: every definition and major theorem has a docstring, plus the `/-! -/` module-doc conventions ([mathlib-doc](notes/mathlib-doc.md)). Batteries sets `linter.missingDocs = true` ([batteries-contributing](notes/batteries-contributing.md)).
- Docstrings are migrating to Verso markup ([verso-docs](notes/verso-docs.md)).

**Stdlib:** survey §11 (coverage, module docs, first-sentence form).

**Other languages:** document every exported item; examples in docs (Rust `C-EXAMPLE`); "Errors"/"Panics" sections (Rust); comments don't restate the code ([rust-api-guidelines](notes/rust-api-guidelines.md), [haskell-tibell](notes/haskell-tibell.md), [ocaml-cs3110](notes/ocaml-cs3110.md)). From type-driven development: comment the invariants that types don't enforce (King, Idris).

**Agree:** document every public declaration, summary first, explain why rather than what.

**Conflict**
- Mood: "indicative" (core-style) vs a noun-phrase fragment (doc-style).
- Delimiter placement: core vs Mathlib, still under negotiation on Zulip in 2024 ([zulip-style-misc](notes/zulip-style-misc.md)).
- Open: Q19, Q20.

## 10. Tests

**Lean sources:** no source states testing conventions, but the Reference describes the mechanism and practice converges on one pattern ([testing-practice](notes/testing-practice.md)):

- The Reference says a file of `#guard_msgs` checks "can be used as a test driver in Lake". It warns that, under the module system, `#eval` tests can pass in the editor and fail in a build unless they use `meta import`.
- **Practice:** a separate `<Pkg>Test` library, named as `testDriver`, which `lake test` just builds.
  - FRO repos, Batteries and Mathlib do this, as do 25 of 34 sampled repos.
  - An executable driver is used when tests must run IO (9 of 34; Strata, repl, LSpec).
- **Property tests:** Plausible (leanprover-community; used by Mathlib, Verso and Strata). LSpec is smaller.
- **FRO directions:**
  - Std.Http tests IO through `#eval runGroup … do check …`, with helpers shipped in `Std.Http.Test.Helpers`, plus fuzz tests.
  - Verso's Errata (Christiansen, 2026) adds `@[test]`, discovery, golden files, Plausible properties and JUnit/JSON reports. It is not a standalone package.
- Earlier material: the compiler's own test harness and its "tests first" practice ([lean-core-contributing](notes/lean-core-contributing.md)), and the `lake test` and `lake lint` drivers ([lake-docs](notes/lake-docs.md)).
- FPIL ([fpil](notes/fpil.md#tests-q21)):
  - Types and proofs remove "certain classes of unit test". Test before proving, and test what proofs can't see, such as copying (`dbgTraceIfShared`, in a built executable).
  - `#eval` on `IO` is re-run "at unpredictable times".
  - `example`s should be "paired with comments".
  - It teaches no test mechanism. The book checks its own examples with a local `#check_msgs`, a variant of `#guard_msgs`.

**Stdlib:** survey §12 (`#guard`, `example`, `#eval`; `tests/`, `BatteriesTest/`, `MathlibTest/`).

**Other languages:** coverage is thin: tests ship with libraries (PureScript), doc examples serve as tests (Rust), and Clojure has a Testing section that wasn't read in depth. Brady: types "rarely eliminate" tests ([tdd-idris-brady](notes/tdd-idris-brady.md)).

**Remaining gap:** where tests live is settled by practice. What is not settled: the boundary between compile-time and runtime tests, whether to recommend Errata once it is released on its own, and a rule for property tests. Open: Q21.

## 11. API design

**Lean sources**
- Stdlib vision: consistency, verified building blocks, performance, smooth adoption ([lean-core-vision](notes/lean-core-vision.md)).
- Namespace per type, `Internal` marking, scoped syntax unless public, and an RFC for any new public syntax ([lean-core-naming](notes/lean-core-naming.md), [lean-core-style](notes/lean-core-style.md)).
- Mathlib: deprecate with `since` and delete after 6 months ([mathlib-style](notes/mathlib-style.md)).
- CSLib: automation (simp and grind sets) is part of the API ([community-cslib](notes/community-cslib.md)).
- FPIL: modules are units of distribution and namespaces are units of organization ([fpil](notes/fpil.md)).
- The Reference on the module system ([lean-reference](notes/lean-reference.md#module-system-guidance-for-library-authors-read-2026-10-20)):
  - Use `public section` rather than `@[expose] public section` "for programming-focused files": "programs that will be run but not reasoned about".
  - Remove `public` and `@[expose]` where possible, to avoid rebuilds.
  - Keep `meta` minimal.
  - Prefer `@[expose]` to `import all` when outsiders may need access.
- Macros and notation:
  - Use macros only for syntax-to-syntax sugar, and an elaborator once types or control flow are involved.
  - Avoid partial, overlapping `macro_rules` on existing syntax ([mpbook](notes/mpbook.md)).
  - Syntax extensions "should be used in _output_ as well as in _input_" ([lean-reference](notes/lean-reference.md#notation-and-ffi-read-2026-10-20)).
- Instances: `BEq` and `Hashable` must agree, and code must not depend on which instance is synthesized ([lean-reference](notes/lean-reference.md#instances-and-deriving-read-2026-10-20)).
- FPIL on API design ([fpil](notes/fpil.md#type-classes-and-instances)):
  - "Polymorphic programs should be written to use as weak of an abstraction as possible, while datatypes should be given instances that are as powerful as possible."
  - Classes: keep them minimal; defaults are "specifications for correctness"; instances obey laws, and combined `Functor`/`Applicative`/`Monad` instances must agree; only sensible instances; default instances used selectively.
  - Coercions: only where the target represents every source value. Use them "responsibly", given three stated limitations, one of which is "visible to users of your API".
  - Prefer type classes to closed universes "In most cases"; use a structure of functions when "more manual control is needed".
  - Keep subtype proofs inside the library.

**Stdlib:** survey §9 (attributes, including `@[inline]`, `@[specialize]`, `@[simp]` and `@[grind]`) and §10 (`private`/`protected`, `open`, `variable`, the module system).

**Other languages**
- The Rust API Guidelines are the main reference: naming, predictability, type safety, future-proofing, stable `C-*` ids ([rust-api-guidelines](notes/rust-api-guidelines.md)).
- F#: qualified access by default and careful auto-open ([fsharp-component-design](notes/fsharp-component-design.md)).
- agda-stdlib limits each file's `variable` declarations to what the main type needs ([agda-stdlib-style](notes/agda-stdlib-style.md)).
- Explicit types on public definitions (F*, Scala, Haskell, Elm).

**Agree:** a minimal public surface, qualified access, explicit signatures, deprecation before deletion.

**Conflict:** none direct. One tension is internal to FPIL: "weakest abstraction" against its warning that effect-class signatures can be "more polymorphic than it should be". Lean sources are silent on visibility policy, `open` hygiene and attribute policy, and FPIL's code has no `private` at all. Open: Q22, Q23, Q24.

## 12. Tooling

**Lean sources**
- Lean core linters include `docBlame` (missingDocs), `unusedVariables` and `lake lint` ([lean-reference](notes/lean-reference.md)).
- Mathlib has three linter families (syntax, text, environment). `linter.mathlibStandardSet` is designed for downstream opt-in, and CSLib and Iris-Lean use it ([mathlib-linters](notes/mathlib-linters.md)).
  - General linters: `cdot`, `dollarSyntax`, `lambdaSyntax`, `longLine`, `emptyLine`, `missingEnd`, `setOption`, `hashCommand`.
  - Proof-specific linters: `flexible`, `multiGoal`, `simpNF`.
- No formatter has been released. The FRO's Year 4 roadmap includes a formatter and more stdlib linters ([fro-blog](notes/fro-blog.md)). Three community formatters exist ([zulip-formatter](notes/zulip-formatter.md), [community-leanfmt](notes/community-leanfmt.md)).
- Project layout follows the Lake template ([lake-docs](notes/lake-docs.md)).

**Stdlib:** survey §15 (linters in lean4, Batteries and Mathlib, and their defaults).

**Other languages:** compile warning-free (Tibell, Kowainik, OCaml, Cornell); a linter as codified style (hlint severity tiers, RuboCop); a pinned formatter version and profile (ocamlformat); a guide shouldn't duplicate what its formatter enforces ([haskell-hlint](notes/haskell-hlint.md), [ocaml-ocamlformat](notes/ocaml-ocamlformat.md)).

**Conflict:** writing layout rules now vs deferring to the coming formatter. Open: Q5, Q25.
