# Zulip: the Lean formatter (official and community)

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/archive/ (threads cited individually below) |
| Author / org | Lean Zulip participants (public archive) |
| Date / version | Threads 2020-09-09 to 2026-07-21. Archive repo [`leanprover-community/archive`](https://github.com/leanprover-community/archive) cloned at `63dc76b4eb239e7814eb5e0cb421cb731b507301` (2026-10-02) to `vendor/repos/zulip-archive/zulip_json` and grepped locally |
| License | none stated for the archive repo (no LICENSE in clone; `gh repo view` reports none); messages remain the authors' |
| Scope & audience | Everyone; mostly Mathlib/Lean-core community |
| Kind | descriptive (discussion) |
| Lean version | Lean 3 for the 2020 thread (flagged), Lean 4 otherwise |
| Raw copy | clone at `vendor/repos/zulip-archive` (JSON per topic); roadmap page `vendor/pages/community/fro-roadmap-y3.md`; leanfmt READMEs `vendor/pages/community/community-*leanfmt*` |

## Summary
There is no released official Lean formatter as of the newest messages (2026-07). The Lean FRO's Year 3 roadmap lists one, community members say it is being built "in private" by a single FRO developer, and in the meantime at least three community formatters exist. The 2020-2024 threads show the same argument repeatedly: Lean's extensible syntax makes a formatter hard, the built-in pretty printer is not safe on arbitrary source, and Mathlib's hand-formatted style makes an auto-formatter's output contentious.

## Threads
Status of an official formatter
- [Autoformatter: what to expect? (lean4, 2026-03-26)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Autoformatter.3A.20what.20to.20expect.3F.html): Thomas Murrills asks how opinionated "the upcoming formatter" will be, what it will stay silent on, whether it is extensible and how linters will interact. No answers recorded in the archive (1 message).
- [Formatter (computer-science, 2026-06-19)](https://leanprover-community.github.io/archive/stream/516743-computer-science/topic/Formatter.html): Julia Markus Himmel: "The Lean FRO is currently working on an official code formatter that will be part of the Lean distribution, as noted in the roadmap ... it will be necessary to annotate much of the syntax that is added by Batteries and mathlib (and all other projects of course) with formatting rules."
- [Formatter for Lean 4 (lean4, 2026-06-16)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Formatter.20for.20Lean.204.html): Zhi Han notes existing repos do not implement the recommended style (`lean4/doc/std/style.md`); Patrick Massot: "Not yet, but it's coming."
- [Built-in Lean formatter (Editors & UIs, 2026-02-24 to 2026-07-09)](https://leanprover-community.github.io/archive/stream/561906-Editors-&-UIs/topic/Built-in.20Lean.20formatter.html): Willem vanhulle ships a fork of lean4 with a built-in formatter (uses Lean's term pretty printer); Patrick Massot on 2026-02-26: "the Lean FRO is very actively working on writing a Lean code formatter"; on 2026-07-07: "Still making progress but not released yet." Henrik Böving confirms (2026-07-09) it is a Lean FRO project. The thread then turns to whether private development is acceptable (Julia Markus Himmel: "Open source does not imply being developed in the open").
- Roadmap source: [FRO Year 3 roadmap](https://lean-lang.org/fro/roadmap/y3/): goal 6 "Close the usability gap: formatter, clearer error messages, IDE polish"; "A fully integrated code formatter will be available within the VS Code extension". (Saved: `vendor/pages/community/fro-roadmap-y3.md`.)

Why it is hard (older threads)
- [autoformatter for lean (general, 2020-09-09 / 2021-10-03)](https://leanprover-community.github.io/archive/stream/113488-general/topic/autoformatter.20for.20lean.html): Lean 3 context at the start. Johan Commelin: "it might be really hard to do this for Lean 4, because its syntax is extremely flexible." Sebastian Ullrich (2021-10-03): "Formatting code with sensible line breaks is an art and someone would likely need to spend a month or so solely on the Lean 4 formatter to achieve remotely acceptable output".
- [Code Formatter (Is there code for X?, 2023-08-28)](https://leanprover-community.github.io/archive/stream/217875-Is-there-code-for-X%3F/topic/Code.20Formatter.html): Kyle Miller: Lean 4 ships a reformatter that parses and pretty-prints a file, "mainly a demonstration"; Mario Carneiro: "95% there but the remaining 5% is way too high an error margin ... should not be used on any code you really care about." Bolton Bailey and Floris van Doorn list wanted features (wrapping, colons at line end, shortening names via open namespaces).
- [formatter (lean4, 2024-09-17)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/formatter.html): Mario Carneiro: "The hard part of writing a formatter is making something that doesn't destroy code which has already been manually formatted (in a style approved way), like mathlib". Henrik Böving: in Go "everyone just accepts the formatting". Eric Wieser shows `ppTerm` output that is illegal syntax.
- [Code style/formatting (lean4, 2022-07-18 and 2024-11-10)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Code.20style.2Fformatting.html): Damiano Testa: `linter.ppRoundtrip` "tries to approximate this ... filled with false positives and negatives".
- [Mathlib-style formatter (mathlib4, 2024-12-11)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Mathlib-style.20formatter.html): Eric Wieser: "Currently the best 'tool' is creating a PR and letting the reviewers advise on style."
- [opinionated formatter a la black (2022-02-08)](https://leanprover-community.github.io/archive/stream/217875-Is-there-code-for-X%3F/topic/opinionated.20formatter.20.C3.A0.20la.20black.html): Patrick Massot: formatter "will exist in Lean 4, but there is no point trying in Lean 3" (Lean 3 context).
- Tracking issue: mathlib4 [#7217 Linter / Formatter Wishlist](https://leanprover-community.github.io/archive/stream/263328-triage/topic/issue.20!4.237217.3A.20Linter.20.2F.20Formatter.20Wishlist.html), created by Bolton Bailey 2023-09-17, labels `enhancement, help-wanted, please-adopt` (via bot posts of 2024-04-30 and 2025-12-01).

Community formatters (post-2026)
- `duckki/leanfmt` ([announcement thread, 2026-07-21 and 2026-08-19](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Formatter.20for.20Lean.204.html)); see `notes/community-leanfmt.md`.
- `toku-sa-n/leanfmt` ("A fast, opinionated code formatter for Lean 4", README says Apache-2.0, `gh` reports no license; last push 2026-06-19) and `wvhulle/lean4` fork; `jcreinhold/lean-fmt` on Reservoir ("formats Lean 4 source into one canonical style and lints it", found by search; not inspected). `codygunton/lean-fmt` is named in the 2026-06-16 thread.

## Rules
Not rules; the only style-relevant point of disagreement is line breaks: Duckki (2026-07-21) wants operators to lead wrapped lines because his "preference is slightly different from Lean community guidance", whereas Mathlib's style says operators go "before a line break rather than at the beginning of the next line".

## Reasons given
See the quotes: syntax extensibility, comments and hand-formatting preservation, parser round-trip bugs, and the need to annotate every syntax extension with formatting rules.

## What transfers to general-purpose Lean
- Any style guide for programs should assume an official formatter will arrive and should avoid specifying what a formatter will decide; open question is which layout questions the FRO formatter will settle (line width, operator position, `fun` arrow) and whether it will take Lean core's `style.md` or Mathlib's rules.
- Until then, enforcement is by reviewers and linters (`notes/mathlib-linters.md`).
- Syntax extensions (Batteries, Mathlib, user macros) will need formatting annotations: library authors adding notation are directly affected.

## Caveats and unverified items
- Status "unreleased" is as of the newest archived message (2026-07-09 in that thread; archive snapshot 2026-10-02). I did not check the lean4 repo for formatter code or release notes (unverified; vendored `lean4/doc/std/style.md` mentions formatting only as prose).
- The Reformat test claim (Lean 4 "can autoformat itself") is from the 2021 thread; Sebastian Ullrich's link there points at `tests/lean/Reformat.lean.expected.out`.
- Direct quotes were taken from locally parsed JSON; HTML entities and code blocks flattened.
