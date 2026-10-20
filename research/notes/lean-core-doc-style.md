# Lean Documentation Style Guide (`doc/style.md`), docstring sections

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md |
| Author / org | Lean FRO (project-attributed; no named author) |
| Date / version | commit `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` (2026-10-17) |
| License | Apache 2.0 (lean4 `LICENSE`) |
| Scope & audience | "all documentation that's officially provided by the project": docstrings, reference manual, dev guide, examples. Explicitly not for texts with a named author |
| Kind | normative (for official docs) |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/lean-official/lean-core-doc-style.md` |

## Summary
A 1250-line prose and API-documentation style guide, found beyond the three `doc/std/` files. Part 1 (lines 45-485) is general writing guidance (US English, Chicago Manual of Style, passive voice, contractions, Unicode, examples). Part 2 (lines 486-1250) is "API Reference Documentation (Docstrings)": goals, general conventions, layout, per-kind structure (theorems, predicates, constants, inductive types, structures, classes, syntax, tactics). It applies to all officially provided docstrings, not only the stdlib, but it is oriented to API docs for hover/doc-gen/reference manual. Only the docstring parts were read closely.

## Rules
Link base `https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md`.

Audience ([L1-L40](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L1)):
> Individuals writing texts where they are named as the author do not need to follow all of these guidelines.

Docstring goals ([L496](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L496)):
> Docstrings are primarily viewed in editor hovers, as part of search results in tools like `doc-gen` or Loogle, and in the reference manual (in this order of importance). [...] They are not primarily viewed in the context of the source module in which they are defined, but they are always viewed together with the corresponding signature.

> **Lean should be self-contained.** Avoid linking to sources outside of the Lean repository or the reference manual.

> **Use structured documentation information**. Use attributes like `tactic_alias` and commands like `recommended_spelling` instead of ad-hoc text.

Non-goal ([L547](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L547)):
> Docstrings do not exist to document the details or internals of the implementation for other developers. This purpose should be served by ordinary comments.

General conventions ([L553](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L553)):
> Docstrings should not refer to the surrounding context of the module in which they're defined.
> Docstrings may assume that parameter names in the corresponding signature are in scope. They may be referred to by name.
> Docstrings should not assume that the body of the definition, the constructors of the inductive type, or the fields of the structure are visible.
> Prefer independently-useful documentation over cross-referencing when inheritance doesn't make sense.
> There's no need to say what kind of declaration is being documented in the docstring.

Layout ([L585](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L585)):
> The `/--` should be at the same column as the start of the declaration or constructor being documented.
> If the docstring fits within the line length limit, it may be on one line [...]. Don't use a one-sentence-per-line or a one-grammatical-clause-per-line formatting.
> Use exactly one blank line between paragraphs.

Constants ([L803](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L803)): structure is "Short summary, Details, Examples". Summary:
> 1–3 sentences (ideally 1) [...] The first (or only) sentence of the short summary should be a *sentence fragment* in which the subject is implied to be the documented item, written in present tense indicative, or a *noun phrase*.

Examples are either a bulleted list of equalities in inline code after `Examples:` (or `Example:`), or alternating `example`/`output` code blocks (compared as with `#guard_msgs`; "though this isn't yet automatically checked").

Structures ([L952](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L952)): "fields should be described according to what they contain, rather than as functions that retrieve the contents."
Classes ([L1023](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L1023)): the docstring must be "clearly connected to any notation that the class overloads and that it uses accessible language."

Inline code ([L328](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L328)): treat identifiers "as if they were words. Do not change their capitalization."

Reference manual links: `lean-manual://section/TAG` URL scheme ([L602](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L602)).

Note the conflict with `style.md` (stdlib): that file says docs use "the indicative mood"; this guide says first sentence is a present-tense fragment or noun phrase. Compatible in practice, not identical wording.

## Reasons given
- Consistency across hover, doc-gen and manual contexts; accessibility to people new to Lean; self-containedness; "Conventions should facilitate an automated migration from Markdown to Verso" (goals, L496-L545).
- On arbitrariness: "Many of these guidelines are essentially arbitrary [...] it's more important to *have* a broadly acceptable standard" ([L45-L60](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/style.md#L45)).

## What transfers to general-purpose Lean
- Highest-value official source for docstrings: summary-first structure, hover-oriented writing, parameters referable by name, no module-relative references, Examples format.
- Library authors outside FRO could adopt it as is for API docs; the `lean-manual://` links and `recommended_spelling` commands are optional.
- Parts oriented to a mathematical audience (theorem names, classical perspective) do not transfer.

## Caveats and unverified items
- Lines 45-485 and 626-1250 were only skimmed via headings; examples and per-kind rules for theorems/predicates/syntax/tactics not recorded in detail.
- Docstring line-length limit is referenced but not given in the text read (**unverified**).
