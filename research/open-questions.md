# Open questions

These are decisions the guide's editors will need to make. Each one lists where the sources conflict or are silent, and links to the evidence. Numbering matches the `Q#` references in [topic-map.md](topic-map.md). The questions marked ★ are the ones I think matter most.

## Scope and method

- **Q0 ★ Adopt or diverge from core `doc/std/style.md`?** It is the only official layout guide, but it is stdlib-only by its own statement, and about half its examples are theorems ([lean-core-style](notes/lean-core-style.md)). Options:
  - adopt it wholesale for general-purpose code;
  - adopt it and override specific rules;
  - write independent rules.

  A second sub-question is how to rank evidence when stdlib practice (survey), core docs, FPIL and Mathlib disagree. The brief treats the stdlib as the gold standard, but `src/Lean` is older and less curated.
- **Q0c ★ What counts as evidence that code is *good*, not just common?** The current research shows what conventional Lean looks like, but not what separates good Lean code from poor. Four reasons:
  - **Frequency isn't quality.** [stdlib-survey.md](stdlib-survey.md) shows how often each pattern occurs. "Std does X 97% of the time" shows a norm, not that X is better.
  - **The gold standard is mostly proofs.** Init and Std have about 5 theorems per def. Ordinary program code lives in Lake and `src/Lean`, which nobody presents as exemplary, and Lake breaks `style.md` in places ([survey §4](stdlib-survey.md#4-formatting)).
  - **Few sources show bad Lean code.** The Lean core documents and the survey give no "this is bad, here's why" example. FPIL is the exception: about 15 statements call a pattern poor style, buggy, confusing, noisy or a "code smell", each next to a better version ([fpil](notes/fpil.md#explicit-donts)). Most of its other advice is hedged with "typically" and "usually".
  - **On design questions, only other languages speak.** Lean sources are silent on errors, recursion, testing and module structure ([topic-map.md](topic-map.md)).

  To decide: which kinds of evidence count, and how to weigh them against measured frequency. Candidate sources, in rough order of value:
  1. Review comments that ask for changes on lean4, Std, Batteries and Mathlib pull requests. Search for "style", "nit", "please use" and "idiomatic".
  2. Cleanup and refactor commits, which show before/after pairs (`git log --grep='style\|cleanup\|refactor'`; needs full, not shallow, clones).
  3. Zulip threads where someone asks "how should I write this?" and gets corrected, especially in `#new members` and `#lean4`.
  4. Linter warnings and the code changes that fixed them. Each linter encodes a "poor" pattern.
  5. Two or three non-mathematical libraries "in the wild" read with a reviewer's eye, not counted ([survey](stdlib-survey.md) has three cloned).
  6. Sampled defect rates, as in [lean-quality-indicators](notes/lean-quality-indicators.md). It defines a defect precisely (an unnecessary hypothesis; a theorem already in Mathlib), has a model judge 1000 uniformly sampled theorems per library, and reports rates with 95% intervals and a blind rerun (κ = 0.92). The rates separate libraries: 3.1% of Mathlib theorems have an unnecessary hypothesis, 20.3% of Anthropic's FLT formalization. Its reports list each flag with a reason, so they are bad examples too. Limits:
     - maths libraries and theorem statements only; program code would need an indicator of its own;
     - the verdicts are a model's, checked by hand on only a handful of flags;
     - the repo appeared on 2026-10-20 and its numbers are preliminary.

  The output would be real good/bad pairs, from which each rule can be argued in bbatsov's format. FPIL's 15 pairs are a first instalment.

  Partly addressed (2026-10-20). [author-survey.md](author-survey.md) splits FRO program code by first author, so a pattern found across all nine columns counts as a convention and one found in a single column as that author's habit. This also answers the worry that the gold standard is mostly proofs: 395k lines of FRO program code exist, spread over many authors.

- **Q0b Proof style in scope?** Libraries that mix programs and proofs (CSLib, Std's lemma files) need some proof rules. Should the guide include proof rules, or defer to core-style's tactic section and Mathlib ([community-cslib](notes/community-cslib.md), [lean-core-style](notes/lean-core-style.md))?

## Naming

- **Q1 ★ The failure-variant family.** Should `?`/`!`/`D` plus a proof-taking variant become a rule for library APIs? Questions within it:
  - which variant is the unsuffixed name;
  - whether `D` is stable enough to state (FPIL teaches it; core-naming doesn't list it);
  - whether to require a safe twin whenever a `!` exists (Ruby's rule).

  Sources: [lean-core-naming](notes/lean-core-naming.md), [fpil](notes/fpil.md), [bbatsov-ruby](notes/bbatsov-ruby.md), [rust-api-guidelines](notes/rust-api-guidelines.md). Survey §1 has the stdlib counts. FPIL makes the unsuffixed name the proof-taking variant (`List.head`), but its own code defines 18 `?` functions and no `!` or `D` ones.
- **Q2 Names no Lean source covers:**
  - instances (anonymous vs named, and the naming scheme for named ones);
  - constructors;
  - modules and files;
  - `ofX`/`toX` conversions;
  - monadic `M` variants;
  - private helpers (`go`, `loop`, `Impl`, `Aux`).

  Survey §1 and §8 record what the stdlib does. FPIL's code: all 133 instances anonymous; helpers named `helper`/`go`/`loop` (local) or `…Helper`/`…Loop` (top level); `Many.fromList` where the stdlib has `ofList` ([fpil](notes/fpil.md#naming)).
- **Q3 Predicates.** Core says `Is` for `Prop`-valued predicates. What about `Bool`-valued tests (`isEmpty`)? Ruby forbids `is_`, while F# and Lean use it ([lean-core-naming](notes/lean-core-naming.md), [bbatsov-ruby](notes/bbatsov-ruby.md)). FPIL uses `isX` for `Bool` and `IsX` for inductive `Prop`s. For programs it advises: "it's easiest to stick to Boolean functions rather than propositions" ([fpil](notes/fpil.md)).

## Layout

- **Q4 ★ `fun x =>` vs `fun x ↦`.** Core prescribes `=>` and Mathlib slightly prefers `↦`. Mathlib's 2025 poll ended in "general disagreement" ([lean-core-style](notes/lean-core-style.md), [zulip-style-misc](notes/zulip-style-misc.md)). Survey §2 has the stdlib counts.
- **Q5 ★ Write layout rules, or defer to the coming formatter?** The FRO roadmap promises one, but none is released ([fro-blog](notes/fro-blog.md), [zulip-formatter](notes/zulip-formatter.md)). Guides in languages with formatters say little about layout in prose ([ocaml-guidelines](notes/ocaml-guidelines.md), [rust-style-guide](notes/rust-style-guide.md)). One option is to state rules now and mark them "until the formatter decides".
- **Q6 Line length and operator position.**
  - Line length: none (core), 100 (Mathlib, linted), 90 (leanfmt). Survey §4 has the distribution.
  - Operator position: at the end of the line (core, Mathlib) or at the start of the next (leanfmt) ([community-leanfmt](notes/community-leanfmt.md)).
  - Match-arm alignment: core allows it, while Elm, F# and Rust forbid layout that depends on name length.

  FRO practice: p95 line length is 84–100 for every author, and 1–5% of each author's lines exceed 100 ([author-survey](author-survey.md)). Split headers continue at +4 for seven of nine columns; Lake uses +2.

## Functions

- **Q7 `where` vs `let rec` vs `private def`** for helpers. No source covers this; survey §3 has the counts. FPIL's code uses `let rec` 15 times, `where` once and `private` never.

  Evidence (2026-10-20): FRO code prefers `where` helpers named `go` in eight of nine author columns. The largest contributor moved from `let rec loop` before 2024 to `where go` after ([author-survey](author-survey.md#consistent-across-authors)).

- **Q8 Point-free style and pipelines** (`∘`, `<|`, `|>`, `·`). Other languages say not to overdo it. FPIL says when each is worth it: `|>` for "an input that is successively refined", `<|` against "many nested parentheses", `·` for "very simple" lambdas, `f <$> E` over `pure f <*> E` ([fpil](notes/fpil.md#functions-and-expressions)). No Lean source covers point-free style or `∘`.

## Data modelling

- **Q9 ★ Bundled vs unbundled invariants.**
  - Std's `DHashMap` says "When in doubt, prefer `DHashMap`" (bundled).
  - FPIL says subtypes and propositions over indexed families.
  - Spitters and van der Weegen say bundling costs flexibility.

  The decision: default to a structure with a proof field, a subtype, or plain data plus separate lemmas? When is an indexed family worth its call-site cost ([bundled-unbundled](notes/bundled-unbundled.md), [fpil](notes/fpil.md), [cpdt-lean](notes/cpdt-lean.md))?

  FPIL's full position ([fpil](notes/fpil.md#data-modelling)):
  - Subtypes are "a two-edged sword": keep them "internal to a library", with an API that discharges the proofs.
  - Indexed families: rarely, with four drawbacks argued. Frequent `▸` casts to unstick them are "a code smell". They are right for APIs that "resemble some other language", and even then as "the core [...] rather than its user interface".
  - `Fin` bundles index and proof, which "can make code easier to read".
- **Q10 `abbrev` vs `def` vs `structure` for domain types.** Cornell encourages type aliases, while F# warns against them for domain types, and Mathlib prefers wrapper structures over `irreducible` ([fsharp-style](notes/fsharp-style.md), [mathlib-style](notes/mathlib-style.md)).

  FPIL settles three cases with reasons: `abbrev` for propositions that tactics must unfold; `abbrev` for monad stacks, so `ReaderT`'s instances stay visible; `abbrev` so dot notation sees through. Types that get their own instances are `def`s. Single-field wrapper structures are free at run time, but "can make it more difficult to read proofs" ([fpil](notes/fpil.md#data-modelling)). No rule for domain types in general.
- **Q11 `deriving` policy.** Which instances should be derived by default (`Repr`, `BEq`, `Hashable`, `DecidableEq`, `Inhabited`)? Survey §8 has the counts. FPIL argues for deriving over hand-written instances: it is less tedious, instances follow type changes, and reviews stay readable. A hand-written `Ord` is fine. It never says which classes to derive by default; its code derives `Repr`, `BEq` and `Hashable` only ([fpil](notes/fpil.md#data-modelling)).

## Errors and effects

- **Q12 ★ Error-reporting policy for libraries:** `Except ε` vs `IO`/`EIO` exceptions vs `Option` vs `panic!`. Only FPIL ranks them, and only partly:
  - evidence arguments first, then `?`, then `!`;
  - `Except` when callers need to know why;
  - `MonadExcept` to avoid tying code to one encoding;
  - an applicative `Validate` to report every input error at once ([fpil](notes/fpil.md#error-handling)). Other languages split: Scala and Rust put errors in the type, while F# and Databricks push back on monadic errors ([fsharp-style](notes/fsharp-style.md), [scala-effective](notes/scala-effective.md)). Survey §6 has the stdlib practice.

  FRO practice ([author-survey](author-survey.md#author-dependent-no-fro-convention)): IO-facing code (Verso, Std.Http, Lake) uses `throw` with `IO.userError` plus `Except`. `MonadExcept`, which FPIL recommends, is close to absent in every column.

- **Q13 Error types and `panic!`.** Should errors be inductive types or `String`? Is `get!`/`panic!` acceptable in application code? Should every failure mode be documented, as in Rust's "Panics" section? FPIL's examples throw an inductive `Err` from a backend and render "a friendly string error" in the frontend. Validation errors are `Field × String`, and it recommends error trees over flat lists. It states no policy and never uses `panic!` ([fpil](notes/fpil.md#error-handling)).
- **Q14 Monad-stack design and resource handling for applications.** FPIL chapter 6 now covers `ReaderT`/`StateT` application structure ([fpil](notes/fpil.md#do-notation-and-effects)):
  - a pure core with a monadic shell;
  - a reader for configuration;
  - stacks as `abbrev`s of stdlib transformers;
  - effect classes, with the warning that signatures can be "more polymorphic than it should be" because transformer order changes meaning;
  - `modify` over `get`/`set`.

  No Lean source covers `withFile`/`finally` (FPIL relies on finalizers) or `Task`.

  The Reference gives a rule for concurrency: `IO` alone for sequential programs, `Task`s for parallel ones, `Async` for programs that mostly wait on events or I/O. It also says to use `IO.checkCanceled` in impure tasks ([lean-reference](notes/lean-reference.md#concurrency-read-2026-10-20)).

## Termination and proofs

- **Q15 ★ Recursion policy for programs.** No source gives a rule for choosing among:
  - structural recursion;
  - `termination_by`;
  - fuel;
  - `partial_fixpoint`;
  - `partial`.

  Should `partial` require a comment? FPIL says "no alternative"; Idris says `partial` is for development and debugging only; Breitner prefers structural recursion when proofs are planned ([fpil](notes/fpil.md), [idris2-docs](notes/idris2-docs.md), [fro-blog](notes/fro-blog.md)). Survey §7 has the counts.

  FPIL's full position ([fpil](notes/fpil.md#termination-and-recursion-q15)):
  - A recommended workflow, close to Idris: start `partial`, test, switch to `termination_by` with `have … := by sorry`, re-test, then prove.
  - `partial` is acceptable when no reasoning about the function is needed.
  - `repeat`/`while` and folds avoid `partial` altogether.
- **Q16 ★ When not to prove.** No source states a rule ([proof-engineering](notes/proof-engineering.md), [correct-by-construction](notes/correct-by-construction.md)). Candidate positions:
  - prove what types can enforce cheaply;
  - comment the other invariants;
  - test the rest.

  FPIL is the nearest Lean statement: proofs "render many tests unnecessary", but "proving theorems about programs can be time consuming and expensive, so other tools are often more economical". It adds: keep the slow version as "an executable specification", and test before proving ([fpil](notes/fpil.md#invariants-and-proofs-about-programs-q0b-q16-q18)).
- **Q17 Where proofs live:** in the same file after the definitions, or a `Lemmas.lean` split as in Std? Survey §13 has the stdlib practice.
- **Q18 Stock automation vs custom tactics in libraries.** Core and Mathlib prefer stock `grind`/`omega`/`simp`, while CPDT argues for program-specific automation ([cpdt-lean](notes/cpdt-lean.md)).
  - FPIL sides with stock automation: "The short, highly-automated proof script is typically easier to maintain". Its final proofs are `fun_induction … <;> grind`.
  - Its intermediate proofs use unsqueezed non-terminal `simp`, which core-style and Mathlib's `flexible` linter reject ([fpil](notes/fpil.md)).

## Docs and tests

- **Q19 Docstring form.** "Indicative mood" (core-style) or a noun-phrase fragment (doc-style)? Also delimiter placement ([lean-core-doc-style](notes/lean-core-doc-style.md), [zulip-style-misc](notes/zulip-style-misc.md)).

  FRO authors split: columns A, C and D lead with a verb ("Returns"), and columns B, E, F and G more often with a noun phrase ("The") ([author-survey](author-survey.md)). Coverage of public defs is 34–57%, except Std.Http at 98.5%.

- **Q20 Docstrings on private declarations, and required sections** ("Errors", "Panics", examples). FPIL: "`example` declarations are best paired with comments that explain how the example illustrates the concepts of the library". Its own code has no docstrings.
- **Q21 ★ Testing conventions.** No source gives a mechanism. The decision covers the mechanism (`#guard_msgs`, `#guard`, `example`, `#eval` in library files, or a `lake test` driver), the directory layout, and property-based testing (`plausible`).

  FPIL supplies principles only ([fpil](notes/fpil.md#tests-q21)):
  - types and proofs remove some tests;
  - test before proving;
  - test what proofs can't see, such as copying, in a built executable;
  - `#eval` on `IO` re-runs "at unpredictable times".

  Evidence now (2026-10-20, [testing-practice](notes/testing-practice.md)):
  - The Reference names `#guard_msgs` files as Lake test drivers and warns that `#eval` tests under the module system need `meta import`.
  - Practice: a `<Pkg>Test` library as `testDriver` in 25 of 34 sampled repos and in FRO repos, Batteries and Mathlib; an executable driver for IO tests.
  - Plausible for property tests. Verso's Errata is FRO-built but not a standalone package.
  - The mechanism and layout are now decidable. Still open: a rule for property tests, and whether to mention Errata.

## API and tooling

- **Q22 Visibility.** When to use `private`, `protected`, `Internal` namespaces, or the module system's `public`/`@[expose]` ([lean-core-naming](notes/lean-core-naming.md), [lean-reference](notes/lean-reference.md)). Survey §10 has the counts.

  The Reference: use `public section` rather than `@[expose] public section` for "programs that will be run but not reasoned about"; drop `public` and `@[expose]` where possible to avoid rebuilds; keep `meta` minimal ([lean-reference](notes/lean-reference.md#module-system-guidance-for-library-authors-read-2026-10-20)). FRO authors differ on `private` (0.2–26% of declarations).

- **Q23 `open` and `variable` hygiene.** Choose between top-level `open` and `open … in`, and decide on `variable` blocks (agda-stdlib restricts them; Carneiro lists heavy `variable` use as a Mathlib habit to avoid) ([agda-stdlib-style](notes/agda-stdlib-style.md), [zulip-style-misc](notes/zulip-style-misc.md)).
- **Q24 Performance attributes.** When to use `@[inline]`, `@[specialize]`, `@[implemented_by]`, `@[extern]` and `unsafe`. No official guidance exists; survey §9 has the counts.

  Author-dependent (2026-10-20): `@[inline]` runs from 0.13 per thousand lines (column B) to 34–36 (columns D and E), and `@[specialize]` is at most 1.4 per thousand lines everywhere ([author-survey](author-survey.md#author-dependent-no-fro-convention)). FRO code has no shared convention to adopt here.

- **Q25 Linter set.** Recommend Mathlib's `linter.mathlibStandardSet`, a subset of it, or core linters only ([mathlib-linters](notes/mathlib-linters.md))? Also: a warning-free policy and a deprecation window (Mathlib uses 6 months).
- **Q26 Guide format.** bbatsov's anchored rules with good/bad pairs, possibly with Rust-style stable IDs and a checklist ([bbatsov-clojure](notes/bbatsov-clojure.md), [rust-api-guidelines](notes/rust-api-guidelines.md)). Also the licence: CC BY 4.0 would allow adapting the CC BY sources, but not the NC-licensed ones (Databricks, PureScript), and not ocaml.org (share-alike) unless the guide is CC BY-SA ([index](index.md)).
- **Q27 Auto-bound implicits.** Should general-purpose code set `autoImplicit false`?
  - Core defaults to `true` (`src/Lean/Elab/AutoBound.lean` at `3a685e6`).
  - Mathlib turns it off globally ([mathlib-linters](notes/mathlib-linters.md)), and Std turns it off in 70 of 499 files.
  - FPIL, the main teaching text, relies on auto-bound implicits throughout and presents them as a convenience. It notes one trap, where a mistyped or misplaced name silently becomes a new implicit ([fpil](notes/fpil.md#functions-and-expressions)).
  - A related choice is `relaxedAutoImplicit`, which limits auto-binding to single letters plus digits.
