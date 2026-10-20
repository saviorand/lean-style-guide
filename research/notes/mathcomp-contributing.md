# Mathematical Components: CONTRIBUTING.md (proof style, naming, Hierarchy Builder)

| Field | Value |
|---|---|
| URL | https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md |
| Author / org | Mathematical Components team |
| Date / version | file last changed in `ee3f6537025659273aac286b1077f219d63fc054` (2026-06-26) |
| License | CeCILL-B (`LICENCE`, "CeCILL-B FREE SOFTWARE LICENSE AGREEMENT"; `vendor/pages/proof-assistants/mc-LICENSE`). GitHub reports NOASSERTION. |
| Scope & audience | MathComp contributors (Rocq/Coq, SSReflect) |
| Kind | normative |
| Lean version | n/a (Rocq) |
| Raw copy | `vendor/pages/proof-assistants/mathcomp-contributing.md` |

## Summary
A guide for a mathematics library written with small-scale reflection. It covers proof-script layout, a detailed lemma-naming grammar (`mainSymbol_suffixes` with optional conditions), naming of structures and interfaces, and how to declare algebraic structures with Hierarchy Builder (the successor to hand-written "packed classes"). The bundled-vs-unbundled design itself is explained in the Garillot et al. paper (see `bundled-unbundled.md`), not here.

## Rules
Proofs in blocks:
> One important guideline is to structure proofs in blocks, i.e., forward steps, to limit the scope of errors.
([General guidelines](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L14-L16))

Terminators:
> Lines that close a goal must start with a terminator (`by` or `exact`).
([L24-L26](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L24-L26))

Chains of optional rewrites:
> Chaining too many optional rewrites makes error detection hard.
([L28-L31](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L28-L31))

New theories:
> Adding new theories with in particular with new datatypes and definitions should be discussed in mathcomp meetings.
([L33-L35](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L33-L35))

Lemma names:
> Names in the library usually obey one of the following conventions: `(condition_)?mainSymbol_suffixes` / `mainSymbol_suffixes(_condition)?`
([Naming conventions for lemmas](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L105-L110))

> `mainSymbol` is the most meaningful part of the lemma. It generally is the head symbol of the left-hand side of an equation or the head symbol of a theorem.
([L117-L118](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L117-L118))

Structures and interfaces (paraphrase): types of structures are `lowerCamelType` (e.g. `unitRingType`); Hierarchy Builder structures are UpperCamel (`UnitRing`); interfaces/mixins at the bottom of a hierarchy start with `is` or `has` (`hasChoice`, `isZsemimodule`); factories extending `A` into `B` via `C` are `A_C_isB` ([Naming conventions for definitions](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L187-L207)).

Deprecation (paraphrase): breaking changes go through a deprecation attribute (`#[deprecated(since="mathcomp x.x.x", use=foo_new)]`) ([L216-L248](https://github.com/math-comp/math-comp/blob/ee3f6537025659273aac286b1077f219d63fc054/CONTRIBUTING.md#L216-L248)).

## Reasons given
Only the block-structure rule (limit error scope), the optional-rewrite rule (error detection), and "make the suffixes readable" for the underscore rule are justified. Others carry no reason.

## What transfers to general-purpose Lean
- The grammar approach (head symbol first, then conditions and suffixes) parallels Lean's `naming.md`; useful as a contrast, not a model.
- "Discuss new datatypes before adding them" is a governance rule for shared libraries; may suit a community library guide.
- Block-structured, terminator-marked proofs correspond to Lean's "every goal closed by a terminal tactic" style; Lean core's `style.md` already covers tactic proofs.
- The mixin/factory/`is`/`has` naming is Hierarchy Builder specific.

## Caveats and unverified items
- Line ranges are approximate to ±2 lines (taken from a local copy of the master file, not the SHA above; the SHA is the last commit that touched the file).
- Parts of the file (indentation of scripts, Hierarchy Builder instantiation) were skimmed only by heading.
