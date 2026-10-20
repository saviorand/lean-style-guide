# Lean quality indicators (sampled, LLM-judged)

| Field | Value |
|---|---|
| URL | https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md (fork with extra judge backends: https://github.com/kim-em/lean-quality-indicators) |
| Author / org | Remy Degenne (all upstream commits); the fork is by Kim Morrison |
| Date / version | upstream `be620058c99ff37c990a4f0fbe902e0c85221c86`, 2026-10-20 (repo created the same day, 3 commits); fork HEAD `6089dd3`, 2026-10-20 |
| License | none stated (default copyright): GitHub metadata `license: null` and no licence file in the tree at `be62005`, both checked 2026-10-20 |
| Scope & audience | Theorems in five Mathlib-based maths libraries; people assessing the quality of (AI-built) Lean libraries |
| Kind | descriptive |
| Lean version | Lean 4; the corpus uses toolchains v4.33.1 to v4.36.0-rc1 ([README L91-L94](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L91-L94)) |
| Raw copy | `vendor/pages/community/lean-quality-indicators-readme.md`, `-uh-prompt.md`, `-dup-prompt.md`, `-uh-report.md`, `-dup-report.md` |

## Summary
Not a style guide. It is an experiment that measures defect rates in Lean libraries instead of pattern frequencies. Each *indicator* is a written definition of one defect, given as a prompt to a model judge (`claude-opus-5-5`, effort `high`). The judge reads one uniformly sampled theorem with its context, can search the library, Mathlib and Lean core, and cannot run Lean. Two indicators exist: *unnecessary hypotheses* and *duplicates of Mathlib*. The corpus is Mathlib, Tau Ceti, Lean Pool, Anthropic's FLT formalization and Formal Frontier's 43 libraries; the README's title calls them "AI-built Lean libraries" ([README L1-L22](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L1-L22)). Results are reported with 95% intervals, and one indicator was rerun blind to measure agreement.

## Results
Unnecessary hypotheses, 1000 theorems per library ([README L24-L49](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L24-L49)):

| Library | Flagged | Rate (95% CI) |
|---|---:|---:|
| Mathlib | 31 | 3.1% (2.2–4.4%) |
| Formal Frontier | 34 | 3.4% (2.4–4.7%) |
| Tau Ceti | 68 | 6.8% (5.4–8.5%) |
| Lean Pool | 150 | 15.0% (12.9–17.3%) |
| FLT (Anthropic) | 203 | 20.3% (17.9–22.9%) |

A blind second run on the first 300 per library reproduces the rates "within 1.3 points per library (Cohen's κ = 0.92)".

Duplicates of Mathlib, 1000 theorems per library, Mathlib itself not judged ([README L51-L64](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L51-L64)): Formal Frontier 4.6%, Tau Ceti 5.0%, Lean Pool 6.8%, FLT 13.7%. Most findings are `special_case` (an instantiation of one Mathlib declaration), not exact duplicates. Re-derived findings, which prove the Mathlib result again instead of applying it, run from 1.6% (Tau Ceti) to 8.6% (FLT).

My count over `report.md` (approximate, by `awk`): of about 740 flagged hypotheses across all libraries, about 200 come from `variable` commands, and about 300 are instance-implicit binders.

## Rules (as indicator definitions)
Unnecessary hypothesis ([prompt L11](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/indicators/unnecessary-hypotheses/prompt.md#L11)):
> A hypothesis is *unnecessary* when the theorem stays true, and provable, after deleting that one argument while leaving the rest of the statement unchanged. The proof may have to change.

It counts more than unused arguments ([prompt L13-L18](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/indicators/unnecessary-hypotheses/prompt.md#L13-L18)):
> a hypothesis implied by the other hypotheses (`0 ≤ x` next to `0 < x`; `[Nonempty α]` next to `[Inhabited α]`; [...] an instance the theorem takes twice, once from `variable` and once as its own binder);

On `variable` ([prompt L9](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/indicators/unnecessary-hypotheses/prompt.md#L9)):
> Instance-implicit variables are therefore a frequent source of hypotheses that the theorem takes without needing them.

Weakening a hypothesis or generalizing the theorem is excluded: "Only deleting an argument counts" ([prompt L20-L24](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/indicators/unnecessary-hypotheses/prompt.md#L20-L24)).

Duplicate of Mathlib: `duplicate` is the same statement up to presentation; `special_case` follows from one Mathlib declaration in "one or two short lines of Lean" of routine glue ([prompt L9-L15](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/indicators/duplicates-mathlib/prompt.md#L9-L15)). The search procedure relies on Mathlib's naming conventions ([prompt L30](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/indicators/duplicates-mathlib/prompt.md#L30)):
> **Guess the names.** Write down the names Mathlib's naming conventions would give this statement [...] and grep for `theorem <name>` and `lemma <name>`.

## Reasons given
None. The README does not argue why either defect matters; it only measures them.

## What transfers to general-purpose Lean
- **As evidence for [Q0c](../open-questions.md#scope-and-method).** This is a worked method for measuring quality rather than frequency: a precise defect definition, a uniform sample, confidence intervals and a test-retest check. It separates a curated library (Mathlib 3.1%) from others (FLT 20.3%). The per-flag reports are bad examples, each with a reason. For program code, someone would first have to define an indicator; the repo has none for programs.
- **Unnecessary hypotheses.** The syntactic case is already covered by Batteries' `unusedArguments` linter ([mathlib-linters](mathlib-linters.md)). New here: implied hypotheses, and instance arguments pulled in by `variable`, which accounted for about a quarter of flags by my count. Relevant to Mario Carneiro's remark that heavy `variable` use is a maths habit a general guide can omit ([zulip-style-misc](zulip-style-misc.md)).
- **Duplicates.** Restates lean4's `AGENTS.md` principle "Lean on Lean [...] avoiding reinventions" ([lean-core-contributing](lean-core-contributing.md)). The search procedure (step 2 above) works only because names are guessable, which supports the guessable-names principle in [proposed-toc.md](../proposed-toc.md).
- **Does not transfer.** Junk values (`x / 0 = 0`, `Real.log 0 = 0`), typeclass hierarchies (`NormedSpace` next to `InnerProductSpace`), and everything about Mathlib as the reference library.

## Caveats and unverified items
- **Very new and moving.** Created 2026-10-20; the unnecessary-hypotheses results went from 400 to 1000 theorems per library within hours. Cite by commit.
- **Model verdicts, lightly checked.** Unnecessary-hypotheses flags were "checked by hand only on a handful of flags (all correct), not by compiling the proposed changes in Lean; two runs of the same model can share blind spots" ([README L47-L49](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L47-L49)). An adversarial verifier "confirmed all 235 claims, so it does not discriminate" ([README L215-L217](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L215-L217)). Duplicates are "not yet audited beyond a 40-theorem test, and not yet test-retested" ([README L64](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L64)).
- **Populations differ.** `private` and deprecated declarations are skipped; sampling is uniform per library, so large projects dominate; about 93% of FLT's population is helper lemmas of its `P2M/Sol` proofs ([README L230-L262](https://github.com/RemyDegenne/lean-quality-indicators/blob/be620058c99ff37c990a4f0fbe902e0c85221c86/README.md#L230-L262)).
- **"AI-built" unverified.** The README does not say which libraries were written by AI, or how much of each.
- **Fork.** `kim-em/lean-quality-indicators` adds a Codex backend and a benchmark of `gpt-6.1-sol`, `gpt-6-luna` and `claude-sonnet-5-5` on the first 300 theorems per library. At `6089dd3` it was 6 commits ahead and 1 behind upstream, still showed the 400-theorem results, and had published throughput measurements only, no verdicts.
- **My counts** of `variable` and instance-implicit flags are an `awk` pass over `report.md`, not checked by hand.
