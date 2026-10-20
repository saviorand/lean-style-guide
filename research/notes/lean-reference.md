# The Lean Language Reference

| Field | Value |
|---|---|
| URL | https://lean-lang.org/doc/reference/latest/ (source: https://github.com/leanprover/reference-manual/tree/400f1682df64bc00e485215bfa4398d24c0f220c) |
| Author / org | Lean FRO (reference-manual repo; individual authors not recorded in the files read, **unverified**) |
| Date / version | Repo commit `400f1682df64bc00e485215bfa4398d24c0f220c` (2026-10-15), `lean-toolchain` = v4.36.0-rc1. Site "latest" tracks Lean releases; announced 2024-12-16 ([blog](https://lean-lang.org/blog/2024-12-16-introducing-the-lean-language-reference)) |
| License | Apache 2.0 (`LICENSE` in repo) |
| Scope & audience | Users who need exact semantics: "first and foremost a reference work in which Lean users can look up detailed information, rather than a tutorial" (repo `README.md`) |
| Kind | descriptive (normative about semantics, not about style) |
| Lean version | Lean 4 |
| Raw copy | source clone `vendor/repos/refman` (not copied to pages) |

## Summary
The Reference is a language specification and does not contain a style guide. A grep for "convention", "recommend", "idiomatic", "best practice", "style" across `Manual/` found about 25 hits, most about unrelated meanings. The relevant ones are a handful of "by convention" statements about API shape and instance idioms, descriptions of `partial`/`implemented_by` semantics, and guidance on custom `Repr` instances. The manual's own contributor rules (`CONTRIBUTING.md`) are about documentation writing, not Lean code. Base for links: `https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/`.

## Rules (statements of convention found)
### API and naming conventions
> By convention, a collection type `Coll` provides a function `Coll.iter` that returns an iterator over the elements of a collection. ([Iterators.lean L121](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Iterators.lean#L121))

> In addition to the general functions described here, there are some functions that are conventionally defined as part of the API of in the namespace of each collection type: `mapM` [...] `forM` [...] `filterM` ([Monads/API.lean L25](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Monads/API.lean#L25))

> `T.Raw` is the version of type `T` without its invariants [...] `T.Raw.WF` is the corresponding well-formedness predicate. ([BasicTypes/Maps.lean L163](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/BasicTypes/Maps.lean#L163)): the naming scheme for raw containers used in nested inductives.

> By convention, commands that are intended for interactive use rather than as part of a durable code artifact are prefixed with `#`. ([Interaction.lean L29](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L29))

### Instances for recursive types
> There is a standard idiom to work around this limitation: define a recursive function independently of the instance, and then refer to it in the instance definition. By convention, these recursive functions have the name of the corresponding method, but are defined in the type's namespace. ([Classes/InstanceDecls.lean L119-L123](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Classes/InstanceDecls.lean#L119))

### `Repr` instances
> When writing a custom `Repr` instance, please follow these conventions: [Precedence, then further items] ([Interaction/FormatRepr.lean L584](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction/FormatRepr.lean#L584)). Instances "should generally not parenthesize recursive calls to `reprPrec`"; `Repr.addAppParen` and `reprArg` are the helpers. Remaining conventions not recorded.

### Termination, `partial`, `unsafe`, `implemented_by`
> While most Lean functions can be reasoned about in Lean's type theory as well as compiled and run, definitions marked `partial` or `unsafe` cannot be meaningfully reasoned about. From the perspective of the logic, `partial` functions are opaque constants ([RecursiveDefs.lean L195-L196](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs.lean#L195))

> The function's return type must be inhabited; this ensures soundness. ([L211](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs.lean#L211)) And: "Even though partial functions are not unfolded by the kernel, it is still possible to reason about other functions that call them so long as this reasoning doesn't depend on the implementation of the partial function itself." (L226)

> Frequently, unsafe operators are used to write fast code [...] safe Lean code may be replaced with unsafe Lean code for runtime programs. This is accomplished by adding the `implemented_by` attribute [...] While this does not threaten Lean's soundness as a logic [...] it is still risky. ([L298-L303](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs.lean#L298))

Other recursion options described (not recommended between): structural recursion, well-founded recursion with `termination_by`/`decreasing_by`, `partial_fixpoint` ("Even in cases where the defining equation fully describes the function's behavior and a termination proof [...] would be possible, it may simply be more convenient to" use it; [PartialFixpoint.lean L48](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs/PartialFixpoint.lean#L48)).

### Arrays and linearity
> Lean code that uses an array in such a way that there's only ever one unique reference (that is, uses it linearly) avoids the performance overhead of persistent data structures while still being as convenient to write, read, and prove things about as ordinary pure functional programs. ([BasicTypes/Array.lean L28-L38](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/BasicTypes/Array.lean#L28))

### `do` notation, IO, errors
`do` "provides familiar syntax for sequencing effectful operations, early return, local mutable variables, loops, and exception handling" ([Monads/Syntax.lean L210](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Monads/Syntax.lean#L210)); Early Return section L431, "Not all monads include early return." Exception monads and `MonadExcept` in `Monads/Zoo`. No stylistic guidance on `do` usage.

### Attributes
`@[macro_inline]` is described in BasicTypes.lean L259 (used so `&&`/`||` short-circuit). `@[inline]`/`@[specialize]` have no dedicated recommendations in the files grepped (**unverified**, may be in sections not found).

### Linters and tooling
`Linters.lean` documents `linter.unusedVariables`, `linter.all`, `lake lint`, "Code Quality Metrics" and how to implement linters; no recommendation of which to enable ([Linters.lean L37-L183](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Linters.lean#L37)). `ValidatingProofs.lean L166`: "We recommend running `lean4checker` as part of CI".

### Modules and visibility
`SourceFiles.lean` documents the module system (`module`, `public import`, `meta import`, `import all`, public vs private sections; [Namespaces.lean L110](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Namespaces.lean#L110)). Descriptive only; includes a remark that porting Mathlib to the module system "has shown savings close to 50%" (L328, **unchecked** in context).

### Module system: guidance for library authors (read 2026-10-20)
Base: `https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/SourceFiles.lean`.

> Prefix the remainder of the file with `@[expose] public section` or, for programming-focused files, with `public section`. The latter should be used for programs that will be run but not reasoned about. ([L843-L844](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/SourceFiles.lean#L843-L844))

> After an initial build under the module system succeeds, the dependencies between modules can be iteratively minimized. In particular, removing uses of `public` and `@[expose]` will help avoid unnecessary rebuilds. ([L847-L848](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/SourceFiles.lean#L847-L848))

> As a guideline, it is usually preferable to keep the amount of `meta` annotations as small as possible. This avoids locking otherwise-reusable declarations into the meta phase and it helps the build system avoid more rebuilds. ([L791-L792](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/SourceFiles.lean#L791-L792)). Helpers go in a separate, non-`meta` module, imported with `public meta import` by the module that registers the metaprogram (L793-L795).

The file says `@[expose]` is preferable to `import all` "if anyone outside your library might feasibly require the same access" ([L826](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/SourceFiles.lean#L826)), and that `prelude` is only for Lean's own source (L225-L233).

### Concurrency (read 2026-10-20)
> Generally speaking, sequential programs that interact with the operating system can use `IO` alone. Parallel programs should use `Task`s. `Async` is most appropriate when a program may spend a significant amount of time waiting on external events or I/O. ([IO/Async.lean L34-L36](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/IO/Async.lean#L34-L36))

- "Pure tasks should typically be created with `Task.spawn`" ([IO/Threads.lean L62](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/IO/Threads.lean#L62)).
- "Impure tasks should use `IO.checkCanceled` to react to cancellation" (L147).
- Under `ContextAsync`, concurrent tasks "should be started with the helpers that are specifically designed for" it, so that cancellation works (IO/Async.lean L1424).
- `recvSelector` and `recv` "should not be used on the same channel" (L793).

### Instances and deriving (read 2026-10-20)
- `BEq` and `Hashable` must agree: "two values equated by `BEq.beq` should always have the same hash" ([Classes/BasicClasses.lean L30](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Classes/BasicClasses.lean#L30)). Ordering instances "should be in agreement with `Ord`, `LT`, and `LE` instances, if they exist, but there is no mechanism to enforce this" (L197).
- "Code that uses instance-implicit parameters should be prepared to consider all instances as equivalent." ([Classes/InstanceSynth.lean L455-L457](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Classes/InstanceSynth.lean#L455-L457))
- A `deriving` clause on a class is legal but should be treated as "an advanced feature" ([Classes.lean L142](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Classes.lean#L142)). The deriving chapter (`Classes/DerivingHandlers.lean`) documents how to write handlers. It says nothing about which classes to derive.

### Notation and FFI (read 2026-10-20)
- "Syntax extensions should be used in _output_ as well as in _input_" (write unexpanders or delaborators for new notation) ([NotationsMacros/Delab.lean L33](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/NotationsMacros/Delab.lean#L33)). Macros that build syntax without quotations "should also ensure hygiene by some other means" (NotationsMacros.lean L183).
- FFI: "The current interface was designed for internal use in Lean and should be considered unstable" ([Runtime.lean L340](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Runtime.lean#L340)). C code for `@[extern]` is built through a Lake custom target and `moreLinkObjs` (Language/InductiveTypes.lean L474-L477).
- File I/O: call `Handle.flush` when buffers must reach the file (IO/Files.lean L110).

### Testing
See [testing-practice](testing-practice.md): `#guard_msgs` files as Lake test drivers (Interaction.lean L552-L553) and the `meta import` trap for `#eval` tests (L95-L96).

### Numeric literal style
> (While it is possible to write the number 123 as `1_2__3`, this is not recommended.) ([Terms.lean L959](https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Terms.lean#L959))

## Reasons given
Semantic: soundness (inhabited return types), logical opacity of `partial`, performance (linear arrays, `implemented_by`). Conventions themselves usually come without reasons.

## What transfers to general-purpose Lean
- The reference is the right place to cite semantics for rules about `partial`, `implemented_by`, instances for recursive types, iterator and monadic-collection API shape, `Repr` instances, and the module system.
- It does not choose between structural recursion, well-founded recursion, `partial`, or `partial_fixpoint`; any guidance on that must come from elsewhere (see `fro-blog`).

## Caveats and unverified items
- Search was keyword-based. On 2026-10-20 a second pass took the advice-word lines (should, prefer, recommend, avoid, convention…) from the chapters on runtime, source files, classes, monads, IO, namespaces, inductive types, notation and build tools, and read the module-system and Async passages in context. Prose that gives no advice was still not read. `@[inline]`/`@[specialize]` turned up no advice in that pass; [author-survey](../author-survey.md) shows their use is author-dependent.
- Quoted line numbers are for the commit above; the live "latest" site may differ.
- Manual's own writing rules (US English, Chicago Manual of Style 18, `deftech`/`tech` roles) are in its `CONTRIBUTING.md`; this overlaps with `lean-core-doc-style`.
