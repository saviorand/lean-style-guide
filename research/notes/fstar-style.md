# F* style guide (wiki "Style-guide")

| Field | Value |
|---|---|
| URL | https://github.com/FStarLang/FStar/wiki/Style-guide (raw: https://raw.githubusercontent.com/wiki/FStarLang/FStar/Style-guide.md) |
| Author / org | F* team (Microsoft Research / Inria contributors; inline initials such as "JP:") |
| Date / version | wiki page undated; fetched 2026-10-17; no revision recorded |
| License | Wiki: none stated on the page. Main repo: Apache-2.0 (`LICENSE`, GitHub API). The wiki is a separate repo, so the repo licence is not asserted for it. |
| Scope & audience | F* contributors and library authors |
| Kind | normative ("partial, evolving guide"); referenced from [CONTRIBUTING.md](https://github.com/FStarLang/FStar/blob/master/CONTRIBUTING.md) L38-L39: "contributions should adhere to the following style guide" |
| Lean version | n/a (F*) |
| Raw copy | `vendor/pages/proof-assistants/fstar-style.md`, `fstar-contrib.md` |

## Summary
F* does have a style guide, a wiki page, described as "a partial, evolving guide recommending various syntactic conventions". It covers modular structure (interface files, abbreviations over opens), naming (underscore identifiers, descriptive names, lemma names that describe the specification), annotating all top-level terms with types, and formatting pre/postconditions and logical formulae.

## Rules
> Modules should have separate interface files, i.e., `CamelCase.fsti`
> Module abbreviations are preferred over opened modules and namespaces, with well-chosen exceptions
> Groups of related modules should be composed into a single module using `include` for easier use by clients
([Modular structure](https://github.com/FStarLang/FStar/wiki/Style-guide))

Naming:
> Use descriptive, multi-character names for top-level names, especially those exported by a module. (i.e., contrary to OCaml style, prefer giving names like `PartialMap.partial_map` rather than `PartialMap.t`
> Redefining commonly used operators with different semantics is a bad idea. We should avoid doing this.
> Sometimes, the name of a definition may reflect its type, e.g., `Seq.seq_of_list`. More often, the name of a definition should provide some more descriptive name, reflecting the most meaningful part of its specification paraphrased in English. [...] Note, although many lemmas in the library have names that include the fragment `lemma_`, this style is not preferred.
(Naming conventions within a module; the middle part of the last quote was truncated in my read, **unverified**)

Types:
> Annotate all top-level terms with their full types.
> Unless required by needs of an interface, prefer the first style (i.e, use only an annotated `let` rather than `let` + `val`).
([Formatting type annotations](https://github.com/FStarLang/FStar/wiki/Style-guide))

Formulae:
> For numeric ranges, prefer semi-open intervals (closed lower bound, open upper bound)
> Prefer one conjunct per line [...] think of `/\` as a line delimiter
([Formatting logical formulae](https://github.com/FStarLang/FStar/wiki/Style-guide))

## Reasons given
Mostly none. Underscore names are justified as "more compatible with our existing conventions" and "better with abbreviations" (`use_SMT_pat`).

## What transfers to general-purpose Lean
- "Annotate all top-level definitions with full types" aligns with Lean's habit of explicit signatures for public definitions.
- "Separate interface (.fsti) and implementation" has no Lean counterpart; the closest are `private`/`@[irreducible]` and structure-hiding patterns (see `bundled-unbundled.md`).
- "Semi-open ranges" and "name lemmas for what they say" are language-agnostic.
- The guide has no section on when to prove; the library mixes SMT-discharged refinements and explicit lemmas.

## Caveats and unverified items
- Wiki history not inspected; the "JP:" and "partial" markers show it is unfinished.
