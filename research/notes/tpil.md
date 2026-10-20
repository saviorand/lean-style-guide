# Theorem Proving in Lean 4

| Field | Value |
|---|---|
| URL | https://lean-lang.org/theorem_proving_in_lean4/ (source: https://github.com/leanprover/theorem_proving_in_lean4/tree/4e28129fdd58037f8f5857548d5e99fe4fb0cc57) |
| Author / org | Jeremy Avigad, Leonardo de Moura, Soonho Kong, Sebastian Ullrich, with contributions from the Lean community (repo `README.md`) |
| Date / version | Repo commit `4e28129fdd58037f8f5857548d5e99fe4fb0cc57` (2026-08-14); `book/lean-toolchain` = v4.34.0-rc1 |
| License | Apache 2.0 (repo `LICENSE`) |
| Scope & audience | People learning to prove theorems in Lean; dependent type theory, tactics, Lean-specific interactive features |
| Kind | descriptive (textbook) |
| Lean version | Lean 4 |
| Raw copy | source clone `vendor/repos/theorem_proving_in_lean4` (not copied to pages) |

## Summary
TPIL is a language tutorial, not a style guide, and it is oriented to proofs. Grepping "convention", "idiomatic", "recommend", "style" across `book/TPiL/*.lean` (16,577 lines) finds no program-style rules. Only "tactic-style vs term-style" proof discussion and a couple of "we recommend" remarks about tooling. Chapters of relevance to program structure: Variables and Sections and Namespaces ([DependentTypeTheory.lean L788, L871](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/DependentTypeTheory.lean#L788)), More on Sections/Namespaces/Attributes ([InteractingWithLean.lean L133, L178, L314](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/InteractingWithLean.lean#L133)), Structures and Records, Type Classes (output parameters, default instances, local/scoped instances), Induction and Recursion (structural, well-founded).

## Rules
Nearly none. Items worth recording (all in `https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/`):

- Structures: "The structure command is essentially a 'front end' for defining inductive data types." ([StructuresAndRecords.lean L40](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/StructuresAndRecords.lean#L40))
- Sections: the `variable` command is for declaring variables "that are inserted as arguments to theorems and definitions, as necessary" ([InteractingWithLean.lean L138-L144](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/InteractingWithLean.lean#L138)). Descriptive: variables are included only if mentioned (paraphrase).
- Namespaces: `protected` prevents the short alias from being created ([InteractingWithLean.lean L252](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/InteractingWithLean.lean#L252)); recursors like `Prod.rec` are protected.
- Type classes: output parameters (`outParam`), `@[default_instance]`, local and scoped instances, `inferInstance` are explained (TypeClasses.lean L440-L805, L1002). Single recommendation, about temporarily disabling an instance with `attribute [-instance]` (paraphrase of the context at L705-L733): "We recommend you only use this command to diagnose problems." ([TypeClasses.lean L733](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/TypeClasses.lean#L733)); the exact command referred to is **unverified**.
- Proof styles: "tactic-style proofs can be harder to read" but support incremental development ([Tactics.lean L18-L25](https://github.com/leanprover/theorem_proving_in_lean4/blob/4e28129fdd58037f8f5857548d5e99fe4fb0cc57/book/TPiL/Tactics.lean#L18)).
- Recursion: structural recursion is handled by the compiler; well-founded recursion with `termination_by` covered in L763-L1165; no advice on choosing between them (see the FRO blog post in `fro-blog` for that).
- Programs: no `partial`, `IO`, `do`, Array vs List, error-handling or testing content (grep for `partial` in `InductionAndRecursion.lean` returns nothing relevant; `#eval` appears as a calculator in `DependentTypeTheory.lean` L61-L78).

## Reasons given
Not applicable; the book explains mechanics, not conventions.

## What transfers to general-purpose Lean
- Useful as the reference description of how `namespace`/`section`/`variable`/`open`/`export`/`protected`/instances behave; any guide rule about them can cite it for semantics.
- No style content to import. Its proof-centric framing (theorem names like `Nat.add_comm`, tactic blocks) is not about programs.

## Caveats and unverified items
- Only headings, grep hits and a few sections were read; not the whole book.
- The online book may differ from this repo commit.
