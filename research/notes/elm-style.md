# Elm style guide and elm-format

| Field | Value |
|---|---|
| URL | https://elm-lang.org/docs/style-guide ; https://github.com/avh4/elm-format |
| Author / org | Elm project (Evan Czaplicki); elm-format by Aaron VonderHaar (avh4) |
| Date / version | Style guide source `pages/docs/style-guide.elm` in elm/elm-lang.org, last commit `66e07115fb6c0b4c8ea6a60f44c1ac495b5ce6c6` (2019-04-04). elm-format `e7e5da37716acbfb4954a88128b5cc72b2c911d9` (2025-06-16, v0.8.7). |
| License | elm-lang.org repo: BSD-3-Clause (`gh repo view`; applies to repo as a whole, **page text not separately licensed**). elm-format: BSD-3-Clause (LICENSE; copyrights Evan Czaplicki, Aaron VonderHaar, Facebook...). |
| Scope & audience | Elm programmers; a very short guide |
| Kind | normative (official) ; elm-format descriptive |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/elm-style-source.elm` (the page is client-rendered; defuddle returned empty, so the Elm source was fetched from GitHub), `elm-format-readme.md` |

## Summary
The official guide is a half-page of goals and layout rules whose single justification is "clean diffs": regularity over compactness, and no alignment that depends on name lengths. elm-format implements that guide "according to a standard set of rules", modelled on gofmt (that it offers no options is not stated in the README; see Caveats).

## Rules
Goal ([source L16-L18](https://github.com/elm/elm-lang.org/blob/66e07115fb6c0b4c8ea6a60f44c1ac495b5ce6c6/pages/docs/style-guide.elm#L16-L18)):
> **Goal:** a consistent style that is easy to read and produces clean diffs. This means trading aggressively compact code for regularity and ease of modification.

Rules:
> Keep it under 80 characters. Going over is not the end of the world, but consider refactoring before you decide a line really must be longer.
> **Be Descriptive.** One character abbreviations are rarely acceptable, especially not as arguments for top-level function declarations where you have no real context about what they are.
> **Qualify variables.** Always prefer qualified names. `Set.union` is always preferable to `union`. In large files and in large projects, it becomes very very difficult to figure out where variables came from without this.
> Always have type annotations on top-level definitions. Always have 2 empty lines between top-level declarations. Always bring the body of the declaration down one line.
> Having `case` appear *later* than the actual cases is strongly discouraged.
> Do not be a maniac with indentation. Simplicity will be better in the long run.

Good/Bad pairs follow each (type declarations with leading `=` and `|`, record fields with leading commas).

elm-format ([README](https://github.com/avh4/elm-format/blob/e7e5da37716acbfb4954a88128b5cc72b2c911d9/README.md#L5-L16)):
> formats Elm source code according to a standard set of rules based on the official Elm Style Guide. It is inspired by the popular gofmt.
> It makes code **easier to write** ... **easier to read** ... **easier to maintain**, because you can no longer have diffs related only to formatting; every diff necessarily involves a material change.
> It **saves your team time** debating how to format things

## Reasons given
Every layout rule is justified by diff behaviour with an explicit before/after thought experiment: renaming a type, adding a longer field, or lengthening a constructor should not force realignment of neighbouring lines; "ending lines with a comma makes diffs messier because adding a field must change two lines instead of one". The justification is stated for the Bad examples, not just asserted.

## What transfers to general-purpose Lean
- A rule-justification pattern: show the diff caused by one edit.
- Qualified-name preference and "top-level annotations always": Lean requires type annotations on `theorem`s in practice, and recommends them for public `def`s; qualified use of names under a namespace is a Lean `open` question.
- Alignment independent of name length (same as F#, Rust).
- No-config formatter stance: elm-format's README does not discuss configuration directly; the README table of editor integrations has a "Configuration" column concerning editor plugin setup, not formatter options. That elm-format has **no style options** is **unverified** here (no explicit statement found).

## Caveats and unverified items
- The style-guide page has no licence statement; the guide has not changed since 2019 as far as the commit history shows (only the latest commit on that path was checked).
- elm-format "no config" claim in the task brief: not found as a quoted statement in the README. Lead can check `elm-format --help` or issue tracker.
