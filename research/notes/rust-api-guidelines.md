# Rust API Guidelines

| Field | Value |
|---|---|
| URL | https://rust-lang.github.io/api-guidelines/ (source: https://github.com/rust-lang/api-guidelines) |
| Author / org | Rust library team (rust-lang) |
| Date / version | `97a0969cb07fe4cabb0eed8a56234053f47d83dc`, last commit 2025-07-07 |
| License | Dual **Apache-2.0 OR MIT**, at your option (repo README "License" section; files `LICENSE-APACHE`, `LICENSE-MIT`). Contributions are dual licensed. Quote and adapt freely with notices. |
| Scope & audience | Rust library/crate authors |
| Kind | community advice ("only guidelines, some more firm than others") |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/rust-api-guidelines-naming.md`, `rust-api-guidelines-checklist.md`, `rust-api-guidelines-rest.md` (interoperability, predictability, type-safety, dependability, documentation, future-proofing, flexibility) |

## Summary
A checklist of 54 numbered guidelines, each with a stable id `C-NAME`, an anchor, a short imperative title, a rationale and std-library examples. Organized by quality (naming, interoperability, macros, documentation, predictability, flexibility, type safety, dependability, debuggability, future proofing, necessities). It is the strongest model for API naming conventions (`as_`/`to_`/`into_`, getters without `get_`) and is also a candidate model for the *format* of a Lean guide (checklist + detail pages).

## Rules
Status of the guide ([about.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/about.md)):
> These are only guidelines, some more firm than others. ... These guidelines should not in any way be considered a mandate that crate authors must follow, though they may find that crates that conform well to these guidelines integrate better with the existing crate ecosystem than those that do not.

Checklist ([checklist.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/checklist.md)) shape: bullet per guideline with a checkbox and `([C-ID])` link.

Naming ([naming.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/naming.md)):
- [C-CASE](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/naming.md#L2-L40): UpperCamelCase for types/traits/variants, snake_case for values; "In `UpperCamelCase`, acronyms and contractions of compound words count as one word: use `Uuid` rather than `UUID`"; "a 'word' should never consist of a single letter unless it is the last 'word'. So, we have `btree_map` rather than `b_tree_map`, but `PI_2` rather than `PI2`."
- [C-CONV](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/naming.md#L42-L110) "Ad-hoc conversions follow `as_`, `to_`, `into_` conventions":
  > | `as_` | Free | borrowed -> borrowed | `to_` | Expensive | ... | `into_` | Variable | owned -> owned (non-Copy types) |
  > Conversions prefixed `as_` and `into_` typically _decrease abstraction_ ... Conversions prefixed `to_`, on the other hand, typically stay at the same level of abstraction but do some work to change from one representation to another.
  > When a type wraps a single value to associate it with higher-level semantics, access to the wrapped value should be provided by an `into_inner()` method.
  > If the `mut` qualifier ... constitutes part of the return type, it should appear as it would appear in the type ... `Vec::as_mut_slice` ... preferred over `as_slice_mut`.
- [C-GETTER](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/naming.md#L112-L160): "With a few exceptions, the `get_` prefix is not used for getters in Rust code." (`first()`, `first_mut()`); "The `get` naming is used only when there is a single and obvious thing that could reasonably be gotten". For checked accessors: "consider adding unsafe `_unchecked` variants": `get(&self, index) -> Option<&V>` and `unsafe fn get_unchecked(...) -> &V`.
- [C-ITER](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/naming.md#L162-L200) `iter`, `iter_mut`, `into_iter`; [C-ITER-TY] iterator type names match the method; [C-FEATURE] no placeholder words in feature names; [C-WORD-ORDER](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/naming.md#L320-L345) "Names use a consistent word order" (e.g. `ParseIntError`, `ParseBoolError`, not mixed orders).

Other checklist items relevant to Lean (titles only; details in the raw copy):
- C-COMMON-TRAITS (types eagerly implement common traits: Copy, Clone, Eq, PartialEq, Ord, PartialOrd, Hash, Debug, Display, Default); C-CONV-TRAITS; C-GOOD-ERR ("Error types are meaningful and well-behaved": implement `Error`, `Send`, `Sync`).
- C-FAILURE: "Error conditions should be documented in an 'Errors' section"; "Panic conditions should be documented in a 'Panics' section" ([documentation.md L65-L110](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/documentation.md#L65-L110)); C-EXAMPLE every item has an example; C-QUESTION-MARK examples use `?`, not `unwrap`.
- C-VALIDATE ([dependability.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/dependability.md#L4-L30)): "Rust APIs do _not_ generally follow the robustness principle ... Instead, Rust code should _enforce_ the validity of input whenever practical" with mechanisms in order: static enforcement (types), dynamic enforcement, debug-only checks.
- C-NEWTYPE, C-CUSTOM-TYPE ("Arguments convey meaning through types, not `bool` or `Option`"), C-BUILDER ([type-safety.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/type-safety.md)).
- C-CTOR constructors are static inherent methods (`new`, `with_*`, `from_*`); C-METHOD functions with a clear receiver are methods; C-OVERLOAD operator overloads unsurprising ([predictability.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/predictability.md)).
- C-STRUCT-PRIVATE ("Making a field public is a strong commitment"), C-SEALED, C-NEWTYPE-HIDE ([future-proofing.md](https://github.com/rust-lang/api-guidelines/blob/97a0969cb07fe4cabb0eed8a56234053f47d83dc/src/future-proofing.md#L55-L63)).
- C-DEBUG all public types implement Debug.

## Reasons given
Each guideline has prose rationale, usually with a "Examples from the standard library" list, i.e. justified by existing practice. Conversions are justified by a cost/ownership table; `get_` removal by brevity and convention.

## What transfers to general-purpose Lean
- Cost-signalling prefixes: Lean already has `toFoo` (structure parent projections and conversions), `ofFoo`, `Foo.get`, `getD`, `get?`, `get!`; a Lean guide can adopt the *idea* of reserving prefixes for cost/ownership (`as_` free, `to_` expensive) — Lean has no ownership notion in the type but `Array` in-place updates and `@&` borrowing are comparable.
- Accessor family `foo` / `foo_mut` / `foo_unchecked` vs Lean's `get`, `get?`, `get!`, `getD`, `[i]`, `[i]?`, `[i]!`, `[i]'h`: a comparison table is a natural content for the naming topic.
- "Document Errors and Panics sections" maps to docstring sections for `panic!`/`throw` conditions.
- C-VALIDATE order (types before runtime checks) fits Lean (subtypes, hypotheses as arguments).
- The checklist+id format: stable ids per rule.
- Ownership, Send/Sync, macros (partially: Lean macros differ), Cargo metadata: do not transfer.

## Caveats and unverified items
- Line anchors above are approximate ranges into the checked-out files; the guidelines also have HTML anchors (e.g. `naming.html#c-conv`).
- Lean's own naming conventions (`vendor/repos/lean4/doc/std/naming.md`) were not compared here.
