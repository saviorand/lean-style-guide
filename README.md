# A Lean Style Guide for Software

*Community draft, October 2026. Targets Lean 4.35.*

This guide describes how to write programs, libraries and tools in Lean 4. It covers layout, naming, structure, documentation and testing. It's a community project, not an official document of the Lean FRO or of Mathlib. It builds on Lean's own [style guide](https://github.com/leanprover/lean4/blob/master/doc/std/style.md) and [naming conventions](https://github.com/leanprover/lean4/blob/master/doc/std/naming.md) for the standard library, and leaves formalized mathematics to [Mathlib's style guide](https://leanprover-community.github.io/contribute/style.html). The evidence behind each rule is in [research/](research/).

## Introduction

### Guiding principles

- Code is read far more often than it is written, so the rules favour the reader.
- Names should be guessable.
- Where an established practice competes with a subjectively better one, follow the established practice.
- Put cheap guarantees in types, test the rest, and prove what matters most.

*Sources: [Clojure guide][clj-principles], [Lean naming conventions][cn-intro], [FPIL][fpil-proofs], [Simple Haskell][simple-haskell], [Boring Haskell Manifesto][boring-haskell].*

### Consistency

Consistency with this guide matters. Consistency within a project matters more, and consistency within one file matters most. Don't break backward compatibility to follow a rule, and don't rewrite old code only to match the guide.

*Sources: [PEP 8][pep8-consistency], [Haskell (Kowainik)][kowainik-existing].*

### Rule format

The [list of rules](#rules) below gives each rule in one line. Its link leads to a chapter page with the reasons, usually a `-- bad` and a `-- good` example, and a line of sources. Every rule has an anchor you can link to in code review.

"Use", "Write" and "Don't" mean always. "Prefer" and "Avoid" mean usually. "Consider" means it's often worth it. Every example compiles with Lean 4.35.0, including the bad ones. FPIL is [*Functional Programming in Lean*](https://lean-lang.org/functional_programming_in_lean/), and "FRO practice" links to measurements of the Lean FRO's own program code.

Lean has no official formatter yet. When one is released, its output takes precedence over the layout rules here.

## Rules

### [Source code layout](guide/layout.md)

- [Indent with two spaces, never with tabs.](guide/layout.md#layout-indentation)
- [Keep lines under 100 characters.](guide/layout.md#layout-line-length)
- [Put single spaces around `:`, `:=`, `|`, `::`, `=>`, `←` and infix operators.](guide/layout.md#layout-spaces)
- [Start top-level commands at column 0, and don't indent inside `namespace` or `section`.](guide/layout.md#layout-top-level)
- [Indent the continuation lines of a long declaration header by four spaces, and never start a line with the colon.](guide/layout.md#layout-headers)
- [Split long expressions at argument boundaries, with infix operators at the end of the line.](guide/layout.md#layout-splitting)
- [Put `match` arms at the column of the `match`, without padding to align the arrows.](guide/layout.md#layout-match)
- [Start `where`, `deriving`, `termination_by` and `decreasing_by` at the column of the declaration they belong to.](guide/layout.md#layout-where)
- [In a multi-line structure instance, put `{` at the end of the line before it and `}` on its own line.](guide/layout.md#layout-structure-instances)
- [Put `do` on the same line as the `:=`, `=>` or `←` before it.](guide/layout.md#layout-do)
- [Order each file as licence comment, `module`, imports, module docstring, then code.](guide/layout.md#layout-file)

### [Naming](guide/naming.md)

- [Use `UpperCamelCase` for types and namespaces, `lowerCamelCase` for functions, values and fields, and `snake_case` for theorems.](guide/naming.md#naming-case)
- [Write acronyms of four or more letters as words, as in `Json`, and shorter ones in one case, as in `IO`.](guide/naming.md#naming-acronyms)
- [Put the functions about a type in the namespace named after the type.](guide/naming.md#naming-namespaces)
- [Name `Bool` functions as questions, as in `isEmpty`, and `Prop` predicates with `Is`, as in `IsSorted`.](guide/naming.md#naming-predicates)
- [Mark failure in the name with `?` for an `Option`, `!` for a panic and `D` for a default.](guide/naming.md#naming-failure)
- [Name conversions `toX` and `ofX`, never `fromX`.](guide/naming.md#naming-conversions)
- [Add `M` to the name of a variant that runs in a monad, as in `mapM` and `forM`.](guide/naming.md#naming-monadic)
- [Don't name a variant of a public function by adding `'`.](guide/naming.md#naming-primes)
- [Use short local names only by convention, such as `xs` for arrays, `acc` for accumulators and `i` for indices.](guide/naming.md#naming-locals)
- [Leave instances anonymous.](guide/naming.md#naming-instances)
- [Name packages in lowercase and modules in `UpperCamelCase`, with file paths that match.](guide/naming.md#naming-files)

### [Functions](guide/functions.md)

- [Give every top-level definition explicit argument types and an explicit result type.](guide/functions.md#functions-signatures)
- [Make an argument implicit, with braces, when later arguments determine it.](guide/functions.md#functions-implicit)
- [Turn off `autoImplicit`, so a misspelled type name is an error.](guide/functions.md#functions-auto-implicit)
- [Write lambdas as `fun x => e`, never with `λ` or `↦`.](guide/functions.md#functions-lambdas)
- [Use `|>`, `|>.` and `<|` to avoid nested parentheses, and don't use `$`.](guide/functions.md#functions-pipelines)
- [Avoid chains of more than two functions joined with `∘`.](guide/functions.md#functions-point-free)
- [Put single-use helpers in a `where` clause, and name a recursive helper `go`.](guide/functions.md#functions-helpers)
- [Keep each function short enough to read at once.](guide/functions.md#functions-size)
- [Group more than about four parameters in a structure with default values.](guide/functions.md#functions-options)
- [Avoid `Bool` parameters that switch a function between two behaviours.](guide/functions.md#functions-bool-args)
- [List every constructor when you match on your own types, rather than ending with `_`.](guide/functions.md#functions-exhaustive)

### [`do` notation and effects](guide/effects.md)

- [Handle special cases first and return early, so the main path isn't nested.](guide/effects.md#do-early-return)
- [Unwrap an `Option` with `let some x := e | fallback` when the failure case is short.](guide/effects.md#do-let-else)
- [Use `(← action)` inline for a result you use once, and `let x ← action` otherwise.](guide/effects.md#do-nested-actions)
- [Use `let mut` and `for` when they're clearer than a fold or a state monad.](guide/effects.md#do-mutation)
- [End `do` blocks with `return x`, and use `pure x` outside them.](guide/effects.md#do-return)
- [Keep program logic in pure functions and `IO` in a thin outer layer.](guide/effects.md#effects-pure-core)
- [Pass shared configuration through `ReaderT`, and define the application's monad with `abbrev`.](guide/effects.md#effects-config)
- [Use `modify` to update state, instead of `get` followed by `set`.](guide/effects.md#effects-modify)
- [Put acquire and release in a `with…` helper built with `try … finally`.](guide/effects.md#effects-resources)
- [Use `IO` for sequential code, `Task` for parallel computation and `Async` for programs that mostly wait on I/O.](guide/effects.md#effects-concurrency)
- [Don't `#eval` actions with side effects in library files.](guide/effects.md#effects-eval)

### [Data modelling](guide/data.md)

- [Use a `structure` for a value with several parts and an `inductive` for alternatives.](guide/data.md#data-structure-inductive)
- [Model state so that impossible combinations can't be written down.](guide/data.md#data-illegal-states)
- [Define structures with named fields instead of passing tuples around.](guide/data.md#data-own-types)
- [Wrap a primitive in a single-field structure when its values must not be mixed with others, such as IDs.](guide/data.md#data-wrappers)
- [Use `abbrev` for exact synonyms, `structure` for new domain types, and never `def` for type synonyms.](guide/data.md#data-abbrev)
- [Update a structure with `{ s with field := value }` instead of copying fields by hand.](guide/data.md#data-update)
- [Build structures with named fields unless the order of the fields is obvious.](guide/data.md#data-constructors)
- [Derive instances instead of writing them, and derive `Repr` for every data type.](guide/data.md#data-deriving)
- [Check a value once where it enters the program, and pass a type that carries the check.](guide/data.md#data-boundary)
- [Avoid indexed families in APIs, except in code that resembles a typed language.](guide/data.md#data-indexed-families)
- [Use `extends` only when one structure clearly "is a" kind of another.](guide/data.md#data-extends)

### [Type classes and instances](guide/classes.md)

- [Define a type class only when several types will have instances and code is generic over them.](guide/classes.md#classes-when)
- [Write instances with `where`, one method per line.](guide/classes.md#classes-where)
- [Ask for the weakest class a function needs, so it works for more types.](guide/classes.md#classes-weakest)
- [Make `BEq` agree with `Hashable`, and `Ord` with `LT` and `LE`.](guide/classes.md#classes-consistent)
- [Add a coercion only when every source value has an obvious counterpart in the target type.](guide/classes.md#classes-coercions)
- [For a recursive type, write the recursive function in the type's namespace and have the instance call it.](guide/classes.md#classes-recursive)

### [Collections](guide/collections.md)

- [Use `Array` for sequences you build, index or update, and `List` for small ones you take apart from the front.](guide/collections.md#collections-array)
- [Keep a single reference to an array you're updating, so Lean can update it in place.](guide/collections.md#collections-sharing)
- [Loop over elements rather than indices, and prefer `xs[i]?` or a proof to `xs[i]!`.](guide/collections.md#collections-iterate)
- [Use `Std.HashMap` for lookups and `Std.TreeMap` when key order matters.](guide/collections.md#collections-maps)

### [Error handling](guide/errors.md)

- [Return `Option` for one obvious failure and `Except` when the caller needs to know which failure happened.](guide/errors.md#errors-option-except)
- [Give a library an inductive error type with a `ToString` instance.](guide/errors.md#errors-types)
- [In `IO` code, throw errors instead of returning default values.](guide/errors.md#errors-io)
- [Use `panic!` and `!` functions only for bugs, never to reject bad input.](guide/errors.md#errors-panics)
- [Say in the docstring how a function fails.](guide/errors.md#errors-document)
- [Don't catch every exception and carry on as if nothing happened.](guide/errors.md#errors-catch-all)

### [Recursion and termination](guide/recursion.md)

- [Prefer structural recursion, and give a measure with `termination_by` when the recursion isn't structural.](guide/recursion.md#recursion-structural)
- [Mark a function `partial` when it might not terminate or a termination proof isn't worth it. Do so only if you won't prove things about it.](guide/recursion.md#recursion-partial)
- [Use `for`, `while` and `repeat` instead of recursive helpers that only loop.](guide/recursion.md#recursion-loops)
- [Use loops or accumulators for recursion over large inputs.](guide/recursion.md#recursion-deep)

### [Proofs about programs](guide/proofs.md)

- [Put cheap guarantees in types, test the rest, and prove what matters most.](guide/proofs.md#proofs-cost)
- [Keep the simple version of an optimized function as its specification.](guide/proofs.md#proofs-spec)
- [Keep short lemmas next to their definitions, and move longer proofs to their own module.](guide/proofs.md#proofs-location)
- [Prefer `grind`, `omega` and `simp` to long manual proofs, and squeeze `simp` calls that aren't the last step.](guide/proofs.md#proofs-automation)
- [Name a theorem after what it states, in `snake_case`, starting from the conclusion.](guide/proofs.md#proofs-names)
- [Don't commit `sorry`.](guide/proofs.md#proofs-sorry)

### [Performance and low-level code](guide/performance.md)

- [Don't add `@[inline]` or `@[specialize]` without a measurement that shows they help.](guide/performance.md#perf-measure)
- [Prefer `@[csimp]` with a proof to `@[implemented_by]`, which Lean doesn't check.](guide/performance.md#perf-implemented-by)
- [Keep `unsafe` code in small functions with a safe interface, and say in a comment why it's needed.](guide/performance.md#perf-unsafe)
- [Keep `@[extern]` declarations in one small module behind a safe Lean API.](guide/performance.md#perf-ffi)

### [API design and visibility](guide/api.md)

- [Use the module system in libraries, with a plain `public section` in program files.](guide/api.md#api-modules)
- [Mark helpers `private`, or put them in an `Internal` namespace.](guide/api.md#api-private)
- [Mark a declaration `protected` if its short name would clash after `open`.](guide/api.md#api-protected)
- [Use `open … in` for a single declaration, and open for a whole file only if the file uses the namespace throughout.](guide/api.md#api-open)
- [Avoid `variable` in program code.](guide/api.md#api-variable)
- [Deprecate a public declaration with `@[deprecated]` before you rename or remove it.](guide/api.md#api-deprecation)
- [Make public only what callers need.](guide/api.md#api-surface)

### [Macros and notation](guide/macros.md)

- [Don't write a macro when a function will do.](guide/macros.md#macros-functions-first)
- [Get standard notation by implementing classes such as `Add` and `GetElem`.](guide/macros.md#macros-classes)
- [Use macros for syntax sugar, and elaborators when the translation needs types or decisions.](guide/macros.md#macros-macro-or-elab)
- [Make notation `scoped` unless every user of your library needs it.](guide/macros.md#macros-scoped)
- [Don't add `macro_rules` that cover only some uses of existing syntax.](guide/macros.md#macros-overlap)
- [Make your notation appear in Lean's output the way users write it.](guide/macros.md#macros-output)
- [Avoid new symbolic operators in program APIs.](guide/macros.md#macros-symbols)

### [Comments](guide/comments.md)

- [Explain why in comments, and don't restate what the code does.](guide/comments.md#comments-why)
- [Write down every invariant that your types don't enforce.](guide/comments.md#comments-invariants)
- [Leave history and dead code to version control.](guide/comments.md#comments-history)

### [Documentation](guide/documentation.md)

- [Give every public declaration in a library a docstring.](guide/documentation.md#docs-public)
- [Start a function's docstring with a verb such as "Returns", and a type's with a noun phrase.](guide/documentation.md#docs-summary)
- [Put a short docstring on one line, and the delimiters of a longer one on lines of their own.](guide/documentation.md#docs-layout)
- [Show short examples in docstrings, and check them with tests.](guide/documentation.md#docs-examples)
- [Begin every file with a module docstring that has a `#` title.](guide/documentation.md#docs-module)

### [Testing](guide/testing.md)

- [Put tests in a `<Pkg>Test` library and make it the package's `testDriver`.](guide/testing.md#tests-library)
- [Check results with `#guard_msgs` and `#guard`.](guide/testing.md#tests-guard-msgs)
- [In test files that are modules, import the code under test with `meta import`.](guide/testing.md#tests-meta-import)
- [Use an executable test driver for tests that run `IO`.](guide/testing.md#tests-runtime)
- [Test clear properties on random inputs with Plausible.](guide/testing.md#tests-property)
- [Test what types and proofs don't cover.](guide/testing.md#tests-coverage)

### [Projects and tooling](guide/projects.md)

- [Start from the layout `lake new` creates, with a small `Main.lean`.](guide/projects.md#project-layout)
- [Commit `lean-toolchain` and `lake-manifest.json`, and require dependencies at release tags.](guide/projects.md#project-dependencies)
- [Set `autoImplicit = false`, and `linter.missingDocs = true` in libraries, in the Lake configuration.](guide/projects.md#project-options)
- [Check for warnings in CI with `lake build --wfail`, and don't set `warningAsError` in a library.](guide/projects.md#project-warnings)
- [Keep Lean's built-in linters on.](guide/projects.md#project-linters)
- [Don't mix reformatting with other changes.](guide/projects.md#project-formatting)

## Existential

- Let the types do the work where that's cheap.
- Be consistent.
- Use common sense.

*Source: [Google Haskell guide][google-parting].*

## Contributing

Open an issue or a pull request. Every Lean example has to compile:

```sh
python3 tools/check_examples.py
```

## Licence

The text of this guide is licensed under [CC BY 4.0](LICENSE). The code examples, [tools/](tools/) and [research/scripts/](research/scripts/) are licensed under [Apache-2.0](LICENSE-CODE). Material quoted in [research/](research/) stays under its original licence, listed for each source in [research/index.md](research/index.md).

[boring-haskell]: https://www.snoyman.com/blog/2019/11/boring-haskell-manifesto/#power-to-weight-ratio
[clj-principles]: https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc?plain=1#L75-L103
[cn-intro]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#standard-library-naming-conventions
[fpil-proofs]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs.lean#L37-L41
[google-parting]: https://google.github.io/styleguide/haskellguide.html#parting-words
[kowainik-existing]: https://kowainik.github.io/posts/2019-02-06-style-guide#rule-of-thumb-when-working-with-existing-source-code
[pep8-consistency]: https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds
[simple-haskell]: https://www.simplehaskell.org/
