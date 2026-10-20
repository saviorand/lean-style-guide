# Idris 2 documentation: tutorial, totality, theorem proving, contributing

| Field | Value |
|---|---|
| URL | https://idris2.readthedocs.io/en/latest/ (source: https://github.com/idris-lang/Idris2/tree/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source) |
| Author / org | The Idris Community (Edwin Brady et al.) |
| Date / version | Idris2 commit `89ba32eb5eb325909bacd0d5411076ac28d166bb`, 2026-10-14 |
| License | Documentation: CC0 ("published under the Creative Commons CC0 License", [index.rst L11-L13](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/index.rst#L11-L13)). Code: BSD-3-style, "Copyright (c) 2020 Edwin Brady" (`LICENSE`); GitHub reports NOASSERTION. |
| Scope & audience | Idris 2 learners and contributors |
| Kind | descriptive (no style guide exists); one contributor note is normative-but-minimal |
| Lean version | n/a (Idris 2) |
| Raw copy | clone at `vendor/repos/Idris2`; no page copies |

## Summary
Idris 2 has no style or naming guide. Its contributor guide explicitly declines to prescribe style. The docs do carry design guidance in three places: the tutorial's totality section, the dependent-types sections (length-indexed vectors, dependent pairs), and the "Theorem Proving" tutorial, which treats proofs as ordinary values of equality types written beside the code. The `%default` pragma sets how strict the totality checker is.

## Rules
Style (none exists):
> Different people have different preferences about coding style. In general, we haven't been too prescriptive about this. If you're editing a source file, try to be consistent with the existing style choices made by previous authors. We may need to be more formal about this in future!
[CONTRIBUTING.md L55-L59](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/CONTRIBUTING.md#L55-L59)

Totality:
> By default, functions in Idris must be `covering`. That is, the patterns must cover all possible values of the input's type.
[typesfuns.rst, "Totality and Covering"](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/tutorial/typesfuns.rst#L235-L262)

> You can override this with a `partial` annotation: [...] However, this is not advisable, and in general you should only do this during the initial development of a function, or during debugging.
[same section, L252-L262](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/tutorial/typesfuns.rst#L252-L262)

> If a function is total, we can consider its type a precise description of what that function will do. [...] Idris makes this distinction so that it knows which functions are safe to evaluate while type checking [...] only total functions will be evaluated during type checking.
[typesfuns.rst, "Totality" L1382-L1410](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/tutorial/typesfuns.rst#L1382-L1410)

`%default` (paraphrase): sets the default totality requirement to `total`, `covering` or `partial`; initial value is `covering` unless `--total` is passed. [pragmas.rst L29-L34](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/reference/pragmas.rst#L29-L34)

Proofs beside code (paraphrase, from `theorems.rst`): equality is an ordinary type with one constructor `Refl`; "theorems about programs" are stated and proved as ordinary definitions (`twoPlusTwo : 2 + 2 = 4`), in the same files as the code. [theorems.rst L1-L40](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/tutorial/theorems.rst#L1-L40)

Dependent data (paraphrase): `Vect n a` carries its length in the type; `(++) : Vect n a -> Vect m a -> Vect (n + m) a`; a dependent pair `(n : Nat ** Vect n Int)` packs a value with an index when the index is not statically known. [typesfuns.rst L940-L960](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/tutorial/typesfuns.rst#L940-L960), [views.rst L1-L25](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/tutorial/views.rst#L1-L25)

Comments:
> Use comments to explain why code is written the way that it is.
[documenting.rst L9-L11](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/docs/source/reference/documenting.rst#L9-L11)

Contributing: new `partial` code in the libraries is accepted only where `total` is not possible, with documentation (paraphrase of [CONTRIBUTING.md L50-L53](https://github.com/idris-lang/Idris2/blob/89ba32eb5eb325909bacd0d5411076ac28d166bb/CONTRIBUTING.md#L50-L53); only the tail of the sentence was seen, **unverified** in full).

## Reasons given
- Totality: a total function's type is a trustworthy specification, and the checker needs totality to evaluate in types (quotes above).
- `partial` is for development and debugging because a partial function can fail at runtime.
- No reason given for the absence of a style guide beyond "we haven't been too prescriptive".

## What transfers to general-purpose Lean
- Lean's analogue of `%default total` is the default: definitions must terminate (`partial`/`unsafe`/`implemented_by` are the escape hatches). The Idris position, "`partial` only during development or where total is impossible, and document it", is a candidate rule for Lean's `partial`.
- Length-indexed vectors and dependent pairs show the "index in the type vs hide in a sigma" choice that Lean users meet with `Vector`, `Fin n` and subtypes.
- Proofs live in the same file and module as the definition; there is no separate-theorem-file convention.
- Nothing on naming, layout or tests.

## Caveats and unverified items
- Idris 2 docs track a moving master; the line numbers refer to the SHA above.
- The pragmatics of erasure/multiplicities (proof arguments at quantity 0) are in `multiplicities.rst`; not read.
