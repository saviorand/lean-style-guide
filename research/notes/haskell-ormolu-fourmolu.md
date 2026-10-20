# Ormolu and Fourmolu design decisions

| Field | Value |
|---|---|
| URL | https://github.com/tweag/ormolu ; https://github.com/fourmolu/fourmolu ; https://fourmolu.github.io/config/ |
| Author / org | Tweag I/O and Mark Karpov (Ormolu); Matt Parsons and contributors (Fourmolu) |
| Date / version | ormolu `56fd8afc3ca03d9b32fa33785cffc673d27d7e1f` (2026-10-01); fourmolu `cae291b3363c9a404a16caeba79f704683b96c1a` (2026-10-02) |
| License | Both BSD-3-Clause (LICENSE.md: "Redistributions of source code must retain...", "Neither the names Tweag I/O and Mark Karpov..."; copyright "2018 Tweag I/O, 2026 Mark Karpov" and "2018-2020 Tweag I/O, 2020-present Matt Parsons"). `gh` reports "Other". |
| Scope & audience | Haskell formatter authors/users |
| Kind | descriptive (design rationale of tools) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/haskell-ormolu-readme.md`, `haskell-ormolu-design.md`, `haskell-fourmolu-readme.md`, `haskell-fourmolu-config.md` |

## Summary
Ormolu deliberately has no configuration: one "true" style, minimal diffs, idempotence, and layout partly programmable by the author's line breaks. Fourmolu is a fork whose README strikes through the "no configuration" goal and exposes about 28 options. The pair is the clearest Haskell data point for the formatter-config debate.

## Rules / decisions
Ormolu goals ([README L36-L50](https://github.com/tweag/ormolu/blob/56fd8afc3ca03d9b32fa33785cffc673d27d7e1f/README.md#L36-L50)):
> Make some whitespace programmable. The layout of the input influences the layout choices in the output, so the choice between single-line and multi-line layouts is made by the user rather than by an algorithm.
> Implement one "true" formatting style that admits no configuration.
> Produce minimal diffs.
> Guarantee idempotence: formatting already formatted code doesn't change it.

Why no config ([DESIGN.md L310-L318](https://github.com/tweag/ormolu/blob/56fd8afc3ca03d9b32fa33785cffc673d27d7e1f/DESIGN.md#L310-L318)):
> We are not allowing to configure any aspect of the formatter. A module might be used in multiple projects, and we prefer to have it formatted the same in all of them.
> ... as long as the default style is conventional and good it doesn't really matter how code gets formatted. Consistency is more important.

What the printer controls vs the author ([DESIGN.md L233-L260](https://github.com/tweag/ormolu/blob/56fd8afc3ca03d9b32fa33785cffc673d27d7e1f/DESIGN.md#L233-L260)): the printer controls every choice except (1) location of comments and (2) line breaking.

Fourmolu ([README L27-L42](https://github.com/fourmolu/fourmolu/blob/cae291b3363c9a404a16caeba79f704683b96c1a/README.md#L27-L42)):
> We share all bar one of Ormolu's goals: ... ~~Implementing one "true" formatting style which admits no configuration.~~ We allow configuration of various parameters, via CLI options or config files. We encourage any contributions which add further flexibility.

Fourmolu options ([config page](https://fourmolu.github.io/config/)): `indentation`, `column-limit`, `function-arrows`, `comma-style`, `record-style`, `import-export-style`, `import-grouping`, `indent-wheres`, `record-brace-space`, `newlines-between-decls`, `haddock-style`, `haddock-style-module`, `haddock-location-signature`, `let-style`, `in-style`, `if-style`, `single-constraint-parens`, `single-deriving-parens`, `sort-constraints`, `sort-derived-classes`, `sort-deriving-clauses`, `trailing-section-operators`, `unicode`, `respectful`, plus semantic inputs `fixities`, `reexports`, `local-modules`.
Ormolu names Fourmolu as a fork "which uses 4-space indentation and allows arbitrary configuration" ([README L352-L357](https://github.com/tweag/ormolu/blob/56fd8afc3ca03d9b32fa33785cffc673d27d7e1f/README.md#L352-L357)).
Fourmolu invites options: "If there are any options you'd like to see, let us know. If it's not too complicated to implement ... we'll probably add it." ([README L303](https://github.com/fourmolu/fourmolu/blob/cae291b3363c9a404a16caeba79f704683b96c1a/README.md#L303))

## Reasons given
- Ormolu: one style across projects; avoid debate (cites Chris Done, hindent author).
- Fourmolu: **no reason is given** in the README for dropping the no-config goal beyond the strike-through; the visible motivating example is indentation (Ormolu uses 2, Fourmolu supports 4). The option list shows what people actually wanted to vary: indentation, line width, comma and arrow placement, record style, import grouping, Haddock placement.

## What transfers to general-purpose Lean
- If Lean grows a community formatter, the Ormolu design (single style, idempotent, minimal diffs, author-controlled line breaks) is the minimal-debate model; Fourmolu's option list is a catalogue of the points where users will dissent.
- "Programmable whitespace" (author chooses one-line vs multi-line) fits Lean's term-mode style, where mechanical line-breaking is hard. (analysis)
- A style guide that precedes a formatter should avoid rules the formatter would own (indentation, alignment).

## Caveats and unverified items
- Fourmolu's rationale for configurability is **unverified** (not in README/config page). Defaults of Fourmolu (e.g. indentation 4) not checked in the generated config; the repo's own `fourmolu.yaml` sets `indentation: 2` "to imitate Ormolu".
