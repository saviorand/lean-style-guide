# leanfmt (duckki): a community formatter and its style rules

| Field | Value |
|---|---|
| URL | https://github.com/duckki/leanfmt (design doc: `docs/design.md`); announcement https://duckki.github.io/2026/08/11/introducing-leanfmt.html (not fetched) |
| Author / org | Duckki Oe (individual) |
| Date / version | commit `65d69c8dc2dfd0aa69fd4132d48f38b7af9a57ef`, 2026-09-18; `docs/design.md` last changed in `6083ef70c691e1de3620239b11a0d09ea91c82a6`; tag v0.3.5 quoted in the Zulip thread of 2026-08-19 |
| License | MIT (LICENSE file: "Copyright (c) 2026 Duckki Oe") |
| Scope & audience | Lean programmers/projects wanting an automated format; "Core, Std, and Mathlib syntax are first-class support targets" |
| Kind | community advice (a tool whose behaviour encodes a style) |
| Lean version | Lean 4 (current toolchain) |
| Raw copy | `vendor/pages/community/community-duckki-leanfmt-readme.md`, `community-duckki-leanfmt-design.md` (2396 lines; skimmed headings and the first 130 lines) |

## Summary
A conservative formatter written in Lean that keeps tokens and comments, formats only whitespace and line breaks, leaves proofs largely untouched, and refuses to write if its idempotence/preservation checks fail. Its 2400-line design document is effectively an unofficial layout style guide for programs and statements (declaration headers, `where`, `match`, `let`, `if`, applications, structures). It states a deliberate departure from "Lean community guidance" on operator placement.

## Rules (as implemented by the tool)
> leanfmt uses a 90-character default line limit and two-space indentation. The line limit is configurable for projects with a different convention. ([Design philosophy](https://github.com/duckki/leanfmt/blob/6083ef70c691e1de3620239b11a0d09ea91c82a6/docs/design.md))

> leanfmt generally breaks before operators for this reason [a leading operator marks continuation without adding a nesting level]. Bodies after `:=`, `=>`, `with`, quantifier commas, and similar separators are indented instead. (Design, "Make continuation structure visible")

> Formatting changes whitespace only. Token text and token order remain the same.

> Proofs receive an even more conservative treatment. Proof subtrees are retained from their original source ...

> `where` returns to the declaration's base column. (Design, `where` blocks)

Its examples use `fun n =>` (design.md lines ~265 and ~334); it does not rewrite `=>` to `↦`.

## Reasons given
Visible structure: "Indentation shows block structure ... a leading operator indicates continuation". The Zulip post: his "preference is slightly different from Lean community guidance" ([Zulip, 2026-07-21](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Formatter.20for.20Lean.204.html)). Safety reasons for conservative design are stated in the README ("trust as much as style").

## What transfers to general-purpose Lean
- A concrete, tool-checked layout for programs that a guide can compare against: 90 columns (Mathlib: 100), leading operators (Mathlib: trailing), 2-space indent.
- Shows which layout questions a formatter forces a decision on (applications, `match` arms, `let` chains, `if`), many of which Mathlib's guide does not address.
- It is not endorsed by Lean core; the official FRO formatter may differ (`notes/zulip-formatter.md`).

## Caveats and unverified items
- Only a fraction of design.md was read; rules above come from the first 130 lines and grep hits.
- Claimed validation over all of Mathlib is the author's statement (Zulip 2026-08-19), unverified.
- Sibling `toku-sa-n/leanfmt` (README only: usage, `--check`, `--in-place`, Apache-2.0 claimed) has no style document; not given its own note.
