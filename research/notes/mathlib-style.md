# Mathlib style guide (leanprover-community)

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/contribute/style.html |
| Author / org | Lean community / Mathlib maintainers (source: leanprover-community.github.io repo, `templates/contribute/style.md`) |
| Date / version | Page served 2026-10-17 (HTTP last-modified is the site build time, not content). Source file last changed 2026-09-14, [`7342787`](https://github.com/leanprover-community/leanprover-community.github.io/blob/734278725a437c9975ff74447a18c6d5ee4cab9d/templates/contribute/style.md). Mentions the `module` keyword and `public import`, so it tracks current Lean 4 (toolchain v4.36.0-rc1 era) |
| License | MIT (GitHub repo metadata of leanprover-community.github.io; the page footer states none) |
| Scope & audience | Mathlib contributors; "guidelines rather than rigid rules". Also the de facto reference for Batteries, CSLib, Iris-Lean |
| Kind | normative (for Mathlib), community advice elsewhere |
| Lean version | Lean 4 (Lean 3 origins; see caveats) |
| Raw copy | `vendor/pages/community/mathlib-style.md` (also `mathlib-index.md` for contribute/index.html) |

## Summary
The main written Mathlib style document: variable names, Unicode, line length, header/imports, module docstrings, declaration layout, instances, binders, anonymous functions, tactic mode, `simp` squeezing, performance, transparency/API design, whitespace, normal forms, trace-message formatting, deprecation. Much of it is layout that applies to any Lean file; the variable conventions, hypotheses-left-of-colon, conjunction, `calc`/tactic and transparency sections are theorem-proving specific. The intro states the purpose: ["Having a uniform style makes it easier to browse the library and read the contents, but these are meant to be guidelines rather than rigid rules."](https://leanprover-community.github.io/contribute/style.html) The sibling page `contribute/index.html` adds that style-only PRs not covered by the guide "may be closed" and should first get Zulip consensus ([Style changes](https://leanprover-community.github.io/contribute/index.html#style-changes)).

## Rules
Layout (general in nature)
> Lines should not be longer than 100 characters. ([Line length](https://leanprover-community.github.io/contribute/style.html#line-length))

> All declarations ... and commands ... are considered top-level and these words should appear flush-left in the document. In particular, opening a namespace or section does not result in indenting the contents ([Structuring definitions and theorems](https://leanprover-community.github.io/contribute/style.html#structuring-definitions-and-theorems))

> Use spaces on both sides of ":", ":=" or infix operators. Put them before a line break rather than at the beginning of the next line.

> After stating the theorem, we indent the lines in the subsequent proof by 2 spaces. ... If the theorem statement requires multiple lines, indent the subsequent lines by 4 spaces. The proof is still indented only 2 spaces ... `by` is placed on the line *prior* to the first tactic; however, `by` should not be placed on a line by itself.

> When providing terms of structures or instances of classes, the `where` syntax should be used to avoid the need for enclosing braces ([Instances](https://leanprover-community.github.io/contribute/style.html#instances))

> Use a space after binders. Also, the binder type should generally be written explicitly, even if Lean doesn't need this information. ([Binders](https://leanprover-community.github.io/contribute/style.html#binders))

> The Lean default for this is `fun x => x * x`, but the `↦` arrow ... is also valid. In mathlib the pretty printer displays `↦`, and we slightly prefer this in the source as well. The lambda notation `λ x ↦ x * x`, while syntactically valid, is disallowed in mathlib in favor of the `fun` keyword. ([Anonymous functions](https://leanprover-community.github.io/contribute/style.html#anonymous-functions))

> sometimes parentheses can be avoided by judicious use of the `<|` operator (or its cousin `|>`). Note: while `$` is a synonym for `<|`, its use in mathlib is disallowed ([Whitespace and delimiters](https://leanprover-community.github.io/contribute/style.html#whitespace-and-delimiters))

> Empty lines inside declarations are discouraged and there is a linter that enforces that they are not present. ([Empty lines](https://leanprover-community.github.io/contribute/style.html#empty-lines-inside-declarations))

> We generally use a blank line to separate theorems and definitions, but this can be omitted ... to group together a number of short definitions

Header and docs
> The file header should contain copyright information, a list of all the authors ..., and a description of the contents. Put the `module` keyword on its own line right after the header, skip a line, then group all `public import`s together ... ([Header and imports](https://leanprover-community.github.io/contribute/style.html#header-and-imports))

> Use module doc delimiters `/-! -/` to provide section headers ... `/- -/` for more technical comments ... `--` for short or in-line comments. Documentation strings for declarations are delimited with `/-- -/`. When a documentation string ... spans multiple lines, do not indent subsequent lines.

Unicode and symbols
> Use special Unicode characters, especially mathematical symbols where they help develop good notation and improve readability. Avoid ... characters which change text direction; invisible characters ...; characters which modify other characters ([Unicode usage](https://leanprover-community.github.io/contribute/style.html#unicode-usage))

Variable names (math-specific): `α β γ` generic types, `a b c` propositions, `x y z` elements, `h` assumptions, `p q r` predicates, `s t` lists/sets, `m n k` naturals, `i j k` integers, `G R K E` for algebraic structures ([Variable conventions](https://leanprover-community.github.io/contribute/style.html#variable-conventions)).

API and proofs
> Hypotheses should not be conjunctions, as this typically makes the lemma harder to use ... the return type of a lemma should not be a conjunction ([Conjunctions, disjunctions](https://leanprover-community.github.io/contribute/style.html#conjunctions-disjunctions))

> Generally, having arguments to the left of the colon is preferred over having arguments in universal quantifiers or implications, if the proof starts by introducing these variables. ([Hypotheses Left of Colon](https://leanprover-community.github.io/contribute/style.html#hypotheses-left-of-colon))

> terminal `simp` calls ... should not be *squeezed* ... ([Squeezing simp calls](https://leanprover-community.github.io/contribute/style.html#squeezing-simp-calls))

> The default for mathlib is that definitions should be `semireducible` unless there is a good reason otherwise which should be clearly articulated in the PR description. ([Transparency and API design](https://leanprover-community.github.io/contribute/style.html#transparency-and-api-design))

> In general, we try to settle on one standard form, called the normal form, and use it both in statements and conclusions of theorems ([Normal forms](https://leanprover-community.github.io/contribute/style.html#normal-forms))

> Any publicly exposed theorems and definitions that are being removed should be gracefully transitioned by keeping the old declaration with a `@[deprecated]` attribute ... Deprecated declarations can be deleted after 6 months. ([Deprecation](https://leanprover-community.github.io/contribute/style.html#deprecation))

> Inside all printed messages ... names and interpolated data should either be inline and surrounded by backticks ... or on their own line and indented (via e.g. `indentD`) ([Expressions in error or trace messages](https://leanprover-community.github.io/contribute/style.html#expressions-in-error-or-trace-messages))  -- the one section aimed at metaprogram authors

Also covered: no `;`-chained tactics ("we opt for a style which avoids delimiting code"), space after `←` in `rw`/`do` (`do return (← f) + (← g)`), `!bench` for performance-sensitive PRs, avoid `nonrec`.

## Reasons given
- Line length: "easier to read, especially on a small screen or in a small window."
- Not squeezing `simp`: squeezed calls drown the key lemmas and "break when one such lemma gets renamed".
- Empty lines: uniformity; "even a short sentence communicates much more than an empty line".
- `<|` over `$`: consistency and symmetry with `|>`.
- Hypotheses left of colon, conjunctions: usability of lemmas (no reason beyond "harder to use").
- `↦`: "slightly prefer"; no reason given beyond the pretty-printer. (Zulip: see `notes/zulip-style-misc.md`.)
- Most layout rules (indent 2/4, flush-left, `where`) give no reason.

## What transfers to general-purpose Lean
- Transfers: 100-column limit (Lean core's `doc/std/style.md` has no 100-column rule in a grep for "100"/"width"/"column"; Zulip: Mario Carneiro 2023-06-29, "lean4 repo doesn't have line limits", see `notes/zulip-style-misc.md`), 2-space body / 4-space continuation, flush-left top-level, `where` for instances, operators-before-line-break, `fun` over `λ`, `<|` over `$`, module-docstring/header structure, deprecation with `since`, trace-message formatting, no empty lines in declarations (contentious for long programs).
- Math-specific, drop: variable letters, hypotheses-left-of-colon and conjunction advice, normal forms, `simp` squeezing, transparency/`irreducible_def`, Unicode-forward stance, `calc` layout.
- Needs adapting: header text (copyright/authors line is Mathlib-specific and linted); "avoid delimiting code" (`;`) vs. programs, where `do`-block `;` and `<;>` conventions are unaddressed.
- Silent on: programs (`do` notation, `where` vs `let rec`, structural vs well-founded recursion, error handling, `partial`, `IO`), tests, API shape of `get?`/`get!`/`getD`.

## Caveats and unverified items
- Lean 3 provenance: the guide descends from the Lean 3 mathlib style guide; pieces such as the variable conventions and 100-column rule date from Lean 3 (Zulip: [Line length linter, 2021-02-12](https://leanprover-community.github.io/archive/stream/113488-general/topic/Line.20length.20linter.html) shows `lint-style.py` enforcing it in Lean 3 mathlib). Mario Carneiro said in 2023 that the mathlib4 style "started with lean4 repo style and adapted" (see `notes/zulip-style-misc.md`).
- The doc contained a known indentation error until fixed ([Zulip, 2024-02-18](https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Is.20the.20indentation.20level.20wrong.20in.20the.20style.20guide.3F.html)).
- Not individually read: sections Calculations, Tactic mode (details), Profiling.
