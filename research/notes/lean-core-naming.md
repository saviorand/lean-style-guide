# Lean standard library naming conventions (`doc/std/naming.md`)

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md |
| Author / org | Lean FRO / stdlib maintainer team |
| Date / version | lean4 commit `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` (2026-10-17), 4.37.0 pre-release |
| License | Apache 2.0 (lean4 `LICENSE`) |
| Scope & audience | Stdlib contributors; titled "Standard library naming conventions". Self-described as "a living document" with "very few hard rules, many heuristics" |
| Kind | normative (stdlib), with heuristic tone |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/lean-official/lean-core-naming.md` |

## Summary
The most complete official naming document. Roughly 80% of it concerns naming theorems and lemmas (a tree-traversal algorithm, special keywords such as `comm`/`assoc`/`inj`, left/right conventions). The parts relevant to programs are short: casing by kind (types, data, theorems), the `Is` prefix for predicates, putting declarations in the namespace of their type to enable dot notation, `?`/`!` suffixes, no primed names, acronym casing, and variable-name recommendations. Links below use base `https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md`.

## Rules
### Casing ([Prelude, L8](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L8))
> Identifiers use a mix of `UpperCamelCase`, `lowerCamelCase` and `snake_case`, used for types, data, and theorems, respectively.

> Structure fields should be named such that the projections have the correct names.

> [Types] When defining a type, i.e., a (possibly 0-ary) function whose codomain is Sort u for some u, it should be named in UpperCamelCase.

> [Data] When defining data, i.e., a (possibly 0-ary) function whose codomain is not Sort u, but has type Type u for some u, it should be named in lowerCamelCase.
([L64](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L64))

> If your data is morally fully specified by its type, then use the naming procedure for theorems described below and convert the result to lower camel case.

### Predicates ([L14](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L14))
> When defining a predicate, prefix the name by `Is`, like in `List.IsPrefix`. The `Is` prefix may be omitted if the resulting name would be ungrammatical, or the predicate depends on additional data in a way where the `Is` prefix would be confusing (like `List.Pairwise`), or the name is an adjective (like `Std.Time.Month.Ordinal.Valid`)

### Namespaces ([L23](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L23))
> Almost always, definitions and theorems relating to a type should be placed in a namespace with the same name as the type.

> Declarations in the root namespace will be relatively rare. The most common type of declaration in the root namespace are declarations about data and properties exported by notation type classes, as long as they are not about a specific type implementing that type class.

> Generally, place your theorem in the most specific namespace that appears in one of the hypotheses of the theorem.

> Thinking about which dot notations are convenient can act as a guideline for deciding where to place a theorem, and is, on occasion, a good reason to duplicate a theorem into multiple namespaces.

> [`Std` namespace, L55] New types that are added will usually be placed in the `Std` namespace and in the `Std/` source directory [...]. Inside the `Std` namespace, all internal declarations should be `private` or else have a name component that clearly marks them as internal, preferably `Internal`.

### Failure variants ([L64](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L64))
> If your function returns an `Option`, consider adding `?` as a suffix. If your function may panic, consider adding `!` as a suffix. In many cases, there will be multiple variants of a function; one returning an option, one that may panic and possibly one that takes a proof argument.

(`D` suffix for default-returning variants is taught by FPIL, not listed here; see `fpil`.)

### Theorem-name algorithm and keywords ([L71](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L71), [L171](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L171))
Includes: `_of_` joins conclusion and hypotheses; `iff` should be included in the name of iff-lemmas; "The more common you expect (or want) a theorem to be, the shorter you should try to make the name"; table of keywords (`refl`, `symm`, `trans`, `comm`, `assoc`, `inj`, `cancel`, `ext`, `mono`, ...); `def` as a lemma-name keyword "Avoid this for public APIs". Math/proof-oriented; not summarised further.

### Primed names ([L226](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L226))
> Avoid disambiguating variants of a concept by appending the `'` character (e.g., introducing both `BitVec.sshiftRight` and `BitVec.sshiftRight'`) [...] Prefer descriptive pairs `BitVec.sshiftRightNat`/`BitVec.sshiftRight`.

### Acronyms ([L230](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L230))
> For acronyms which are three letters or shorter, all letters should use the same case as dictated by the convention. For example, `IO` is a correct name for a type and the name `IO.Ref` may become `IORef` when used as part of a definition name and `ioRef` when used as part of a theorem name.

> For acronyms which are at least four letters long, switch to lower case starting from the second letter. For example, `Json` is a correct name for a type, as is `JsonRPC`.

> If an acronym is typically spelled using mixed case, this mixed spelling may be used in identifiers (for example `Std.Net.IPv4Addr`).

### Simp sets ([L238](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L238))
> Simp sets centered around a conversion function should be called `source_to_target`.

### Variable names ([L243](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L243))
"We make the following recommendations for variable names, but without insisting on them":
> Simple hypotheses should be named `h`, `h'`, or using a numerical sequence `h₁`, `h₂`, etc.
> `List`s should be named `l`, `l'`, `l₁`, etc, or `as`, `bs`, etc. [...] `xs`, `ys`, `zs` are allowed, but it is better if these are reserved for `Array` and `Vector`.
> `Array`s should be named `xs`, `ys`, `zs` [...] An array of arrays may be named `xss`.
> A common exception for `List` / `Array` / `Vector` is to use `acc` for an accumulator in a recursive function.
> `i`, `j`, `k` are preferred for numerical indices. Descriptive names such as `start`, `stop`, `lo`, and `hi` are encouraged when they increase readability.
> `n`, `m` are preferred for sizes [...] `w` is preferred for the width of a `BitVec`.

## Reasons given
- Core rationale ([intro, L1-L6](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L1-L6)): "easily guessable names (which are still reasonably short) make Lean users more productive", because finding a result by guessing its name (with autocomplete) "is faster and has lower friction than more sophisticated search tools".
- Primed names: "it is impossible to tell the difference without looking at the type signature, the documentation or even the code, and even if you know what the two variants are there is no way to tell which is which."
- `iff` in names: otherwise "users might try to `apply` it when the goal is `l.head? = none`".
- Namespaces: enables generalized projection (dot) notation.
- Casing, `Is` prefix, `?`/`!` and acronym rules: no reasons given.

## What transfers to general-purpose Lean
- Casing by kind, `Is` for predicates, namespace-per-type for dot notation, `?`/`!` suffixes, primed-name avoidance and acronym casing apply to any library.
- "Guessability" is a stated design value that generalises.
- `Std.`/`Internal` rules, root-namespace guidance for notation classes, and the theorem algorithm are stdlib/proof specific. Variable-name list is generic but mostly List/Array/BitVec oriented.
- Gaps: no rules for constructor names, type class and instance names (`instFoo...`), module/file names, `mk`-style function names (`ofX`/`toX`), `Monad`-variants (`M` suffix) or private helper names, despite stdlib practice (**unverified** whether other docs state them).

## Caveats and unverified items
- Explicitly "a living document" with "very few hard rules"; the guide says unhelpful suggestions are "probably safe to ignore".
- A few typos in the source (e.g. `antisymmm`, `Std.Hashmap`); table of keywords is partial.
- Companion file `naming-tree.svg` in the same directory illustrates the algorithm (not read).
