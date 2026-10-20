# Zulip: style debates (lambda arrow, official style, line length, docstrings, layout)

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/archive/ (threads cited individually) |
| Author / org | Lean Zulip participants |
| Date / version | Threads 2021-08 to 2026-06; archive clone `63dc76b4eb239e7814eb5e0cb421cb731b507301` (2026-10-02) |
| License | none stated for archive repo; messages remain authors' |
| Scope & audience | Mathlib/Lean core/Batteries |
| Kind | descriptive |
| Lean version | Lean 4 unless flagged |
| Raw copy | `vendor/repos/zulip-archive/zulip_json/<stream>/<topic>.json` |

## Summary
The most useful discussion for a programs guide is [official style? (lean4, 2023-06-29/30)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/official.20style.3F.html): it states that Lean core publishes no style guide, that Mathlib's is the most developed, and argues whether a mathematician-flavoured guide can serve general programs. Other threads cover the `fun`/`↦`/`λ` question (still unsettled in 2025), docstring layout (consensus in 2024), line length, indentation of namespaces, and `calc` layout. No thread was found on `where` vs `let rec` as style (grep hits were questions about how they work).

## Threads
Official vs community style (key thread)
- Mario Carneiro: "The most polished documentation we have on style matters comes from mathlib"; "lean4 repo doesn't have line limits"; "lean4 repo does not maintain a style guide"; Std/Mathlib style "absolutely does" have line limits. He lists math-biased habits not in the guide: "lots of use of variable; use of the root namespace; lots of use of notation especially unicode notation", which "can just be omitted from a general style guide". "The mathlib4 style looks significantly different from mathlib3, because we started with lean4 repo style and adapted it for a general audience."
- Mac Malone (Lake author): "Style, in my view, should be a per-project (or group) thing"; the mathlib guide "will be more mathematician focused and there is not yet a real need ... to create a more general Lean 4 style guide"; wants no heavy Unicode/variable use. Carneiro replies the guide is "a template for making project style guides" and asks him to propose changes; "just please stop assuming that it is unsuitable just because there are a lot of mathematician users".
- Style disagreements inside core are named: Leonardo de Moura wants parentheses in `if (<- x)`, Sebastian Ullrich does not (Malone, 2023-06-30). Carneiro: core style "is encoded in the pretty printer" only approximately; "style change PRs are not welcome, AFAIK".
- Context 2023: Jireh Loreaux's summary in [style guidelines (lean4, 2023-06-26)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/style.20guidelines.html): continued declaration lines 4 spaces, body 2 spaces, `by` at end of the line before the proof; for `do` blocks "I think the goal is to handle everything with more indentation, and eschew parenthesizing, but I'm not positive". 

`fun x =>` vs `↦` vs `λ`
- [=> notation (mathlib4, 2022-11-16)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/.3D.3E.20notation.html): Sébastien Gouëzel and Patrick Massot want `↦` ("That => is simply wrong in any context vaguely related to mathematics if it doesn't mean 'implies'"); Mario Carneiro: "I'm not sure I like the idea of an inconsistent or domain-dependent formatting convention, that sounds like hell for an autoformatter" and wants no "wildly divergent style from other lean 4 projects".
- [Should we remove/deprecate λ? (lean4, 2023-06-03)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Should.20we.20remove.2Fdeprecate.20.CE.BB.3F.html): Eric Wieser: "fun is just fun to write"; Carneiro: "λ is not so friendly to mathematical uses. It's type theory jargon." Mathlib later added a `lambdaSyntax` linter (`notes/mathlib-linters.md`).
- [Are "↦" and "=>" interchangeable? (lean4, 2024-11-26)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Are.20.22.E2.86.A6.22.20and.20.22.3D.3E.22.20interchangeable.3F.html): Kyle Miller: interchangeable for `fun`, not in `match`/`case` arms; `set_option pp.unicode.fun true` pretty-prints `↦`; Massot: "=> is wrong and ↦ is right".
- [Switch to ↦ (\mapsto) globally (mathlib4, 2025-08-18)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Switch.20to.20.E2.86.A6.20(.5Cmapsto).20globally.html): Junyan Xu proposes a global switch plus a linter; poll 48 votes from 41 people. Thomas Murrills: "I would use ↦ in 'math' files and => in 'programming' files (metaprogramming, infrastructure)"; Jovan Gerbscheid: "=> is faster to type ... and there are cases where ↦ doesn't work". Outcome: Jireh Loreaux (2025-08-20): "We don't exactly make changes based on majority rule ... I don't see a strong reason to disallow one option or the other at the moment." Kim Morrison: the poll "counts as general disagreement". Mathlib's guide still says "slightly prefer" `↦`.
- A pretty-printer parenthetical: in Mathlib `↦` is displayed because the lakefile sets `pp.unicode.fun` (Eric Wieser: "only when you are in a project that records this desire in the lakefile").

Docstrings and comments
- [style guide for comments? (lean4, 2024-05-15)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/style.20guide.20for.20comments.3F.html): Kim Morrison posts a proposed consensus for Lean/Batteries: one-line `/-- ... -/` docstrings "are great!"; multi-line docstrings put the delimiters on their own lines "but variation is permitted"; no indentation in block comments; comments get a space after `--`. Disagreements: Yaël Dillies and Johan Commelin prefer delimiters on the line; Morrison: "the FRO's internal style guide now says they must be on their own lines!"; whether comments must be "complete sentences" is relaxed to "complete grammatical phrases" (Thomas Murrills). Utensil Song and Jovan Gerbscheid ask for the indicative vs imperative mood to be written down. Linked to Batteries PR/issue "#475" (not opened). Bears directly on Batteries' lack of a style doc.
- [Docstring style? (mathlib4, 2022-11-18)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Docstring.20style.3F.html): Thomas Murrills asks where "don't restate the type, use present tense" is written; Morrison: "the best you'll find is [the Mathlib style page]"; Carneiro points to lean4 issue #1461 by Patrick Massot about a style guide.
- [tactic docstrings (lean4, 2023-09-28)](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/tactic.20docstrings.html): Carneiro: cross-references instead of copy-paste are "a discouraged method of documentation".

Layout and linters
- [Should namespaces be indented? (new-members, 2023-10-13)](https://leanprover-community.github.io/archive/stream/113489-new-members/topic/Should.20namespaces.20be.20indented.3F.html): Mathlib does not indent; David Loeffler: for multi-screen namespaces "indenting it doesn't really add readability". The Lean Manual does indent.
- [calc indentation: style guide? (mathlib4, 2024-02-19)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/calc.20indentation.3A.20style.20guide.3F.html): several co-existing calc layouts; Yury Kudryashov asks whether to standardise (14 messages; no conclusion read).
- [Improving the mathlib style guide (general, 2022-07-30)](https://leanprover-community.github.io/archive/stream/113488-general/topic/Improving.20the.20mathlib.20style.20guide.html): Violeta Hernández runs polls on trailing commas, infix spacing and spacing after `←` in `rw`. **Lean 3 era** (`begin ... end`). Yakov Pechersky: "a 'black' style tool would be great. But likely only really feasible and useful lean4".
- [Style linter for ← (PR reviews, 2024-08-09)](https://leanprover-community.github.io/archive/stream/144837-PR-reviews/topic/Style.20linter.20for.20.E2.86.90.html): Ruben Van de Velde: backward arrows in `rw` are always spaced in Mathlib; "I think this was a bad choice in the mathport output, but that's where we are".
- [Line length linter (general, 2021-02-12)](https://leanprover-community.github.io/archive/stream/113488-general/topic/Line.20length.20linter.html) and [line length (2021-08-13)](https://leanprover-community.github.io/archive/stream/113488-general/topic/line.20length.html): **Lean 3** mathlib's `scripts/lint-style` checked lines; a pre-push hook calling it. These are where the 100-column check was enforced before the Lean 4 `longLine` linter.
- [Rewriting Python style linters in Lean (PR reviews, 2024-05-31)](https://leanprover-community.github.io/archive/stream/144837-PR-reviews/topic/Rewriting.20Python.20style.20linters.20in.20Lean.html) and [Duplication in style linters (mathlib4, 2024-08-14)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Duplication.20in.20style.20linters.html): history of moving Mathlib's text linters from Python to Lean (titles only; bodies not read).
- [Style linter too picky? (mathlib4, 2026-06-10)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Style.20linter.20too.20picky.3F.html): docstring linter rejects a space before `;` inside a code block; Gerbscheid: "Punctuation should not be in a code block".
- [Looking for code style review (new-members, 2024-12-09)](https://leanprover-community.github.io/archive/stream/113489-new-members/topic/Looking.20for.20code.20style.20review.html), [style guide concerning macros that add parens for fn calls (2025-10-03)](https://leanprover-community.github.io/archive/stream/113489-new-members/topic/style.20guide.20concerning.20macros.20that.20add.20parens.20for.20fn.20calls.html), [style guidelines for grind (mathlib4, 2026-02-06)](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/style.20guidelines.20for.20grind.html): titles only, not read.

## Rules
Quotes above only; none are normative.

## Reasons given
- `↦`: mathematical reading of `=>`; consistent Unicode in pp output.
- `=>`: faster to type, works in all binders, consistent with metaprogramming.
- `λ` disallowed: type-theory jargon, `fun` already available.
- Delimiters on own lines: avoids confusion about indentation of docstring continuation lines (Eric Wieser, 2024-05-15).

## What transfers to general-purpose Lean
- The thread [official style?] is the single best evidence that the community knows Mathlib's guide is the de facto standard, that no program-oriented guide exists, and that some leaders (Malone) consider a per-project style the right model; Carneiro's list of math-biased habits is a ready exclusion list.
- Open disputes a programs guide inherits unresolved: `=>` vs `↦` (programs plausibly `=>`), docstring delimiter placement and mood, `calc` layout (probably irrelevant), namespace indentation, `do` parenthesisation.
- A formatter-compatible style is desirable (Carneiro, 2022: domain-dependent conventions are "hell for an autoformatter").

## Caveats and unverified items
- Quotes were read from locally parsed JSON; code blocks truncated.
- Several thread bodies listed as "titles only".
- The claim that Batteries adopted Morrison's comment conventions is **unverified**; the thread says "#475" without repo context in the text I read.
