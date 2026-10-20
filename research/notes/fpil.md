# Functional Programming in Lean (David Thrane Christiansen)

| Field | Value |
|---|---|
| URL | https://lean-lang.org/functional_programming_in_lean/ (source: https://github.com/leanprover/fp-lean/tree/0abeea545d560a324e2561f7210fbd6ed154fa02) |
| Author / org | David Thrane Christiansen; written on contract to Microsoft (2023), revised at the Lean FRO (2023–2026) |
| Date / version | Repo commit `0abeea545d560a324e2561f7210fbd6ed154fa02` (2026-08-13), which was upstream `HEAD` on 2026-10-17. The rendered book says "All code samples are tested with Lean release 4.33.0", matching `examples/lean-toolchain` (`book/lean-toolchain` is v4.34.0-rc1). Its release history stops at "October, 2025: … Lean release (version 4.23.0) … functional induction and the `grind` tactic" ([Intro.lean L135](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Intro.lean#L135)). Rendered pages link to Lean Reference 4.26.0 |
| License | Text: CC BY 4.0 (`README.md`, `LICENSE-ASSETS`, the book's own "License" section). Code: no licence stated in the README, `LICENSE-ASSETS` or the GitHub metadata (`gh repo view` reports "Other"), checked 2026-10-17 |
| Scope & audience | Programmers learning Lean, no FP background assumed; also mathematicians who write proof automation |
| Kind | descriptive (teaching book), with about 70 explicit recommendations, most of them hedged ("typically", "generally", "usually") and many with reasons |
| Lean version | Lean 4 (4.23–4.34 era; earlier editions 4.0–4.18) |
| Raw copy | rendered book: `vendor/pages/lean-official/fpil/` (70 pages, defuddle, fetched 2026-10-17); source: `vendor/repos/fp-lean` |

## How this note was made

- **Full read.** All 70 rendered pages (chapters 1–9 and both interludes) were read in full. This replaces the earlier note, which was built from keyword greps.
- **Links.** Quotes are copied from the rendered text and located in the Verso source with a phrase lookup. The source has one sentence per line, so links point at the exact sentence at commit `0abeea5`. Code-level observations link to `examples/`.
- **Measurements.** The book's example code (`examples/`, 53 files, 14.5k nonblank lines) was measured with the stdlib survey script as an opt-in `FPIL` column (`python3 ../../scripts/survey.py --cols FPIL,Lake,Std,Wild`, run from `research/vendor/repos`). See [Measured](#measured-the-books-example-code).
- **Labels.** "Q" quotes are verbatim. "(paraphrase)" marks an idiom the book shows without stating it. "(survey)" marks a count.

## Summary

FPIL is the FRO's book on writing programs in Lean, and the most detailed official source on program design. It teaches by example and states no style guide, but a full read finds about 70 explicit recommendations. These are concentrated in five areas: type annotations and data modelling; type-class and coercion design; effects and monad-stack architecture; termination (with a recommended write-test-prove workflow); and when proofs are worth their cost, including a long argument against indexed families in ordinary code. Most recommendations come with reasons: readability, error localisation, maintenance under change, provability, performance or caller convenience. Unlike the other Lean sources, FPIL also says plainly what is bad: about 15 statements call a pattern poor style, buggy, confusing, noisy or a "code smell", usually next to a better version (see [Explicit "don't"s](#explicit-donts)). Its own code is not fully consistent: theorem names mix three casings, helper names vary, and it relies on auto-bound implicits, which Mathlib disables and Std disables in 70 files.

## Rules

Grouped by the chapters of [proposed-toc.md](../proposed-toc.md).

### Naming

> A Lean naming convention is to define operations that might fail in groups using the suffixes `?` for a version that returns an `Option`, `!` for a version that crashes when provided with invalid input, and `D` for a version that returns a default value when the operation would otherwise fail. Following this pattern, `List.head` requires the caller to provide mathematical evidence that the list is not empty, `List.head?` returns an `Option`, `List.head!` crashes the program when passed an empty list, and `List.headD` takes a default value to return in case the list is empty. ([GettingToKnow/Polymorphism.lean L419-L420](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L419-L420))

So in FPIL's scheme the unsuffixed name is the proof-taking variant. The book's own code follows it only for `?`: `NonEmptyList.get?` next to a proof-taking `NonEmptyList.get` ([TypeClasses/Indexing.lean L176](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Indexing.lean#L176)), and 18 `?` defs but no `!` or `D` defs anywhere in `examples/` (survey).

> It is customary to use Greek letters to name type arguments in Lean when no more specific name suggests itself. ([GettingToKnow/Polymorphism.lean L45](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L45))

> Just as type arguments are conventionally named with Greek letters, universe arguments are conventionally named `u`, `v`, and `w`. ([FunctorApplicativeMonad/Universes.lean L142](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Universes.lean#L142))

> By convention, the Greek letter `ρ`, which is pronounced “rho”, is used for environments. ([Monads/Arithmetic.lean L595](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Arithmetic.lean#L595)) (paraphrase: `σ` for states and `ε` for errors throughout.)

> Names such as `xs` and `ys` are conventionally used to stand for lists of unknown values. ([GettingToKnow/Polymorphism.lean L267](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L267))

> In the definition of `plus`, the name `k'` is chosen to indicate that it is connected to, but not identical with, the argument `k`. ([GettingToKnow/DatatypesPatterns.lean L327](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/DatatypesPatterns.lean#L327)) (Primes are used for related locals throughout: `xs'`, `h'`, `st'`. core-naming's "no primes" concerns declaration names.)

> Generally, however, the choice of argument name is less important than the choice of a structure field name, as it does not form as large a part of the API. ([GettingToKnow/DatatypesPatterns.lean L86](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/DatatypesPatterns.lean#L86))

> By convention, package and executable names begin with a lowercase letter, while libraries begin with an uppercase letter. ([HelloWorld/StartingAProject.lean L104](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StartingAProject.lean#L104))

> [Monad classes with and without output parameters] both versions are typically provided, with the ordinary-parameter version of the type class having a name that ends in `-Of`. ([MonadTransformers/Summary.lean L45](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Summary.lean#L45))

> Ranges are represented by a collection of types with a naming convention that describes their bounds. ([MonadTransformers/Do.lean L508](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L508)) (`Std.Rco`, `Std.Roi` and so on.)

> The name `CanFail` suggests that the effect introduced by division is potential failure. ([Monads/Arithmetic.lean L238](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Arithmetic.lean#L238))

Observed naming (paraphrase and survey):
- **Instances** are always anonymous: 133 instances, none named (survey §8). Std names 8.1%.
- **Predicates:** `Bool` tests are `isX` (`Weekday.isWeekend`, `isEven`); inductive `Prop` predicates are `IsX` (`IsThree`), matching core-naming.
- **Monad-generic variants** end in `M` (`mapM`, `evaluateM`). Option-returning recognisers end in `?` (`Inline.string?`, `Nat.asFastPos?`).
- **Conversions:** `Many.fromList`, where the stdlib has 30 `ofList` defs and no `fromList`.
- **Helpers** have no single scheme: `let rec helper`, `go` or `loop`; top-level `Tail.sumHelper`, `arrayMapHelper`, `insertionSortLoop`.
- **Theorems** are inconsistent. Of 172, 59.9% are snake_case, 22.7% snake+camel and 15.1% lowerCamel (survey §1). The interlude uses sentence names (`onePlusOneIsTwo`, `fairlyEasy`), later chapters snake_case (`plusR_zero_left`, `BinTree.mirror_count`). The def `insertSorted` becomes `insert_sorted_size_eq` ([InstrumentedInsertionSort.lean L21-L24](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/examples/Examples/ProgramsProofs/InstrumentedInsertionSort.lean#L21-L24)), against core-naming's "When encountering a name, put it in lower camel case."

### Layout

> Each `IO` action or local binding in the `do` is expected to start on its own line, and they should all have the same indentation. Almost all uses of `do` should be written this way. ([HelloWorld/Conveniences.lean L140-L141](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L140-L141))

> Idiomatic Lean code uses curly braces with `do` very rarely. ([HelloWorld/Conveniences.lean L181](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L181))

> Idiomatic Lean code makes use of a variety of Unicode characters that are not part of ASCII. [...] This allows Lean code to more closely resemble ordinary mathematical notation. ([Intro.lean L112-L113](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Intro.lean#L112-L113)) (Survey: 1,039 `→` vs 4 `->`, 0 `<-`.)

The book's code layout (survey §4) matches core-style rather than Lake:
- Split headers continue at +4 (92.5%; Std 98.8%, Lake 10.6%) and end the line with ` :`. No header line starts with `:`.
- Bodies start at +2 (98.7%). Match arms sit at the `match` column (98.3%). Equation-compiler arms are at +2 (100%).
- Aligned `=>` is rare (0.4% of arms). Line length is short: p95 59, p99 83.

Other layout habits (paraphrase):
- `if c then` / branch / `else e`, with a short `else` on one line.
- `:= do` at the end of the header.
- Blank lines inside long `do` blocks to separate phases, for example validation, prompt and output in the early-return `main` ([MonadTransformers/Do.lean L151](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L151)). Mathlib's `emptyLine` linter forbids this.
- Leading `|>.` on continuation lines of long pipelines (the query examples near [DependentTypes/TypedQueries.lean L756](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L756)).
- Two structure-literal layouts: `:= {` at line end, or `{ f := …,` with aligned fields and `}` on its own line.
- Small inconsistencies: `not` vs `!`, and `rw [←h]` with no space.

### Functions and expressions

**Type annotations.** One of the book's strongest recommendations:

> Generally speaking, it is a good idea to err on the side of too many, rather than too few, type annotations. First off, explicit types communicate assumptions about the code to readers. Even if Lean can determine the type on its own, it can still be easier to read code without having to repeatedly query Lean for type information. Secondly, explicit types help localize errors. The more explicit a program is about its types, the more informative the error messages can be. This is especially important in a language like Lean that has a very expressive type system. Thirdly, explicit types make it easier to write the program in the first place. The type is a specification, and the compiler's feedback can be a helpful tool in writing a program that meets the specification. Finally, Lean's type inference is a best-effort system. ([GettingToKnow/Conveniences.lean L238-L246](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L238-L246))

> In general, it is a good idea to write most types explicitly, only letting Lean fill out the very obvious types. This improves Lean's error messages and helps make programmer intent more clear. ([GettingToKnow/Summary.lean L68-L69](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Summary.lean#L68-L69)) The book adds a rule of thumb: "Omitting return types for function definitions will often work, but function parameters typically require annotations." ([GettingToKnow/Conveniences.lean L219](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L219))

**Implicit and auto-bound arguments.** Explicit type arguments are "somewhat bureaucratic to use, because the type argument is typically uniquely determined by the later values" ([GettingToKnow/Polymorphism.lean L288](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L288)). FPIL then relies on auto-bound implicits everywhere (`def length (xs : List α)`):

> When writing polymorphic functions in Lean, it is typically not necessary to list all the implicit parameters. Instead, they can simply be mentioned. ([GettingToKnow/Conveniences.lean L27-L28](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L27-L28))

It notes one trap: in `checkSubtype` "it's important that the type class `[Decidable (p v)]` occur after the specification of the arguments `v` and `p`. Otherwise, it would refer to an additional set of automatic implicit arguments" ([FunctorApplicativeMonad/Alternative.lean L155-L156](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Alternative.lean#L155-L156)). This conflicts with Mathlib, which sets `autoImplicit false`, and with Std, where 70 of 499 files set `set_option autoImplicit false`. Lean core's default is `true` (`src/Lean/Elab/AutoBound.lean` L17-L19 at `3a685e6`).

**Pattern matching.**

> Recursive functions that take two parameters should not match against the pair, but rather match each parameter independently. Otherwise, the mechanism in Lean that checks whether recursive calls are made on smaller values is unable to see the connection between the input value and the argument in the recursive call. ([GettingToKnow/Polymorphism.lean L732-L733](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L732-L733))

Simultaneous matching (`match xs, ys with`) is the fix. The book also says to use pattern-matching definitions when an argument is named only to be matched: "it is quite common to name an argument and then immediately use it with pattern matching. [...] In these situations, the cases of the `match` expression can be written directly" ([GettingToKnow/Conveniences.lean L57-L59](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L57-L59)). For `Nat` patterns, "the second argument to `+` should always be a literal `Nat`" ([GettingToKnow/Conveniences.lean L450](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L450)).

> Using underscores instead of names is a way to clearly communicate to readers that part of the input is ignored. ([GettingToKnow/Polymorphism.lean L408](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L408))

> Using or-patterns can vastly simplify some definitions and increase their clarity [...]. Because there is a potential for confusing behavior, it's a good idea to be careful when using them, especially when variables of multiple types or disjoint sets of variables are involved. ([Monads/Conveniences.lean L189-L190](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Conveniences.lean#L189-L190))

> Omitting the namespaces [with leading-dot constructors] makes it significantly shorter, at the cost of making the program harder to read in contexts like code review tools that don't include the Lean compiler ([Monads/Conveniences.lean L59](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Conveniences.lean#L59)). The book's own code from chapter 5 on uses `.ctor` heavily.

> In some contexts, using `if let` instead of `match` can make code easier to read. ([GettingToKnow/Conveniences.lean L724](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L724))

**Local definitions and helpers.**

> In many cases, intermediate values represent useful concepts all on their own, and naming them explicitly can make the program easier to read. In other cases, the intermediate value is used more than once. As in most other languages, writing down the same code twice in Lean causes it to be computed twice ([GettingToKnow/Conveniences.lean L125-L127](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L125-L127))

> Judicious use of patterns with `let` can make code easier to read, compared to writing the accessor calls by hand. ([GettingToKnow/Conveniences.lean L178](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L178))

> The fundamental problem with this code is that it addresses two concerns [...]. It is often good style to lift a repetitive segment into a helper function ([Monads.lean L111-L113](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L111-L113))

> the function mixes two concerns: evaluating subexpressions and applying a binary operator to the results. It can be improved by splitting it into two functions ([Monads/Arithmetic.lean L95](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Arithmetic.lean#L95))

> While it can be written as a series of nested `if` expressions, it's easier to design the three cases independently and then combine them. ([FunctorApplicativeMonad/Alternative.lean L57](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Alternative.lean#L57))

No rule on `where` vs `let rec` (Q7). The code uses `let rec` 15 times and a `where` helper once (survey §3; Std is 21 vs 113). No `private` declaration appears anywhere.

**Lambdas, sections and pipelines.**

> Even though Lean does permit `λ` to be used instead of `fun`, it is most common to write `fun`. ([GettingToKnow/Conveniences.lean L511](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L511)) (Survey: 98.9% `fun x =>`, no `↦`.)

> When an anonymous function is very simple, like `fun x => x + 1`, the syntax for creating the function can be fairly verbose. [...] For these simple cases, Lean provides a shorthand. ([GettingToKnow/Conveniences.lean L551-L553](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L551-L553)) That shorthand is `(· + 1)`.

> some programs are easier to understand in terms of an input that is successively refined to produce the output. For these situations, Lean provides a *pipeline* operator ([MonadTransformers/Conveniences.lean L25](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L25)) ... pipelines really come into their own when they contain many components. ([MonadTransformers/Conveniences.lean L38](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L38)) ... [`<|`:] in cases where many nested parentheses pose a challenge for readers, they can clarify the steps of application. ([MonadTransformers/Conveniences.lean L56](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L56))

> For every `Applicative`, `pure f <*> E` is equivalent to `f <$> E`. In other words, using `seq` to apply a function that was placed into the `Applicative` type using `pure` is overkill ([FunctorApplicativeMonad/Alternative.lean L132-L133](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Alternative.lean#L132-L133))

**Shared binders.** For `(x y : α)`: "This is especially useful when the type signature is large." ([Monads/Conveniences.lean L42](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Conveniences.lean#L42))

**Holes.** On using `_` placeholders to let the types guide a definition: "It's not always possible to write correct functions by simply “following the types”, and it carries the risk of not understanding the resulting program. However, it can also be easier to understand a program that has been written than one that has not, and the process of filling in the underscores can bring insights." ([Monads/Arithmetic.lean L713-L714](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Arithmetic.lean#L713-L714))

### `do` notation and effects

**Why effects are explicit.** Separating evaluation from execution "means that programs must be explicit about which functions can have side effects. Because the parts of the program that do not have effects are much more amenable to mathematical reasoning, whether in the heads of programmers or using Lean's facilities for formal proof, this separation can make it easier to avoid bugs." ([HelloWorld/StepByStep.lean L161-L162](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StepByStep.lean#L161-L162)) Monads make programs "honest about which effects they use in their types. A quick glance at a type signature describes *everything* that the program can do" ([Monads/Arithmetic.lean L21](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Arithmetic.lean#L21)). Purity "helps programmers understand the parts of the program in isolation from each other, because there are no hidden state changes that create subtle coupling between components" ([HelloWorld/RunningAProgram.lean L94](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/RunningAProgram.lean#L94)).

**Application shape.**

> A typical application has a core set of easily testable functions written without monads paired with an outer wrapper that uses a monad to encode the necessary application logic. ([MonadTransformers.lean L28](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers.lean#L28))

> Typically, the majority of the application logic will be in a collection of libraries for the program, while `Main.lean` will contain a small wrapper around these pieces that does things like parsing command lines and executing the central application logic. ([HelloWorld/StartingAProject.lean L40](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StartingAProject.lean#L40))

**`do` style.**
- Prefer `do` to explicit `>>=` chains. With `do`, the rewritten function "becomes significantly more readable" ([Monads/Do.lean L93](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Do.lean#L93)).
- Nested actions: "avoids introducing names that are used only once, which can greatly simplify a program" ([HelloWorld/Conveniences.lean L67](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L67)). But "Even though it's often good style to use nested actions, it can still sometimes be helpful to name intermediate results." ([HelloWorld/Conveniences.lean L85](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L85))
- Early return: "Many programs begin with a section that validates arguments and inputs before proceeding to the main body of the program." ([MonadTransformers/Do.lean L151](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L151)) It "avoids needing to nest the control flow" ([MonadTransformers/Do.lean L216](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L216)). The catch is that "Lean's early return applies only to the current `do`-block" ([MonadTransformers/Do.lean L239](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L239)).
- Loops: exiting a `forM` early via `OptionT` "is not so easy to read" next to `for … break` ([MonadTransformers/Do.lean L448-L449](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L448-L449)). The `continue` form of `find?` is "An alternative (but confusing) formulation" ([MonadTransformers/Do.lean L493](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L493)).
- `let mut`: "Local mutable variables can be more convenient to use and easier to read than an explicit local use of `StateT`." They can only be mutated in their own `do` block, so a loop can't be swapped for a recursive helper ([MonadTransformers/Do.lean L653-L656](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L653-L656)).
- `repeat` and `while` replace a `partial` stream loop: "This function can be greatly shortened using `repeat`", and the result needs no `partial` ([MonadTransformers/Conveniences.lean L100](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L100), [MonadTransformers/Conveniences.lean L113](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Conveniences.lean#L113)).
- Imperative or functional: "some tasks are just most naturally thought of imperatively", and `do` lets "functional versus imperative programming [...] be a matter of perspective" ([MonadTransformers/Do.lean L800](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L800)). No preference is stated.

**Monad stacks.** Chapter 6 is the only Lean source on application monad design (Q14).
- **Why a reader.** "manually passing the configuration around is verbose and error-prone. The type system will not catch it if the wrong configuration is passed downwards" ([MonadTransformers/ReaderIO.lean L201](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L201)). The book lists three advantages and three downsides of a hand-written `ConfigIO` ([MonadTransformers/ReaderIO.lean L293](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L293) ff.).
- **Name the boundary.** `ConfigIO.run` "is not really necessary [...]. However, naming the operation can make it easier to see which parts of the code are intended to run in which monad." ([MonadTransformers/ReaderIO.lean L227-L228](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L227-L228))
- **Use stdlib transformers.** "rewriting the code using components from the standard library does have long-term benefits": readers already know `ReaderT`, adding effects "requires far fewer changes", and polymorphic code need not care about transformer order ([MonadTransformers/ReaderIO.lean L444](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L444) ff.).
- **Declare stacks with `abbrev`.** "It is an `abbrev` because `ReaderT` has many useful features defined in the standard library that a non-reducible definition would hide." ([MonadTransformers/ReaderIO.lean L337](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L337)) The book's `M1`/`M2` stacks are `abbrev` too.
- **Write against effect classes.** "The type classes are a way for programs to express their requirements, and monad transformers are a convenient way to meet these requirements." ([MonadTransformers/Transformers.lean L28](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L28)) But beware over-generality: since stack order changes meaning, "the type signature of `countWithFallback` is probably more polymorphic than it should be" ([MonadTransformers/Order.lean L154](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Order.lean#L154)). "In general, monad transformers should not be expected to commute." ([MonadTransformers/Order.lean L142](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Order.lean#L142))
- **Prefer `modify` to `get`/`set`.** "it becomes too easy to `set` the wrong state when updating it" ([MonadTransformers/Transformers.lean L434](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L434)). "In a large program, this kind of mistake can lead to difficult-to-diagnose bugs." ([MonadTransformers/Transformers.lean L476](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L476)) Also, "duplicating the references to the state might lead to code that is significantly slower" ([MonadTransformers/Transformers.lean L481](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L481)).
- **`Of` classes.** "It's generally a good idea to implement the `Of` version, and then start writing programs using the non-`Of` versions of the class, transitioning to the `Of` version if the output parameter becomes inconvenient." ([MonadTransformers/Transformers.lean L560](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L560))

**Resources.** FPIL never teaches `try … finally` (0 uses in the code) or `withFile`. File handles rely on reference counting: "When there are no references to the file handle value, a finalizer closes the file descriptor." ([HelloWorld/Cat.lean L159](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Cat.lean#L159))

**Survey contrasts.** FPIL ends `do` blocks with `pure` (226 `pure` vs 17 `return`), where Lake has 134 vs 867. It never uses let-else (`let some x ← e | alt`), which core-style recommends (§5).

### Data modelling

> Typically, `structure` is used to introduce a product type (that is, a type with just one constructor that takes any number of arguments), while `inductive` is used to introduce a sum type ([GettingToKnow/Summary.lean L87](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Summary.lean#L87))

> Defining separate structures prevents API clients from confusing one for another. ([GettingToKnow/Structures.lean L28](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L28))

> Many applications are best served by defining their own structures, even for simple cases like `Point`, because using domain terminology can make it easier to read the code. Additionally, defining structure types helps catch more errors by assigning different types to different domain concepts, preventing them from being mixed up. ([GettingToKnow/Polymorphism.lean L497-L498](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L497-L498)) Exceptions: "there are some cases where it is not worth the overhead of defining a new type. Additionally, some libraries are sufficiently generic that there is no more specific concept than “pair”." ([GettingToKnow/Polymorphism.lean L500-L501](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L500-L501))

> Like `Prod`, `Sum` should be used either when writing very generic code, for a very small section of code where there is no sensible domain-specific type, or when the standard library contains useful functions. In most situations, it is more readable and maintainable to use a custom inductive type. ([GettingToKnow/Polymorphism.lean L559-L560](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L559-L560))

> [Wrappers are free:] single-field structures can be created to keep track of different uses of `Nat`s or `String`s without paying a performance penalty. ([ProgramsProofs/SpecialTypes.lean L52](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/SpecialTypes.lean#L52)) A subtype "is represented identically to its underlying type".

**Structure update.** Copying fields by hand (`{ x := 0, y := p.y }`):

> This style of programming has drawbacks, however. First off, if a new field is added to a structure, then every site that updates any field at all must be updated, causing maintenance difficulties. Secondly, if the structure contains multiple fields with the same type, then there is a real risk of copy-paste coding leading to field contents being duplicated or switched. Finally, the program becomes long and bureaucratic. ([GettingToKnow/Structures.lean L243-L246](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L243-L246))

**Constructors.**
- `Point.mk 1.5 2.8`: "this is not generally considered to be good Lean style, and Lean even returns its feedback using the standard structure initializer syntax" ([GettingToKnow/Structures.lean L325](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L325)).
- Constructors can't validate: "It is not possible to provide a custom constructor that pre-processes data or rejects invalid arguments." ([GettingToKnow/Structures.lean L313](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L313))
- `⟨…⟩` "can be useful when emphasizing that a structure type is very much like a tuple in which the fields happen to be named" ([TypeClasses/Conveniences.lean L71](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L71), also [GettingToKnow/Conveniences.lean L738](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Conveniences.lean#L738)). With `extends`, though, it "reveals the internal details" ([FunctorApplicativeMonad/Inheritance.lean L91](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Inheritance.lean#L91)).

**Inheritance.**

> This can be useful when modeling concepts that have a clear taxonomic relationship. ([FunctorApplicativeMonad/Inheritance.lean L20](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Inheritance.lean#L20))

> If the child structure should not deviate from the parent structure, there are a few options: 1. Documenting the relationship, as is done for `BEq` and `Hashable` 2. Defining a proposition that the fields are related appropriately, and designing the API to require evidence that the proposition is true where it matters 3. Not using inheritance at all ([FunctorApplicativeMonad/Inheritance.lean L238-L242](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Inheritance.lean#L238-L242))

**Precise types.**

> Rather than relying on natural numbers, and littering the code with assertions that the number is not zero, it can be useful to design a datatype that represents only positive numbers. ([TypeClasses/Pos.lean L22](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Pos.lean#L22))

> Having a trade-off between precise types and convenient APIs means that the precise types become less useful. ([TypeClasses/Pos.lean L276](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Pos.lean#L276)) (So `Pos` gets `OfNat`, `Add` and `ToString` instances.)

> Subtypes are a two-edged sword. They allow efficient representation of validation rules, but they transfer the burden of maintaining these rules to the users of the library, who have to *prove* that they are not violating important invariants. Generally, it's a good idea to use them internally to a library, providing an API to users that automatically ensures that all invariants are satisfied, with any necessary proofs being internal to the library. ([FunctorApplicativeMonad/Applicative.lean L225-L227](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L225-L227))

> [`Fin`:] Rather than passing an index and a proof separately, a type called `Fin` can be used to bundle up the index and the proof into a single value. This can make code easier to read. ([ProgramsProofs/Fin.lean L20-L21](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Fin.lean#L20-L21)) ... A more specific type results in a value that can be used without making the program significantly more complicated ([ProgramsProofs/Fin.lean L41](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Fin.lean#L41))

A subtype of `Nat` beats a user-defined `Pos` inductive at run time because it "allows the new type to use the efficient representation while still ruling out zero at compile time" ([FunctorApplicativeMonad/Applicative.lean L203](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L203)).

**Indexed families.** The book's most developed design argument (Q9):
- **Implementations leak into types.** "the distinction between the interface and the implementation of functions begins to break down when functions are used in types" ([DependentTypes/Pitfalls.lean L22](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Pitfalls.lean#L22)).
- **Four drawbacks.** Definitional equality "has serious software engineering drawbacks". Type-level functions may not be efficient and become interface; definitional-equality checks can be slow; error messages are hard to read; and invariants encoded this way are "brittle" ([DependentTypes/Pitfalls.lean L500](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Pitfalls.lean#L500) ff.).
- **Verdict:**

  > In idiomatic Lean code, indexed datatypes are not used very often. Instead, subtypes and explicit propositions are typically used to enforce important invariants. This approach involves many explicit proofs, and very few appeals to definitional equality. As befits an interactive theorem prover, Lean has been designed to make explicit proofs convenient. Generally speaking, this approach should be preferred in most cases. ([DependentTypes/Pitfalls.lean L511-L515](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Pitfalls.lean#L511-L515))

- **But sometimes right.** "indexed datatypes are sometimes exactly the right tool for the job. Fluency in their use is an important part of knowing when to use them." ([DependentTypes/Pitfalls.lean L522](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Pitfalls.lean#L522)) In particular: "Indexed families are very useful when building an API that is supposed to resemble some other language." ([DependentTypes/TypedQueries.lean L18](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L18)) Even then, `Query` "is probably best as the core of a typed database interaction library, rather than its user interface" ([DependentTypes/TypedQueries.lean L851](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L851)).
- **Costs:** "each invariant requires its own datatype, which then requires its own support libraries" ([DependentTypes/Summary.lean L71](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Summary.lean#L71)). Re-indexing functions are "nothing but a slow identity function" ([DependentTypes/TypedQueries.lean L708](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L708)).
- **Code smell:** "the frequent use of propositional equality to unstick type-level computation is typically a code smell. It typically means that coincidences were not well-engineered, and it's usually a better idea to either redesign the types and indices or to use a different technique to enforce the needed invariants. When propositional equality is instead used to prove that a program meets a specification, or as part of a subtype, there is less reason to be suspicious." ([DependentTypes/Summary.lean L98-L100](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Summary.lean#L98-L100))
- **General warning:** "there is a real risk of tying oneself in knots and being unable to complete the program" ([DependentTypes.lean L59](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes.lean#L59)).

**Inductive declarations.**

> It is worth thinking about which arguments should be parameters and which should be indices when choosing the order of arguments to a datatype. Having as many arguments as possible be parameters helps keep universe levels under control [...]. ([DependentTypes/IndicesParametersUniverses.lean L178-L180](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/IndicesParametersUniverses.lean#L178-L180))

> even though Lean is capable of determining that arguments after the colon are nonetheless parameters by their usage, it's a good idea to write parameters with explicit names. This makes the intention clear to readers, and it causes Lean to report an error if the argument is mistakenly used inconsistently across the constructors. ([DependentTypes/IndicesParametersUniverses.lean L182-L183](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/IndicesParametersUniverses.lean#L182-L183))

> There are a few general guidelines to follow when writing universe-polymorphic types. First off, independent type arguments should have different universe variables [...]. Secondly, the whole type is itself typically either in the maximum of all the universe variables, or one greater than this maximum. Try the smaller of the two first. Finally, it's a good idea to put the new type in as small of a universe as possible ([FunctorApplicativeMonad/Universes.lean L246-L250](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Universes.lean#L246-L250)). "Generally speaking, Lean libraries should use universe polymorphism when implementing libraries of polymorphic operations." ([FunctorApplicativeMonad/Summary.lean L82](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Summary.lean#L82))

**`abbrev` vs `def` (Q10).** FPIL gives four reasons for `abbrev`:
1. Abbreviations "are always unfolded" ([GettingToKnow/FunctionsDefinitions.lean L224](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/FunctionsDefinitions.lean#L224)), but "Control over reducibility is essential to allow Lean to scale" ([GettingToKnow/FunctionsDefinitions.lean L242](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/FunctionsDefinitions.lean#L242)).
2. Propositions that tactics must see through should be `abbrev` (`NonEmptyList.inBounds`, [TypeClasses/Indexing.lean L110](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Indexing.lean#L110); `SizesMatch`, [FunctorApplicativeMonad/Inheritance.lean L251](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Inheritance.lean#L251)).
3. Monad stacks should be `abbrev` (`ConfigIO`, above).
4. "Just like type class search, dot notation can see through definitions created with `abbrev`." ([DependentTypes/TypedQueries.lean L756](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L756))

Types that get their own instances (`State`, `Reader`, `OptionT`, `ConfigIO` before `ReaderT`) are `def`s (paraphrase). Structure wrappers have a cost: "these structures can make it more difficult to read proofs" ([MonadTransformers/Transformers.lean L137](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L137)). For `def`-defined transformers the book adds identity `mk`/`run` functions, which "indicate the boundary between code that is intended to present the interface of `OptionT` and code that is intended to present the interface of the underlying monad" ([MonadTransformers/Transformers.lean L145](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L145)).

**Deriving (Q11).**

> Instance of classes like `BEq` and `Hashable` are often quite tedious to implement by hand. Lean includes a feature called *instance deriving* that allows the compiler to automatically construct well-behaved instances of many type classes. ([TypeClasses/StandardClasses.lean L348-L349](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L348-L349))

> Aside from the clear advantages in programmer productivity and code readability, deriving instances also makes code easier to maintain, because the instances are updated as the definitions of types evolve. When reviewing changes to code, modifications that involve updates to datatypes are much easier to read without line after line of formulaic modifications to equality tests and hash computation. ([TypeClasses/StandardClasses.lean L377-L378](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L377-L378))

The exception: "the derived `Ord` instance may not produce precisely the ordering desired in an application. When this is the case, it's fine to write an `Ord` instance by hand." ([TypeClasses/StandardClasses.lean L374](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L374)) In practice the book derives Repr 23 times, BEq 5 and Hashable 3, and never Inhabited or DecidableEq (survey §8).

### Type classes and instances

**Class design.**
- Keep classes small: "a class will specify some minimal set of overloadable operations that make sense together, and then use polymorphic functions with instance implicit arguments that build on the overloaded operations to provide a larger library of features." ([TypeClasses/StandardClasses.lean L482](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L482))
- Use default methods where internals allow a faster version ([TypeClasses/StandardClasses.lean L492](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L492)). But "These default implementations should only be overridden with new functions that are behaviorally equivalent, but more efficient. The default implementations should be seen as specifications for correctness as well as automatically-created code." ([FunctorApplicativeMonad/Complete.lean L130-L131](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Complete.lean#L130-L131))
- Hierarchies: "By carefully designing type class inheritance hierarchies, programmers can get the best of both worlds: a fine-grained collection of independently-implementable abstractions, and automatic construction of these specific abstractions from larger, more general abstractions." ([FunctorApplicativeMonad/Inheritance.lean L277](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Inheritance.lean#L277))

> Polymorphic programs should be written to use as weak of an abstraction as possible, while datatypes should be given instances that are as powerful as possible. This maximizes code re-use. ([FunctorApplicativeMonad/Summary.lean L58-L59](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Summary.lean#L58-L59))

It is applied to `doList`: "the full power of `Monad` is not necessary, and it will work for any `Applicative`" ([MonadTransformers/ReaderIO.lean L185](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L185)). The other side of the trade-off: "A more powerful abstraction like `Monad` increases the flexibility that's available to the API consumer, but it decreases the flexibility that is available to the API implementor." ([FunctorApplicativeMonad/Applicative.lean L406](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L406))

**Laws.**
- "If two values are considered equal according to a `BEq` instance for their type, then they should have the same hashes." ([TypeClasses/StandardClasses.lean L284](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L284))
- "Just as a `Hashable` instance that doesn't respect `BEq` is buggy, a `Functor` instance that moves around the data as it maps the function is also buggy." ([TypeClasses/StandardClasses.lean L511](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L511))
- Monad and applicative contracts ([Monads/Class.lean L265](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Class.lean#L265)). Combined instances must agree:

  > combined implementations `Functor`, `Applicative` and `Monad` should work equivalently to these default implementations. [...] This is important because polymorphic functions may be refactored to replace a use of `>>=` with an equivalent use of `<*>`, or a use of `<*>` with an equivalent use of `>>=`. This refactoring should not change the meaning of programs that use this code. ([FunctorApplicativeMonad/ApplicativeContract.lean L356-L358](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/ApplicativeContract.lean#L356-L358))

  That is why `Validate`, which accumulates errors, gets no `Monad` instance.

**Which instances to give.**
- Only sensible ones: "Because `0` is not a positive number, there should be no instance of `Zero Pos`." ([TypeClasses/Pos.lean L286](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Pos.lean#L286))
- Not `Monad List`: "Because of this performance trap, it's usually not a good idea to define a `Monad` instance for `List`." ([DependentTypes/TypedQueries.lean L647](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L647))
- Default instances: "default instances can make instance selection less predictable [...]. Be selective about where default instances are used!" ([TypeClasses/OutParams.lean L155-L157](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/OutParams.lean#L155-L157))
- Readable constraints: `Zero α` over `OfNat α 0`, which "can be easier to read" ([TypeClasses/Polymorphism.lean L68](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Polymorphism.lean#L68)).
- Precedence: "When more than one instance is defined, the most recent takes precedence." ([TypeClasses/Pos.lean L233](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Pos.lean#L233))

**Instance syntax.**

> The `where` syntax is typically used for instances, while structures use either the curly-brace syntax or the `where` syntax. ([TypeClasses/Conveniences.lean L70](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L70)) A library-provided constructor function after `:=` "is the easiest way to use such a function" ([TypeClasses/Conveniences.lean L74](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L74)).

Instances usually delegate to a named function in the type's namespace, as in `instance : Add Pos where add := Pos.plus` (paraphrase).

**Comparison.** "Comparing values using `<`, `==`, and `>` can be inefficient. Checking first whether one value is less than another, and then whether they are equal, can require two traversals over large data structures." ([TypeClasses/StandardClasses.lean L246-L247](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L246-L247)) "In situations where `compareTo` would be the right approach in Java, use `Ord.compare` in Lean." ([TypeClasses/StandardClasses.lean L269](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L269))

**`Bool` vs `Prop`.** "Generally speaking, when using Lean as a programming language, it's easiest to stick to Boolean functions rather than propositions." ([TypeClasses/StandardClasses.lean L150](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L150))

**Coercions.** An API-design section in its own right:
- When to define one: "An instance of `Coe α β` makes sense when the type `β` has a value that can represent each value from the type `α`. [...] a coercion from `Int` to `Nat` is a poor idea because `Nat` does not contain the negative numbers." ([TypeClasses/Coercions.lean L217-L218](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L217-L218))
- General stance:

  > Coercions are a powerful tool that should be used responsibly. On the one hand, they can allow an API to naturally follow the everyday rules of the domain being modeled. This can be the difference between a bureaucratic mess of manual conversion functions and a clear program. ([TypeClasses/Coercions.lean L538-L540](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L538-L540)) ... Think carefully about these limitations before using coercions in your own libraries. ([TypeClasses/Coercions.lean L547](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L547))

- Three limitations: coercions need full type information, so "a return type annotation on a function can be the difference between a type error and a successfully applied coercion" ([TypeClasses/Coercions.lean L549](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L549)); failures show the original error, "which can make it difficult to debug chains of coercions" ([TypeClasses/Coercions.lean L571](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L571)); and "coercions are not applied in the context of field accessor notation", so the difference "is visible to users of your API" ([TypeClasses/Coercions.lean L573](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L573)).
- An explicit `↑` "can also make the programmer's intentions more clear" ([TypeClasses/Coercions.lean L209](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L209)).

**Class vs explicit structure of functions.** "putting a type in a field of a structure [...] can make sense in contexts where there is more than one way to implement an operation and more manual control is needed than type classes would allow" ([TypeClasses/Coercions.lean L328](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L328)).

**Class vs closed universe of codes.** "Type classes allow an open-ended collection of types to be used with an API [...]. In most cases, this is preferable. It is hard to predict all use cases for an API ahead of time" ([DependentTypes/UniversePattern.lean L101-L103](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/UniversePattern.lean#L101-L103)). The book lists three cases where a closed universe à la Tarski is better.

### Collections and performance

- **Arrays.** "Lean arrays are much more efficient than linked lists for most purposes." ([TypeClasses/Indexing.lean L26](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Indexing.lean#L26)) Also "most use cases for a variable-length sequential collection of data are better served by arrays" ([ProgramsProofs/ArraysTermination.lean L20](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/ArraysTermination.lean#L20)), while "Linked lists have their place: in some applications, the ability to share the tails of lists is very important." ([ProgramsProofs/ArraysTermination.lean L19](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/ArraysTermination.lean#L19)) The book's own signatures still use `List` four times as often as `Array` (19.2% Array; survey §14).
- **Uniqueness.** "One of the most important steps in optimizing hot loops in Lean code is making sure that the data being modified is not referred to from multiple locations." ([ProgramsProofs/InsertionSort.lean L691](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L691))
- **Test copying, don't assume.** "Lean's proof logic works at the level of pure functional programs, not the underlying implementation. This means that the best way to discover whether a program unnecessarily copies data is to test it." ([ProgramsProofs/InsertionSort.lean L512-L513](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L512-L513)) Use `dbgTraceIfShared`, and test from a built executable: "`#eval` will report that many more values are shared than in compiled code" ([ProgramsProofs/InsertionSort.lean L64](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L64)).
- **Special types.** Using the constructor or field accessors of `Array` or `String` "can trigger expensive conversions", and "these conversions should be avoided in code that is intended to be run" ([ProgramsProofs/SpecialTypes.lean L38](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/SpecialTypes.lean#L38)).
- **Tail calls.** "Programmers must be able to reliably identify tail calls, and they must be able to trust that the compiler will eliminate them." ([ProgramsProofs/TailRecursion.lean L30](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/TailRecursion.lean#L30)) But "At the time of writing, Lean only eliminates direct tail calls in recursive functions." ([ProgramsProofs/TailRecursion.lean L141](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/TailRecursion.lean#L141)) Accumulator-passing style "can also make it more difficult to understand" ([ProgramsProofs/Summary.lean L57](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L57)).
- **Strings.** Slice operations let you "write string manipulations as a series of incremental steps without risking intermediate string copying" ([GettingToKnow/Strings.lean L69](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Strings.lean#L69)).
- **Notation.** Macros "can help make expressions easier to read by eliminating this boilerplate" ([DependentTypes/TypedQueries.lean L489](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L489)). For custom infix operators, "figuring out the most convenient precedences for a group of operators requires some experimentation and a large collection of examples" ([Monads.lean L172](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L172)).

### Error handling

- **Option over null.** "the type system ensures that checks for `null` cannot be forgotten" ([GettingToKnow/Polymorphism.lean L381](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L381)), and "APIs that explicitly describe nullability through type signatures are more informative than ones that don't" ([GettingToKnow/Polymorphism.lean L397](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L397)).
- **Except when the caller needs to know why.** With a bare `Option`, "it is likely relevant for a user to know just how long the list was and where the lookup failed" ([Monads.lean L206](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L206)). Callers of `Except` "are expected to handle both errors and successes, which makes the type variable `ε` play a role that is a bit like that of a list of checked exceptions in Java" ([Monads.lean L218](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L218)). Writing against `>>=` pays off: "only a small modification is required for it to provide an error message on failure" ([Monads/Arithmetic.lean L115](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/Arithmetic.lean#L115)).
- **Exception-polymorphic code.** Pattern matching on `Except` "ties a program that uses exceptions to one specific encoding of the exception handling effect. Using a type class to capture these operations allows a program that uses exceptions to be used in *any* monad that supports throwing and catching." ([MonadTransformers/Transformers.lean L337-L338](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L337-L338))
- **Error types** (paraphrase). The division service throws an inductive `Err` (`divByZero`, `notANumber : String`) from a `MonadExcept Err m` backend. The frontend catches it and returns "a friendly string error". Validation errors are `Field × String`. The teaching examples elsewhere use `String` with context ("Index {i} not found (maximum is …)").
- **Validation.** "it's generally considered to be best to provide many errors at once, rather than one error at a time." ([FunctorApplicativeMonad/Applicative.lean L145](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L145))
  - The result type should say what was checked: "It should return a datatype that is specific—checking that a text box contains a number should return an actual numeric type" ([FunctorApplicativeMonad/Applicative.lean L149](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L149)).
  - Exceptions are the wrong tool: "they terminate the program at the first error" ([FunctorApplicativeMonad/Applicative.lean L151](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L151)). A hand-built list of errors is no better: "it's easy to lose track of an error message or two" ([FunctorApplicativeMonad/Applicative.lean L153-L154](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L153-L154)).
  - Error trees beat flat lists: errors gathered through `<|>` "can be difficult to read, because inclusion in the list of errors simply means that the error can be reached through *some* code path" ([FunctorApplicativeMonad/Alternative.lean L311](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Alternative.lean#L311)).
- **Indexing.** Two alternatives follow from FPIL's ordering:
  - First choice: "One of the easiest ways to make indexing safe is to have the function that performs a lookup into a data structure take the required evidence of safety as an argument." ([PropsProofsIndexing.lean L287](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/PropsProofsIndexing.lean#L287))
  - Otherwise: "In cases where it's not practical to prove that an indexing operation is in bounds, there are other alternatives" ([PropsProofsIndexing.lean L331](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/PropsProofsIndexing.lean#L331)), namely `xs[i]?` and then `xs[i]!`.
  - The book's code has 25 `[i]?`, 1 `[i]!`, and no `panic!`, `get!` or `getD` (survey §6).
- **When an `Option` isn't worth it.** For `zip` on unequal lengths, an `Option`/`Except` result "would introduce a burden that may not be worth the safety" ([DependentTypes/IndexedFamilies.lean L247](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/IndexedFamilies.lean#L247)).
- **Programs.** The CLI examples print to stderr and return an exit code from `main : List String → IO UInt32` (paraphrase).

### Termination and recursion (Q15)

**When `partial` is right.**
- Only when termination truly can't hold. For a loop over a possibly infinite stream: "In cases like this, there is no alternative to declaring the function `partial`" ([HelloWorld/Cat.lean L107](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Cat.lean#L107)). A structurally recursive function "does not need to be marked `partial`" ([HelloWorld/Cat.lean L199](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Cat.lean#L199)).
- Directory trees: "Lean's logic has no way to know that directory trees are finite" ([MonadTransformers/ReaderIO.lean L127](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L127)).
- Not needed for proofs: "In an application that just needs to produce JSON strings and doesn't need to mathematically reason about the process, having the function be `partial` is not likely to cause problems." ([TypeClasses/Coercions.lean L486](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L486))
- Costs: partial functions "can't be unfolded during type checking or in proofs [...]. Additionally, showing that a function that is expected to terminate actually always does terminate removes one more potential source of bugs." ([ProgramsProofs/Summary.lean L110-L112](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L110-L112))

**Recommended workflow.**

> A good way to write recursive functions is to begin by declaring them `partial` and debugging them with testing until they return the right answers. Then, `partial` can be removed and replaced with a `termination_by` clause. Lean will place error highlights on each recursive call for which a proof is needed that contains the statement that needs to be proved. Each of these statements can be placed in a `have`, with the proof being `sorry`. If Lean accepts the program and it still passes its tests, the final step is to actually prove the theorems that enable Lean to accept it. This approach can prevent wasting time on proving that a buggy program terminates. ([ProgramsProofs/Summary.lean L121-L126](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L121-L126))

The same advice appears where the workflow is used: [ProgramsProofs/InsertionSort.lean L151](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L151) and [ProgramsProofs/Inequalities.lean L648-L649](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Inequalities.lean#L648-L649). `sorry` "isn't intended for use in production code or final proofs" ([ProgramsProofs/Inequalities.lean L652](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Inequalities.lean#L652)), and "keeping it in the code is dangerous" because a false proof can let an out-of-bounds access through to run time ([ProgramsProofs/Summary.lean L99](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L99)).

> Typically, `let` is used to define names that refer to interesting values, while `have` is used to locally prove propositions that can be found when Lean is searching for evidence that an array lookup is in-bounds or that a function terminates. ([ProgramsProofs/Inequalities.lean L658](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Inequalities.lean#L658))

**Getting termination for free.**
- Library combinators: a right fold "can be used to make it clear to the termination checker that the function terminates" ([DependentTypes/UniversePattern.lean L259](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/UniversePattern.lean#L259)).
- Precondition arguments: taking evidence that the divisor is nonzero lets Lean prove `div` terminates automatically (paraphrase).
- Loops: replace `partial` stream recursion with `repeat`/`while` (above).

The book's code: 8 `partial`, 14 `termination_by`, no `decreasing_by` (survey §7). Final versions put termination facts in anonymous `have`s inside the body ([InstrumentedInsertionSort.lean L26-L33](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/examples/Examples/ProgramsProofs/InstrumentedInsertionSort.lean#L26-L33)).

### Invariants and proofs about programs (Q0b, Q16, Q18)

> In Lean, it is conventional to declare theorems with the `theorem` keyword instead of `def`. This helps readers see which declarations are intended to be read as mathematical proofs, and which are definitions. ([PropsProofsIndexing.lean L130-L131](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/PropsProofsIndexing.lean#L130-L131)) ... Because the details of a proof don't matter for later proofs, using the `theorem` keyword enables greater parallelism in the Lean compiler. ([PropsProofsIndexing.lean L134](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/PropsProofsIndexing.lean#L134))

**When to prove.** The closest any Lean source comes to Q16:

> Proofs allow elision of run-time bounds checks, they render many tests unnecessary, and they provide an extremely high level of confidence in a program without introducing any runtime performance overhead. However, proving theorems about programs can be time consuming and expensive, so other tools are often more economical. ([ProgramsProofs.lean L40-L41](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs.lean#L40-L41))

> In this way, the slow, straightforward program can serve as a specification for the fast, complicated version. ([ProgramsProofs.lean L37](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs.lean#L37)) ... It can be useful to keep the original version of the program that is more clearly correct, and then use it as an executable specification for the optimized version. ([ProgramsProofs/Summary.lean L58](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L58))

> After testing both versions of the program on examples to rule out simple bugs, proofs can be used to show once and for all that the programs are equivalent. ([ProgramsProofs/TailRecursionProofs.lean L20](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/TailRecursionProofs.lean#L20))

**Proof style.**

> Each style of proof can be appropriate to different circumstances. The detailed proof script is useful in cases where beginners may be reading the code, or where the steps of the proof provide some kind of insight. The short, highly-automated proof script is typically easier to maintain, because automation is frequently both flexible and robust in the face of small changes to definitions and datatypes. The recursive function is typically both harder to understand from the perspective of mathematical proofs and harder to maintain, but it can be a useful bridge for programmers who are beginning to work with interactive theorem proving. ([ProgramsProofs/Inequalities.lean L459-L462](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Inequalities.lean#L459-L462))

- Tactics: "Proofs written with tactics are easier to maintain over time, because flexible automation can paper over small changes to definitions." ([PropsProofsIndexing.lean L172](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/PropsProofsIndexing.lean#L172)) A proof written as a recursive function "does not always do a good job of expressing the intentions behind the proof" ([TacticsInductionProofs.lean L57](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TacticsInductionProofs.lean#L57)).
- Golf: "a common pattern for expert users is to take care of a number of simple cases with powerful tactics like `simp`, allowing them to focus the text of the proof on the interesting cases. Additionally, these proofs tend to be more robust in the face of small changes [...]. The game of tactic golf is a useful part of developing good taste and style when writing proofs." ([TacticsInductionProofs.lean L312-L314](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TacticsInductionProofs.lean#L312-L314))
- Robustness: "the use of `exact` is somewhat fragile", because golfing may rename the hypothesis; prefer `assumption` ([TacticsInductionProofs.lean L247](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TacticsInductionProofs.lean#L247)). "For structured, readable proofs, the `with` syntax is convenient. It complains if any cases are missing" ([TacticsInductionProofs.lean L263](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TacticsInductionProofs.lean#L263)).
- Final forms: proofs end as `fun_induction f <;> grind […]` or `induction t <;> simp +arith […, *]`.

### Tests (Q21)

FPIL teaches no test mechanism: no `#guard_msgs`, no `lake test`, no test layout. It does say three relevant things:
- **Types replace some tests.** Types are "lightweight specifications [...] obviating the need for certain classes of unit test" ([GettingToKnow/Summary.lean L57](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Summary.lean#L57)), and proofs "render many tests unnecessary" (above). But test before proving ([ProgramsProofs/TailRecursionProofs.lean L20](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/TailRecursionProofs.lean#L20)), and test what proofs can't see, such as copying.
- **`#eval` is not a test harness.** "Quickly testing `IO` actions with `#eval` can be much more convenient that compiling and running whole programs. However, there are some limitations." ([HelloWorld/Conveniences.lean L213](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L213)) In particular, "the `IO` action is re-executed whenever Lean needs to update the diagnostic information that it provides to users, and this can happen at unpredictable times." ([HelloWorld/Conveniences.lean L216](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/Conveniences.lean#L216))
- **Examples need comments.** "In source files, `example` declarations are best paired with comments that explain how the example illustrates the concepts of the library." ([TypeClasses/Conveniences.lean L111](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L111))

The book checks its own examples with a local `#check_msgs` command (438 uses in `examples/`). It is defined in `examples/ExampleSupport.lean` as "A version of `#guard_msgs` that leaves the messages in the log for extraction" ([L266-L272](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/examples/ExampleSupport.lean#L266-L272)). That is book infrastructure, not taught practice.

### Modules, visibility and projects

> The module name hierarchy is decoupled from the namespace hierarchy. In Lean, modules are units of code distribution, while namespaces are units of code organization. ([HelloWorld/StartingAProject.lean L143-L144](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StartingAProject.lean#L143-L144))

- **`protected`:** "`protected` means that the full name `EST.pure` is needed even if the `EST` namespace has been opened" ([Monads/IO.lean L153](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/IO.lean#L153)). Shown, not recommended.
- **`open`:** `open X in` before an expression or command, file-level `open`, selective `open Nat (toFloat)` and `export`, with no preference stated (Q23). The code has 80 top-level `open`s and 52 `open … in` (survey §10).
- **Absent:** no `private`, no module system (`module`, `public`), and no docstrings or module docs anywhere in the example code (survey §10–11).

## Explicit "don't"s

Statements that call a pattern poor, each paired in the book with a better version. This is evidence for [Q0c](../open-questions.md):

| Don't | Do instead | Link |
|---|---|---|
| copy fields by hand to update a structure | `{ p with x := 0 }` | [GettingToKnow/Structures.lean L243](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L243) |
| construct structures positionally (`Point.mk 1.5 2.8`) | `{ x := 1.5, y := 2.8 }` | [GettingToKnow/Structures.lean L325](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L325) |
| use `Sum String String` for domain data | a custom inductive with informative constructors | [GettingToKnow/Polymorphism.lean L560](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L560) |
| match a recursive function's two arguments as a pair | match them simultaneously | [GettingToKnow/Polymorphism.lean L732](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L732) |
| coerce `Int` to `Nat` | coerce only where the target represents every source value | [TypeClasses/Coercions.lean L217](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L217) |
| define `Monad List` | a lazy search monad (`Many`) | [DependentTypes/TypedQueries.lean L647](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/TypedQueries.lean#L647) |
| use default instances freely | "Be selective" | [TypeClasses/OutParams.lean L157](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/OutParams.lean#L157) |
| `seq (pure f) x` | `f <$> x` | [FunctorApplicativeMonad/Alternative.lean L133](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Alternative.lean#L133) |
| `get`, compute, `set` the state | `modify` | [MonadTransformers/Transformers.lean L434](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Transformers.lean#L434) |
| exit a `forM` via `OptionT` | `for … break` | [MonadTransformers/Do.lean L449](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L449) |
| `continue` to skip non-matches | early `return` | [MonadTransformers/Do.lean L493](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/Do.lean#L493) |
| frequent `▸` casts to unstick indices | redesign the types, or use subtypes | [DependentTypes/Summary.lean L98](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Summary.lean#L98) |
| `Hashable` that disagrees with `BEq`; `Functor` that moves data | lawful instances | [TypeClasses/StandardClasses.lean L511](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L511) |
| `exact ih` after golfing | `assumption` | [TacticsInductionProofs.lean L247](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TacticsInductionProofs.lean#L247) |
| leave `sorry` in code | prove it, or keep the function `partial` | [ProgramsProofs/Summary.lean L99](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L99) |

## Measured: the book's example code

`examples/` measured as an extra survey column (opt-in `FPIL` in `scripts/leanlex.py`). The code includes deliberately broken examples and successive drafts of the same function, so counts weight drafts. `example`, `variable` and `section` counts are inflated by the book's hover-link scaffolding (`example := String.drop`) and are left out.

| Measure | FPIL | Std | Lake |
|---|---|---|---|
| nonblank lines | 14,546 | 162,450 | 27,001 |
| theorems / defs | 172 / 666 | 20,937 / 4,584 | 24 / 2,529 |
| `fun … =>` share of lambdas | 98.9% (0 `↦`) | 99.3% | 97.3% |
| named instances | 0 of 133 | 8.1% | 1.0% |
| split headers continuing at +4 | 92.5% | 98.8% | 10.6% |
| match arms at `match` column | 98.3% | 99.4% | 99.7% |
| `let rec` / `where` helpers | 15 / 1 | 21 / 113 | 7 / 101 |
| `pure` / `return` in program code | 226 / 17 | 301 / 560 | 134 / 867 |
| `partial` / `termination_by` / `decreasing_by` | 8 / 14 / 0 | 62 / 122 / 5 | 51 / 5 / 2 |
| `[i]?` / `[i]!` / `panic!` | 25 / 1 / 0 | 19 / 7 / 45 | 151 / 47 / 5 |
| `private` decls | 0 | 2.1% | 0.1% |
| docstrings on public defs | 0% | 70.6% | 55.6% |
| line length p95 / p99 | 59 / 83 | 94 / 109 | 86 / 100 |
| type binders named with Greek letters | 82.9% | 76.3% | 77.3% |

## Reasons given

Most rules carry a reason inline. The kinds, roughly by frequency:
- **Readers and reviewers:** annotations, named intermediates, `theorem`, deriving, leading dot in review tools, `⟨⟩` revealing internals.
- **Maintenance under change:** structure update, deriving, tactics, automated proofs, stdlib transformers.
- **Error localisation and quality:** annotations, coercion failures, definitional-equality errors.
- **Bugs prevented:** `modify` vs `set`, `Option` vs null, separate structures, laws, `sorry`, termination proofs.
- **Provability:** `partial`, logging outside `IO`, effects in types.
- **Performance:** arrays, uniqueness, `Ord.compare`, `modify`, subtypes over custom inductives, free newtypes.
- **Caller convenience:** precise types need instances, implicit arguments, outParams, subtypes internal to the library.

Naming conventions are stated without reasons.

## What transfers to general-purpose Lean

- Nearly everything. FPIL is about programs, and its proof material is the program-proof kind (termination, equivalence of fast and slow versions, invariants), not mathematics.
- The strongest, reasoned rules are guide-ready:
  - type annotations; structure update; custom types over `Prod`/`Sum`; deriving;
  - lawful and coherent instances; weakest abstraction for functions;
  - coercion criteria; `modify` over `get`/`set`; `abbrev` for monad stacks; stdlib transformers;
  - subtypes kept internal to a library; indexed families rarely;
  - the partial-then-prove workflow; `let` for values and `have` for proofs.
- Chapter 6 (monad transformers) is the only Lean material on application structure (Q14). Chapter 8's introduction is the only Lean statement on the economics of proving (Q16).
- The "don't" table supplies good/bad pairs in bbatsov's format.
- Hedges ("typically", "generally") mark most rules as defaults, not mandates.
- The code itself is a weaker guide than the prose: it is pedagogical, contains drafts and has the inconsistencies listed below.

## Conflicts with other sources

- **autoImplicit.** FPIL relies on auto-bound implicits. Mathlib disables them, Std disables them in 70 files, and core's default is on ([mathlib-linters](mathlib-linters.md)). No open question covers this yet.
- **Theorem names.** FPIL's mixed casings, and its conversion of `insertSorted` to `insert_sorted_…`, contradict core-naming ([lean-core-naming](lean-core-naming.md)).
- **`do` endings and let-else.** FPIL ends `do` blocks with `pure` and never shows let-else, which core-style recommends ([lean-core-style](lean-core-style.md)). Stdlib program code prefers `return`.
- **Blank lines inside declarations.** Used in FPIL's `main`s, linted by Mathlib's `emptyLine` ([mathlib-style](mathlib-style.md)).
- **Non-terminal `simp`.** FPIL's intermediate proofs run unsqueezed `simp […]` followed by `rw`. core-style asks to squeeze non-terminal `simp`, and Mathlib's `flexible` linter flags it ([lean-core-style](lean-core-style.md), [mathlib-linters](mathlib-linters.md)). FPIL's final forms are terminal (`<;> grind`).
- **Leading-dot constructors.** FPIL warns that they hurt reading in review tools, then uses them heavily from chapter 5 on.
- **Conversions.** `fromList` vs the stdlib's `ofList`.
- **The book revises itself.** Chapter 2's `partial def dump` is rewritten without `partial` in chapter 6.

## Caveats and unverified items

- **Version sensitivity.** Several APIs and features are recent and fix the edition to Lean ≥ 4.2x: `String.Slice`, `trimAscii`, `dropEnd`; range syntax `3...10` with `Std.Rco`; `fun_induction`; `grind`.
- **Dated claims.** "At the time of writing, Lean only eliminates direct tail calls" and the stack-overflow figures (216,856 elements) are explicitly dated.
- **Unverified:**
  - whether current Lean can prove `JSON.asString` terminating without `partial` (the book says it cannot);
  - the claim that dot notation sees through `abbrev` (stated by the book, not tested here).
- **Rendered vs source.** The rendered book was fetched on 2026-10-17 and matches the source toolchain (4.33.0). Its release history has not been updated since the 4.23.0 entry.
- **Correction to the earlier note.** It cited the "lift a repetitive segment into a helper function" quote to `Monads/Conveniences.lean L113`; the sentence is at [Monads.lean L113](https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads.lean#L113).
- **Counts.** The survey's regex lexer is approximate ([stdlib-survey.md](../stdlib-survey.md#how-to-read-the-numbers-caveats-common-to-all-sections)). FPIL counts include drafts and error examples.
