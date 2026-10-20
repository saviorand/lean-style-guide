# Mathlib naming conventions

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/contribute/naming.html |
| Author / org | Lean community / Mathlib maintainers (`templates/contribute/naming.md`) |
| Date / version | Served 2026-10-17; source last changed 2026-09-15, [`4bfcf92`](https://github.com/leanprover-community/leanprover-community.github.io/blob/4bfcf92fd4218e9a3497ed4fb3ffb90fe39d2442/templates/contribute/naming.md). Page says "This guide is written for Lean 4." |
| License | MIT (repo metadata) |
| Scope & audience | Mathlib contributors; the casing rules (1-7) also match Lean core/Batteries practice |
| Kind | normative (Mathlib) |
| Lean version | Lean 4; it contrasts itself with Lean 3 |
| Raw copy | `vendor/pages/community/mathlib-naming.md` |

## Summary
Defines file names (UpperCamelCase), a seven-rule casing scheme (`snake_case` for proofs, `UpperCamelCase` for types/props, `lowerCamelCase` for other data and functions), a dictionary of symbol names, rules for dots/namespaces, coercion names, and a long catalogue of theorem-name patterns (`_of_`, `_iff_`, `.ext`, `_injective`, `Is`/`Has` prefixes). Rules 1-7 and the dots/namespace/`.ext`/`Is` parts are general; the dictionary, lattice/algebra/set sections, and axiomatic-description sections are mathematics-specific. It has no guidance on naming programs beyond rules 3-4 ("functions named like their return values").

## Rules
> Unlike Lean 3, in which the convention was that all declarations used `snake_case`, in mathlib under Lean 4 we use a combination of `snake_case`, `lowerCamelCase` and `UpperCamelCase` according to the following naming scheme. ([Capitalization](https://leanprover-community.github.io/contribute/naming.html#capitalization))

> 1. Terms of `Prop`s (e.g. proofs, theorem names) use `snake_case`.
> 2. `Prop`s and `Type`s (or `Sort`) (inductive types, structures, classes) are in `UpperCamelCase`. ...
> 3. Functions are named the same way as their return values (e.g. a function of type `A → B → C` is named as though it is a term of type `C`).
> 4. All other terms of `Type`s (basically anything else) are in `lowerCamelCase`.
> 5. When something named with `UpperCamelCase` is part of something named with `snake_case`, it is referenced in `lowerCamelCase`.
> 6. Acronyms like `LE` are written upper-/lowercase as a group, depending on what the first character would be.
> 7. Rules 1-6 apply to fields of a structure or constructors of an inductive type in the same way.

> `.lean` files in mathlib should generally be named in `UpperCamelCase`. ([File names](https://leanprover-community.github.io/contribute/naming.html#file-names))

> Declaration names use American English spelling. ([Spelling](https://leanprover-community.github.io/contribute/naming.html#spelling))

> We adopt the following naming guidelines to make it easier for users to guess the name of a theorem or find it using tab completion. ([Identifiers and theorem names](https://leanprover-community.github.io/contribute/naming.html#identifiers-and-theorem-names))

> A lemma of the form `(∀ x, f x = g x) → f = g` should be named `.ext`, and labelled with the `@[ext]` attribute. ... `f = g ↔ ∀ x, f x = g x` should be named `.ext_iff`. ([Extensionality](https://leanprover-community.github.io/contribute/naming.html#extensionality))

> Most predicates should be added as prefixes. Eg `IsClosed (Icc a b)` should be called `isClosed_Icc`, not `Icc_isClosed`. ([Predicates as suffixes](https://leanprover-community.github.io/contribute/naming.html#predicates-as-suffixes))

> If the class is a noun (or noun phrase) then its name should begin with `Is`. If however is it an adjective then its name does not need to begin with an `Is`. ([Prop-valued classes](https://leanprover-community.github.io/contribute/naming.html#prop-valued-classes))  (the `Has` prefix is allowed for predicates on data other than the explicit argument)

Stated exceptions: "`Ne` rather than `NE` to follow the example of `Eq`", `outParam`, intervals `Set.Icc`; "Any such exceptions should be discussed on Zulip."

Not covered: the `?`/`!`/`D` suffixes for `Option`/panic/default variants, `mk`/`of`/`to` conversion prefixes for programs, `Aux`/`_aux`, instance names. (Searched the page; `get?`, `getD`, `Array`, `List` as program API do not appear. `ofFoo`/`toFoo` appear only through the coercion section.) Lean core's `doc/std/naming.md` (line 69) covers `?`/`!` suffixes ([permalink-free local read](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#L69)); `getD` not checked there.

## Reasons given
- Theorem names are meant to be guessable and tab-completable (intro of the identifiers section).
- Rule 5 and the dictionary: since `UpperCamelCase` types become `lowerCamelCase` inside theorem names, the symbol dictionary stays valid for `And`, `Or`, `Iff`, `Eq` ([Dots](https://leanprover-community.github.io/contribute/naming.html#dots)).
- Coercion names: "motivated by the fact that coercions are reducible. This wasn't the case in Lean 3, and therefore many names are wrong still."
- No reason is given for the casing split itself; the history is on Zulip (see below).

## What transfers to general-purpose Lean
- Rules 1-7 transfer wholesale; they are the same rules Lean core uses (compare `lean4/doc/std/naming.md`, covered by another track).
- Rule 3 is the key program-facing rule: functions named by return type (so `Foo → Bar` returning a `Type` data value is `lowerCamelCase`; returning a structure type, `UpperCamelCase`).
- Theorem-name vocabulary (`_of_`, `_iff`, `_eq`, `.ext`) transfers for programs that carry proofs; the math dictionary does not.
- UpperCamelCase file names transfer.
- The guide gives no naming guidance for variants (`?`, `!`, `D`), constructors like `mk`/`ofX`, or `IO`/monadic actions.

## Caveats and unverified items
- Lean 3: the whole page is a reaction to Lean 3's all-`snake_case`. Origin of the Lean 4 scheme: mathlib4 porting; see the [Porting wiki, Naming convention](https://github.com/leanprover-community/mathlib4/wiki/Porting-wiki#naming-convention) (saved: `vendor/pages/community/mathlib-porting-wiki.md`, lines ~201-260), which repeats rules 1-5 and says mathport "will usually get the name wrong" for multiword lowerCamelCase inside snake_case. Decision history: `notes/zulip-naming.md`.
- A Lean-3 style duplicate of this page existed before the port; this note covers only the current Lean 4 page.
- Sections Names of symbols (logic/set/algebra/lattices), Axiomatic descriptions, groups-vs-groups-with-zero were skimmed headings only; they are math dictionaries.
