# Bundled vs unbundled structures and invariants (packed classes, type classes for mathematics, Mathlib, Lean Std `Raw`)

Combined note. Primary sources: Garillot et al. (MathComp packed classes), Spitters & van der Weegen, Mathlib source headers, and Lean core's `Std.DHashMap` docs.

| Field | Value |
|---|---|
| URL | (1) https://inria.hal.science/inria-00368403 (2) https://arxiv.org/abs/1102.1323 (3) https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Algebra/Group/Hom/Defs.lean (4) https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/Basic.lean |
| Author / org | (1) F. Garillot, G. Gonthier, A. Mahboubi, L. Rideau, TPHOLs 2009 (2) B. Spitters, E. van der Weegen, Mathematical Structures in Computer Science (arXiv 2011) (3) Mathlib contributors (4) Lean FRO / core contributors |
| Date / version | (1) 2009 (6-page HAL document seen; the TPHOLs paper is "Packaging mathematical structures") (2) arXiv 1102.1323, 2011 (3) mathlib4 `7bb03b4c...` 2026-10-17 (4) lean4 `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` |
| License | (1) HAL deposit ("Autorisation HAL", not an open licence); (2) arXiv non-exclusive distribution licence (arxiv.org/licenses/nonexclusive-distrib/1.0); (3) Apache-2.0 (Mathlib repo; per CONVENTIONS vendoring, not rechecked); (4) Apache-2.0 (lean4 repo; not rechecked) |
| Scope & audience | Library designers in Rocq/Lean |
| Kind | descriptive (papers); descriptive-with-recommendation (Lean docs: "When in doubt, prefer `DHashMap`") |
| Lean version | (1)(2) Coq; (3)(4) Lean 4 |
| Raw copy | `vendor/pages/proof-assistants/packaging.txt`, `spitters-vdw.txt`, `spitters-vdw-abs.md`; sources in `vendor/repos/mathlib4`, `vendor/repos/lean4` |

## Summary
Two senses of "bundling" occur. (a) Hierarchy design: whether an algebraic structure packs carrier, operations and laws into one record (bundled), keeps predicates over separate operations (unbundled), or something between (MathComp's packed classes; type-class-based unbundling). (b) Invariant design for data structures: whether the well-formedness proof is a field of the structure (bundled, so every value is valid) or a separate predicate (unbundled, so the type can be used where proofs cannot be carried). The first is mostly a mathematics-library concern; the second matters for application and library code in Lean, and Lean core documents its choice for hash maps.

## Claims
**Lean core: `Raw` + `WF`** (primary, descriptive and prescriptive):
> These hash maps contain a bundled well-formedness invariant, which means that they cannot be used in nested inductive types. For these use cases, `Std.DHashMap.Raw` and `Std.DHashMap.Raw.WF` unbundle the invariant from the hash map. When in doubt, prefer `DHashMap` over `DHashMap.Raw`.
([DHashMap/Basic.lean L61-L64](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/Basic.lean#L61-L64))

> maps with unbundled well-formedness invariant. This version is safe to use in nested inductive types. The well-formedness predicate is available as `Std.DHashMap.Raw.WF` and we prove in this file that all operations preserve well-formedness.
([DHashMap/Raw.lean L16-L22](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/Raw.lean#L16-L22))

> Dependent hash maps without a bundled well-formedness invariant, suitable for use in nested inductive types.
([RawDef.lean L31-L32](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/RawDef.lean#L31-L32))

So the documented rule of thumb: bundle by default; offer an unbundled `Raw` + `WF` variant only where a technical limitation (nested inductives) forces it, and say so in the doc comment. A further variant, `ExtDHashMap`, exists "for use in proofs because of extensionalities" ([Basic.lean](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/Basic.lean#L66-L67)). The same `Raw`/`WF` pattern was not grepped for in other Std types (**unverified** how widespread; `Std.HashMap`, `HashSet` follow the DHashMap one).

**Mathlib** (descriptive): homomorphisms are bundled structures ("This file defines the bundled structures for monoid and group homomorphisms"); "Historically this file also included definitions of unbundled homomorphism classes; they were deprecated and moved to `Deprecated/Group`" ([Hom/Defs.lean L13-L55](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Algebra/Group/Hom/Defs.lean#L13-L55)). Order homs: "a 'more bundled' version of the latter. We can't just drop the 'less bundled' version because the more bundled version usually does not work with dot notation" ([Order/Hom/Basic.lean L31-L33](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Order/Hom/Basic.lean#L31-L33)). Also "There is no `GroupHom` -- the idea is that `MonoidHom` is used" (Hom/Defs.lean L41-L45).

**Spitters & van der Weegen** (unbundled with type classes):
> Thus, bundled representations come at a substantial cost in flexibility. Historically, using bundled representations has nevertheless been an acceptable tradeoff, because (1) the unbundled alternative was such a pain, and (2) the standard algebraic hierarchy [...] is not all that wild.
([arXiv text, section 2](https://arxiv.org/abs/1102.1323))
They also give the costs of bundling: stacked records make projection paths "ever more unwieldy", and sharing makes them non-canonical. They decline to unbundle proofs themselves: "there is no point in sharing them" (same page). The paper's position: type classes make fully unbundled predicates practical.

**Garillot et al.** (packed classes): fully unbundling "allows for maximal flexibility" but "induces a proliferation of arguments that is rapidly overwhelming", so "related operations and axioms should be packed using Coq's dependent records (Σ-types); we call such records mixins"; nested packed structures are "telescopes"; their alternative, packed classes, "introduce an intermediate record that bundles all the mixins of a structure, but not the representation type; the latter is packed in a second stage" ([HAL text, §2-§3](https://inria.hal.science/inria-00368403)). Quotes checked against the PDF text extract (`packaging.txt` L109-L124, L254-L262). Their motivating cost: term size "grows as C^n" with C components and nesting depth n (C = 15, n = 3 for Cayley-Hamilton), "large enough to make theorem proving impractical".

## Reasons given
- Lean Std: nested inductives can't carry the invariant field; preferred default is bundled for safety ("When in doubt").
- Mathlib: bundled homs give coercion-to-function and dot notation; unbundled classes were deprecated.
- S&vdW: bundled costs flexibility (multiple structures on one carrier, long projection paths) which type classes recover.
- Garillot et al.: complete unbundling makes argument lists explode; packed classes give sharing and inheritance.

## What transfers to general-purpose Lean
- For application data structures the relevant model is Std's: a structure with the invariant bundled as a field (or subtype), plus an escape hatch when the invariant can't be carried, with the preference stated in the doc comment.
- Class hierarchy design (MathComp, S&vdW) is mathematics-library material; for general-purpose code the take-away is limited to "avoid argument proliferation; group laws with operations; use `class` for laws about operations, `structure` for data".
- Mathlib's `ₘ` suffix for "more bundled" variants is specific to its hom hierarchy.

## Caveats and unverified items
- The HAL document retrieved is 6 pages; it is the short version, check against the TPHOLs paper.
- No Lean-specific discussion of bundled-vs-unbundled for application code (Zulip, Lean 4 docs) was found or read. Lean Zulip threads on "Subtype vs structure with proof field" are an **unverified lead**.
- Licences for Mathlib/lean4 follow CONVENTIONS' vendored repos; not rechecked here.
