# Iris proof style guide (docs/style_guide.md)

| Field | Value |
|---|---|
| URL | https://gitlab.mpi-sws.org/iris/iris/-/blob/master/docs/style_guide.md |
| Author / org | Iris project (MPI-SWS) |
| Date / version | fetched 2026-10-17 from `master`; commit SHA not recorded (**unverified**) |
| License | CC-BY 4.0 for `docs/` (this file), BSD for source: "the documentation (i.e., everything inside the docs/ and tex/ folders) is licensed under the terms of the CC-BY 4.0 license" ([LICENSE](https://gitlab.mpi-sws.org/iris/iris/-/raw/master/LICENSE), fetched 2026-10-17) |
| Scope & audience | Iris and std++ contributors (Rocq) |
| Kind | normative (self-described as "still in development and rather incomplete") |
| Lean version | n/a (Rocq) |
| Raw copy | `vendor/pages/proof-assistants/iris-style.md` |

## Summary
A short, unfinished guide mixing proof-script syntax rules with library conventions. For a general Lean guide only the "Naming" and "Parameter order and implicitness for lemmas" sections are of interest; the rest is Rocq/Ltac syntax. It has no guidance on data modelling, invariants or when to prove.

## Rules
Implicit arguments:
> In new lemmas, arguments should be marked as implicit when they can be inferred by unification in all intended usage scenarios. (If an argument can *sometimes* be inferred, we do not have a clear guideline yet -- consider on a case-by-case basis, for now.)
([Parameter order and implicitness](https://gitlab.mpi-sws.org/iris/iris/-/blob/master/docs/style_guide.md))

Parameter order:
> Parameter order is usually from more higher-order to less higher-order (types, functions, plain values), and otherwise follows the order in which variables appear in the lemma statement.
(same section)

Naming (selected, quoted from the "Naming" section):
> If you have lemma `foo` which is an iff and you want single direction versions, name them `foo_1` (forward) and `foo_2` (backward)
> Operations that "extract" from the data structure (`lookup`, `elem_of`, ...) should come before operations that "alter" the data structure (`filter`, `insert`, `union`, `fmap`). For example, use `map_lookup_filter` instead of `map_filter_lookup`.
> Suffix `'` (prime) is used when `foo'` is a corollary of `foo`. Try to avoid these since the name doesn't convey how `foo'` is related to `foo`.
> Lower-case theorem names, lower-case types, upper-case constructors
> For lemmas `f x = g ...` that give a definition of function `f` in terms of `g`, we use `f_as_g`.

Proof layout:
> Put proofs either all on one line (`Proof. reflexivity. Qed.`) or split up the usual way with indentation.
(Uncategorized/Proof section)

Lemma statements:
> Put the entire theorem statement on one line or one premise per line, indented by 2 spaces.

## Reasons given
Mostly none. The prime-suffix rule gives its own reason; the `first [ ... | fail ... ]` rule links an issue.

## What transfers to general-purpose Lean
- "Extract before alter" ordering and avoiding primes as corollary markers are language-agnostic naming ideas; compare Lean's naming doc.
- "Implicit when inferable in all intended uses; otherwise case by case" matches the agda-stdlib rule almost word for word and admits the question is open.
- Everything else is Rocq/Ltac syntax and Iris logic specific.

## Caveats and unverified items
- Document admits TODOs and an internal disagreement (a reviewer remark on match indentation is left inline).
- No commit SHA recorded. Licence read from the repo `LICENSE`; `LICENSE-DOCS` itself not opened.
