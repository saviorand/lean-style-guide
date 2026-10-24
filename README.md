# A Lean Style Guide for Software

*Community draft, October 2026.*

This guide describes how to write programs, libraries and tools in Lean 4, focusing on general-purpose software, not math. 

It's a community project, not an official document of the Lean FRO or of Mathlib. 

Main resources used here are Lean's own [style guide](https://github.com/leanprover/lean4/blob/master/doc/std/style.md) and [naming conventions](https://github.com/leanprover/lean4/blob/master/doc/std/naming.md) for the standard library. Some rules were borrowed from other language ecosystems where they make sense for Lean, e.g Haskell, OCaml

## Guiding principles

- Names should be guessable ([Lean naming conventions][cn-intro]).
- Give each claim the strongest guarantee it admits: a type, then a theorem, then a property test, then an example ([Paul Butcher, issue #1][issue-1]).

## Rules

"Use", "Write" and "Don't" mean always, "Prefer" and "Avoid" mean usually, and "Consider" means it's often worth it. Once Lean's official formatter is released ([FRO roadmap][fro-roadmap]), its output takes precedence over the layout rules.

### [Data modelling](guide/data.md)

- Use a `structure` for a value with several parts and an `inductive` for alternatives ([`data-structure-inductive`](guide/data.md#data-structure-inductive)).
- Define structures with named fields instead of passing tuples around ([`data-own-types`](guide/data.md#data-own-types)).
- Wrap a primitive in a single-field structure when its values must not be mixed with others, such as IDs ([`data-wrappers`](guide/data.md#data-wrappers)).
- Check a value once where it enters the program, and pass a type that carries the check ([`data-boundary`](guide/data.md#data-boundary)).
- Use `abbrev` for exact synonyms, `structure` for new domain types, and never `def` for type synonyms ([`data-abbrev`](guide/data.md#data-abbrev)).
- Use `extends` only when one structure clearly "is a" kind of another ([`data-extends`](guide/data.md#data-extends)).
- Avoid indexed families in APIs, except in code that resembles a typed language ([`data-indexed-families`](guide/data.md#data-indexed-families)).
- Derive instances instead of writing them, and derive `Repr` for every data type ([`data-deriving`](guide/data.md#data-deriving)).
- Build structures with named fields unless the order of the fields is obvious ([`data-constructors`](guide/data.md#data-constructors)).
- Update a structure with `{ s with field := value }` instead of copying fields by hand ([`data-update`](guide/data.md#data-update)).

### [Effects and `do` notation](guide/effects.md)

- Keep program logic in pure functions and `IO` in a thin outer layer ([`effects-pure-core`](guide/effects.md#effects-pure-core)).
- Pass shared configuration through `ReaderT`, and define the application's monad with `abbrev` ([`effects-config`](guide/effects.md#effects-config)).
- Put acquire and release in a `with…` helper built with `try … finally` ([`effects-resources`](guide/effects.md#effects-resources)).
- Use `IO` for sequential code, `Task` for parallel computation and `Async` for programs that mostly wait on I/O ([`effects-concurrency`](guide/effects.md#effects-concurrency)).
- Don't `#eval` actions with side effects in library files ([`effects-eval`](guide/effects.md#effects-eval)).
- Handle special cases first and return early, so the main path isn't nested ([`do-early-return`](guide/effects.md#do-early-return)).
- Unwrap an `Option` with `let some x := e | fallback` when the failure case is short ([`do-let-else`](guide/effects.md#do-let-else)).
- Use `let mut` and `for` when they're clearer than a fold or a state monad ([`do-mutation`](guide/effects.md#do-mutation)).
- Use `modify` to update state, instead of `get` followed by `set` ([`effects-modify`](guide/effects.md#effects-modify)).
- Use `(← action)` inline for a result you use once, and `let x ← action` otherwise ([`do-nested-actions`](guide/effects.md#do-nested-actions)).
- End `do` blocks with `return x`, and use `pure x` outside them ([`do-return`](guide/effects.md#do-return)).

### [Error handling](guide/errors.md)

- Return `Option` for one obvious failure and `Except` when the caller needs to know which failure happened ([`errors-option-except`](guide/errors.md#errors-option-except)).
- Give a library an inductive error type with a `ToString` instance ([`errors-types`](guide/errors.md#errors-types)).
- In `IO` code, throw errors instead of returning default values ([`errors-io`](guide/errors.md#errors-io)).
- Don't replace a missing value with a default when its absence can mean that the program is misconfigured ([`errors-defaults`](guide/errors.md#errors-defaults)).
- Use `panic!` and `!` functions only when essential: for bugs, where you can't pass a proof instead, and never to reject bad input ([`errors-panics`](guide/errors.md#errors-panics)).
- Say in the docstring how a function fails when its type doesn't already say so ([`errors-document`](guide/errors.md#errors-document)).

### [Logging](guide/logging.md)

- Log where the code makes a decision that its result can't express ([`logging-decisions`](guide/logging.md#logging-decisions)).
- Record the value that decided the branch, not just the outcome ([`logging-values`](guide/logging.md#logging-values)).
- Log what was asked for, since a span records only the route ([`logging-requests`](guide/logging.md#logging-requests)).
- Don't log ordinary success when a span already records the request ([`logging-success`](guide/logging.md#logging-success)).

### [API design and visibility](guide/api.md)

- Make public only what callers need ([`api-surface`](guide/api.md#api-surface)).
- Use the module system in libraries, with a plain `public section` in program files ([`api-modules`](guide/api.md#api-modules)).
- Mark helpers `private`, or put them in an `Internal` namespace ([`api-private`](guide/api.md#api-private)).
- Mark a declaration `protected` if its short name would clash after `open` ([`api-protected`](guide/api.md#api-protected)).
- Deprecate a public declaration before you rename, remove or change it, and note every such change in the changelog ([`api-deprecation`](guide/api.md#api-deprecation)).
- Avoid `variable` in program code ([`api-variable`](guide/api.md#api-variable)).

### [Naming](guide/naming.md)

- Use `UpperCamelCase` for types and namespaces, `lowerCamelCase` for functions, values and fields, and `snake_case` for theorems ([`naming-case`](guide/naming.md#naming-case)).
- Put the functions about a type in the namespace named after the type ([`naming-namespaces`](guide/naming.md#naming-namespaces)).
- Name `Bool` functions as questions, as in `isEmpty`, and `Prop` predicates with `Is`, as in `IsSorted` ([`naming-predicates`](guide/naming.md#naming-predicates)).
- Mark failure in the name with `?` for an `Option`, `!` for a panic and `D` for a default ([`naming-failure`](guide/naming.md#naming-failure)).
- Name conversions `toX` and `ofX`, never `fromX` ([`naming-conversions`](guide/naming.md#naming-conversions)).
- Add `M` to the name of a variant that runs in a monad, as in `mapM` and `forM` ([`naming-monadic`](guide/naming.md#naming-monadic)).
- Don't name a variant of a public function by adding `'` ([`naming-primes`](guide/naming.md#naming-primes)).
- Write acronyms of four or more letters as words, as in `Json`, and shorter ones in one case, as in `IO` ([`naming-acronyms`](guide/naming.md#naming-acronyms)).
- Use short local names only by convention, such as `xs` for arrays, `acc` for accumulators and `i` for indices ([`naming-locals`](guide/naming.md#naming-locals)).
- Leave instances anonymous ([`naming-instances`](guide/naming.md#naming-instances)).
- Name packages in lowercase and modules in `UpperCamelCase`, with file paths that match ([`naming-files`](guide/naming.md#naming-files)).

### [Functions](guide/functions.md)

- Give every top-level definition explicit argument types and an explicit result type ([`functions-signatures`](guide/functions.md#functions-signatures)).
- Make an argument implicit, with braces, when later arguments determine it ([`functions-implicit`](guide/functions.md#functions-implicit)).
- Turn off `autoImplicit`, so a misspelled type name is an error ([`functions-auto-implicit`](guide/functions.md#functions-auto-implicit)).
- Put single-use helpers in a `where` clause, and name a recursive helper `go` ([`functions-helpers`](guide/functions.md#functions-helpers)).
- Give optional parameters default values, and put options that several functions share in a structure ([`functions-options`](guide/functions.md#functions-options)).
- Pass `Bool` arguments by name, as in `(quiet := true)` ([`functions-bool-args`](guide/functions.md#functions-bool-args)).
- Use `|>`, `|>.` and `<|` to avoid nested parentheses, and don't use `$` ([`functions-pipelines`](guide/functions.md#functions-pipelines)).
- Write lambdas as `fun x => e`, never with `λ` or `↦` ([`functions-lambdas`](guide/functions.md#functions-lambdas)).

### [Type classes and instances](guide/classes.md)

- Define a type class only when several types will have instances and code is generic over them ([`classes-when`](guide/classes.md#classes-when)).
- Ask for the weakest class a function needs, so it works for more types ([`classes-weakest`](guide/classes.md#classes-weakest)).
- Make `BEq` agree with `Hashable`, and `Ord` with `LT` and `LE` ([`classes-consistent`](guide/classes.md#classes-consistent)).
- Add a coercion only when every source value has an obvious counterpart in the target type ([`classes-coercions`](guide/classes.md#classes-coercions)).
- For a recursive type, write the recursive function in the type's namespace and have the instance call it ([`classes-recursive`](guide/classes.md#classes-recursive)).
- Write instances with `where`, one method per line ([`classes-where`](guide/classes.md#classes-where)).

### [Collections](guide/collections.md)

- Use `Array` for sequences you build, index or update, and `List` for small ones you take apart from the front ([`collections-array`](guide/collections.md#collections-array)).
- Keep a single reference to an array you're updating, so Lean can update it in place ([`collections-sharing`](guide/collections.md#collections-sharing)).
- Loop over elements rather than indices, and prefer `xs[i]?` or a proof to `xs[i]!` ([`collections-iterate`](guide/collections.md#collections-iterate)).
- Use `Std.HashMap` for lookups and `Std.TreeMap` when key order matters ([`collections-maps`](guide/collections.md#collections-maps)).

### [Recursion and termination](guide/recursion.md)

- Prefer structural recursion, and give a measure with `termination_by` when the recursion isn't structural ([`recursion-structural`](guide/recursion.md#recursion-structural)).
- Mark a function `partial` only when it might not terminate, or nobody knows whether it does ([`recursion-partial`](guide/recursion.md#recursion-partial)).
- Use `for`, `while` and `repeat` instead of recursive helpers that only loop ([`recursion-loops`](guide/recursion.md#recursion-loops)).
- Use loops or accumulators for recursion over large inputs ([`recursion-deep`](guide/recursion.md#recursion-deep)).

### [Proofs about programs](guide/proofs.md)

- Prove claims as theorems by default, and fall back to property tests and examples only when a proof doesn't work out ([`proofs-first`](guide/proofs.md#proofs-first)).
- Keep the simple version of an optimized function as its specification, and prove that the two agree ([`proofs-spec`](guide/proofs.md#proofs-spec)).
- Time-box a proof, and if it fails, write a property test with a comment that records the obstacle ([`proofs-timebox`](guide/proofs.md#proofs-timebox)).
- When a module with property tests changes, check whether each property can now be proved ([`proofs-recheck`](guide/proofs.md#proofs-recheck)).
- Keep short lemmas next to their definitions, and move longer proofs to their own module ([`proofs-location`](guide/proofs.md#proofs-location)).
- Prefer `grind`, `omega` and `simp` to long manual proofs, and squeeze `simp` calls that aren't the last step ([`proofs-automation`](guide/proofs.md#proofs-automation)).
- Name a theorem after what it states, in `snake_case`, starting from the conclusion ([`proofs-names`](guide/proofs.md#proofs-names)).
- Don't commit `sorry` ([`proofs-sorry`](guide/proofs.md#proofs-sorry)).

### [Testing](guide/testing.md)

- Test what types and proofs don't cover ([`tests-coverage`](guide/testing.md#tests-coverage)).
- Don't write tests that only restate literals from the source ([`tests-literals`](guide/testing.md#tests-literals)).
- Put tests in a `<Pkg>Test` library run by `lake test`, or in a `test/` subproject when a library's tests need extra dependencies ([`tests-library`](guide/testing.md#tests-library)).
- Check results with `#guard_msgs` and `#guard` ([`tests-guard-msgs`](guide/testing.md#tests-guard-msgs)).
- Compare whole outputs with saved copies only where their exact form is the contract, and review every regenerated copy ([`tests-golden`](guide/testing.md#tests-golden)).
- Use an executable test driver for tests that run `IO` ([`tests-runtime`](guide/testing.md#tests-runtime)).
- Test properties of your own code that aren't proved yet on random inputs, with `Plausible.Testable.check` rather than the `plausible` tactic ([`tests-property`](guide/testing.md#tests-property)).
- In test files that are modules, import the code under test with `meta import` ([`tests-meta-import`](guide/testing.md#tests-meta-import)).

### [Documentation](guide/documentation.md)

- Write a docstring when the name and type leave something unsaid, and not one that restates them ([`docs-when`](guide/documentation.md#docs-when)).
- Begin a file with a module docstring, with a `#` title, when the file needs more explanation than its code gives ([`docs-module`](guide/documentation.md#docs-module)).
- Start a function's docstring with a verb such as "Returns", and a type's with a noun phrase ([`docs-summary`](guide/documentation.md#docs-summary)).
- Show short examples in docstrings, and check them with tests ([`docs-examples`](guide/documentation.md#docs-examples)).
- Put a short docstring on one line, and the delimiters of a longer one on lines of their own ([`docs-layout`](guide/documentation.md#docs-layout)).

### [Comments](guide/comments.md)

- Explain why in comments, and don't restate what the code does ([`comments-why`](guide/comments.md#comments-why)).
- Write down every invariant that your types don't enforce ([`comments-invariants`](guide/comments.md#comments-invariants)).
- Leave history and dead code to version control, and unfinished work to the issue tracker ([`comments-history`](guide/comments.md#comments-history)).

### [Macros and notation](guide/macros.md)

- Get standard notation by implementing classes such as `Add` and `GetElem` ([`macros-classes`](guide/macros.md#macros-classes)).
- Use macros for syntax sugar, and elaborators when the translation needs types or decisions ([`macros-macro-or-elab`](guide/macros.md#macros-macro-or-elab)).
- Make notation `scoped` unless every user of your library needs it ([`macros-scoped`](guide/macros.md#macros-scoped)).
- Don't add `macro_rules` that cover only some uses of existing syntax ([`macros-overlap`](guide/macros.md#macros-overlap)).
- Make your notation appear in Lean's output the way users write it ([`macros-output`](guide/macros.md#macros-output)).

### [Performance and low-level code](guide/performance.md)

- Don't add `@[inline]` or `@[specialize]` without a measurement that shows they help ([`perf-measure`](guide/performance.md#perf-measure)).
- Prefer `@[csimp]` with a proof to `@[implemented_by]`, which Lean doesn't check ([`perf-implemented-by`](guide/performance.md#perf-implemented-by)).
- Keep `unsafe` code in small functions with a safe interface, and say in a comment why it's needed ([`perf-unsafe`](guide/performance.md#perf-unsafe)).
- Keep `@[extern]` declarations in one small module behind a safe Lean API ([`perf-ffi`](guide/performance.md#perf-ffi)).

### [Projects and tooling](guide/projects.md)

- Start from the layout `lake new` creates, with a small `Main.lean` ([`project-layout`](guide/projects.md#project-layout)).
- Commit `lean-toolchain` and `lake-manifest.json`, and require dependencies at release tags ([`project-dependencies`](guide/projects.md#project-dependencies)).
- Declare files that you embed with `include_str` as Lake inputs in the library's `needs`, or editing them rebuilds nothing ([`project-embedded-files`](guide/projects.md#project-embedded-files)).
- Set `autoImplicit = false` in the Lake configuration ([`project-options`](guide/projects.md#project-options)).
- Check for warnings in CI with `lake build --wfail`, and don't set `warningAsError` in a library ([`project-warnings`](guide/projects.md#project-warnings)).
- Keep Lean's built-in linters on ([`project-linters`](guide/projects.md#project-linters)).
- Don't mix reformatting with other changes ([`project-formatting`](guide/projects.md#project-formatting)).

### [Source code layout](guide/layout.md)

- Order each file as licence comment, `module`, imports, module docstring, then code ([`layout-file`](guide/layout.md#layout-file)).
- Indent with two spaces, never with tabs ([`layout-indentation`](guide/layout.md#layout-indentation)).
- Keep lines under 100 characters ([`layout-line-length`](guide/layout.md#layout-line-length)).
- Put single spaces around `:`, `:=`, `|`, `::`, `=>`, `←` and infix operators ([`layout-spaces`](guide/layout.md#layout-spaces)).
- Start top-level commands at column 0, and don't indent inside `namespace` or `section` ([`layout-top-level`](guide/layout.md#layout-top-level)).
- Indent the continuation lines of a long declaration header by four spaces, and never start a line with the colon ([`layout-headers`](guide/layout.md#layout-headers)).
- Split long expressions at argument boundaries, with infix operators at the end of the line ([`layout-splitting`](guide/layout.md#layout-splitting)).
- Put `match` arms at the column of the `match`, without padding to align the arrows ([`layout-match`](guide/layout.md#layout-match)).
- Start `where`, `deriving`, `termination_by` and `decreasing_by` at the column of the declaration they belong to ([`layout-where`](guide/layout.md#layout-where)).
- In a multi-line structure instance, put `{` at the end of the line before it and `}` on its own line ([`layout-structure-instances`](guide/layout.md#layout-structure-instances)).
- Put `do` on the same line as the `:=`, `=>` or `←` before it ([`layout-do`](guide/layout.md#layout-do)).

## Contributing

Open an issue or a pull request. Every Lean example has to compile:

```sh
python3 tools/check_examples.py
```

## Licence

The text of this guide is licensed under [CC BY 4.0](LICENSE). The code examples, [tools/](tools/) and [research/scripts/](research/scripts/) are licensed under [Apache-2.0](LICENSE-CODE). Material quoted in [research/](research/) stays under its original licence, listed for each source in [research/index.md](research/index.md).

[cn-intro]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#standard-library-naming-conventions
[fro-roadmap]: https://lean-lang.org/fro/roadmap/y4-1/
[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
