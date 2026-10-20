# HLint (default hints as codified practice)

| Field | Value |
|---|---|
| URL | https://github.com/ndmitchell/hlint |
| Author / org | Neil Mitchell |
| Date / version | `7f5a30407968d5be857424c03139b1814f21af5b`, 2026-09-26 |
| License | BSD-3-Clause (LICENSE file: "Copyright Neil Mitchell 2006-2026", three-clause redistribution text; `gh` reports "Other" because of the copyright line). Quoting with attribution is fine. |
| Scope & audience | Haskell programmers; a linter, not a guide |
| Kind | descriptive (codified practice enforced by a tool) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/haskell-hlint-readme.md`, `haskell-hlint-hints.md` |

## Summary
HLint suggests code improvements via ~900 rewrite rules in `data/hlint.yaml`, grouped by builtin categories. The README documents a severity model (error / warning / suggestion) and says outright that most hints are "a good idea in most circumstances, but not universally". Optional hint groups (e.g. `partial`) are disabled by default. The point for the style guide: which rules a community considers mechanical enough to automate, and how it distinguishes "always" from "taste".

## Rules (structure and representative hints)
Categories in [`hints.md`](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/hints.md): Bracket, Comment, Export, Extensions, Fixities, Import, Lambda, List, ListRec, Monad, Naming, Negation, NewType, NumLiteral, Pattern, Pragma, Stutter, Unsafe, plus "Configured hints" from `hlint.yaml`.

Severity model ([README L163-L171](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/README.md#L163-L171)):
> **Warning** - for example `concat (map f x)` suggests `concatMap f x` as a "warning" severity hint. From a style point of view, you should always replace a combination of `concat` and `map` with `concatMap`.
> **Suggestion** - ... Suggestion hints are often worthwhile, but should not be applied blindly.
> The difference between warning and suggestion is one of personal taste, typically my personal taste.

Representative hints:
- Use a specific library function instead of a composition: `concat . map f` to `concatMap f`; `not (a == b)` to `a /= b`; `if x then True else b` to `x || b`.
- Redundant syntax: "Redundant bracket", "Redundant if", "Redundant return", "Eta reduce", "Use section", "Use tuple-section" ([hints.md Lambda](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/hints.md#L346)).
- Naming: single hint "Use camelCase" (severity Suggestion) ([hints.md L1061](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/hints.md#L1061)).
- Stutter: "Redundant module qualifier" (e.g. `Foo.fooBar`-style repetition).
- Unsafe: "Missing NOINLINE pragma" for `unsafePerformIO` globals.
- Partial functions, disabled by default, in two groups ([hlint.yaml L1219-L1280](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/data/hlint.yaml#L1219-L1280)):
> # Warn on partial functions whose use can be avoided relatively easily.
> # Strictly warn even on partial functions in the base package whose use are almost unavoidable for their functionality.
Rule name: "Avoid partial function".

## Reasons given
- Not about performance: "HLint doesn't suggest optimisations, it suggests code improvements - the intention is to make the code simpler" ([README L153](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/README.md#L153)).
- Hints are annotated with semantic notes ("Decreases laziness", "Removes error") when not a perfect substitution ([README L155-L161](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/README.md#L155-L161)).
- "Most hints are intended to be a good idea in most circumstances, but not universally - judgement is required. ... only make changes you consider improvements - not merely to adhere to HLint rules." ([README L72](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/README.md#L72))
- Adoption path: `hlint . --default > .hlint.yaml` generates a file ignoring all outstanding hints, to tighten over time ([README L69](https://github.com/ndmitchell/hlint/blob/7f5a30407968d5be857424c03139b1814f21af5b/README.md#L69)).

## What transfers to general-purpose Lean
- Two-tier severity (always vs taste) and a hint-note vocabulary are a model for how a guide can label rules (e.g. "must" vs "consider").
- A separate, off-by-default `partial` group is an exact analogue of Lean's `get!`, `[i]!`, `head!`, `panic!` family; it frames "avoid partial functions" as opt-in, split into avoidable and unavoidable. (analysis)
- Hints are rewrite pairs (lhs/rhs); a guide could phrase simple rules in the same "instead of X write Y" form with a mechanical check.
- Category list shows what Haskell considers automatable: redundant syntax, library function substitution, stutter in qualified names.

## Caveats and unverified items
- Counts: `grep -c 'warn:'` gives 924 matching lines in `hlint.yaml`; this includes group rules. Not a count of distinct hints.
- Whether hlint's choices are "community consensus" is not claimed by the source; it says taste is largely the author's.
