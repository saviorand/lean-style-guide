# lean-lang.org/learn (official learning resources page)

| Field | Value |
|---|---|
| URL | https://lean-lang.org/learn/ |
| Author / org | Lean FRO / Lean project (website) |
| Date / version | Undated; fetched 2026-10-17 with defuddle |
| License | none stated on the fetched text (page footer not captured; **unverified**) |
| Scope & audience | Newcomers: programmers, mathematicians, students |
| Kind | descriptive (index of resources) |
| Lean version | Lean 4 (Lean 3 is mentioned only in the citation section) |
| Raw copy | `vendor/pages/lean-official/lean-learn-page.md` |

## Summary
The page is a catalogue of resources in sections: Core documentation, Further reading, Interactive Games and Tutorials, Tools, Resources, and How to cite. It does not itself give any style advice. The programming-relevant resources are FPIL and the Language Reference; there is no link to the stdlib style guide, naming conventions, or the documentation style guide. It describes Lean as "built for formalizing math and for formal verification, but is flexible enough for general coding", i.e. programming is positioned as secondary to mathematics.

## Resources listed (as on the page)
Author and date are not on the page; author/date given only where the page says so, otherwise **unverified**.

| Resource | URL | What the page says | Program style content? |
|---|---|---|---|
| Functional Programming in Lean (FPIL) | https://lean-lang.org/functional_programming_in_lean/ | "the main resource for programmers who want to learn Lean" | Yes, implicit and a few explicit conventions: see `fpil` |
| Theorem Proving in Lean (TPIL) | https://lean-lang.org/theorem_proving_in_lean4/ | proofs, dependent type theory, automation | Minimal: see `tpil` |
| Mathematics in Lean (MIL) | https://leanprover-community.github.io/mathematics_in_lean/ | for mathematicians, Mathlib | No (math, community-hosted; not fetched) |
| Lean Language Reference | https://lean-lang.org/doc/reference/latest/ | "comprehensive, precise description of Lean" | Semantics and a few conventions: see `lean-reference` |
| Lean FAQ | https://lean-lang.org/faq | common questions | not fetched |
| Mathlib API Reference | https://leanprover-community.github.io/mathlib4_docs/ | docs for core, std, Mathlib | API docs only |
| Hitchhiker's Guide to Logical Verification | https://github.com/lean-forward/logical_verification_2025 | course text, VU Amsterdam | Not fetched; verification course |
| Logic and Proof | https://leanprover-community.github.io/logic_and_proof/ | classical logic textbook | No |
| The Mechanics of Proof | https://hrmacbeth.github.io/math2001/ | Math2001, Fordham | No |
| Founder's Blog | https://leodemoura.github.io/blog/ | essays by Chief Architect Leo de Moura | Not fetched; may contain design essays (lead) |
| Natural Number Game, Lean Game Server | adam.math.hhu.de | games | No |
| VS Code extension manual; Semantic Highlighting; LaTeX | various | tooling | No |
| Loogle, LeanExplore, LeanSearch, LeanDojo, REPL, Pantograph, Lean4Web, Verso | various | tooling | No (Verso: see `verso-docs`) |

Cite: "The Lean 4 Theorem Prover and Programming Language" (de Moura and Ullrich, CADE-28, 2021) is the paper cited for Lean 4; it is a system description, not style guidance (not read here).

## Reasons given
Not applicable.

## What transfers to general-purpose Lean
- Shows the official reading path for a programmer: FPIL then the Reference. A guide aimed at programmers has no official sibling document for "how should program code look"; the closest are in `lean-core-style` and `lean-core-naming`, which are not linked from this page.

## Caveats and unverified items
- Page has no date; resource authors and dates are not on it. Authors of MIL, Logic and Proof, etc. were not verified.
- Linked resources other than those with their own notes were not opened.
