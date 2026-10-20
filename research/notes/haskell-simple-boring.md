# Simple Haskell and the Boring Haskell Manifesto

| Field | Value |
|---|---|
| URL | (1) https://www.simplehaskell.org/ (2) https://www.snoyman.com/blog/2019/11/boring-haskell-manifesto/ |
| Author / org | (1) The Simple Haskell Initiative; the page quotes Lennart Augustsson, Graham Hutton, Don Stewart, Richard Eisenberg and Mark Karpov (2) Michael Snoyman |
| Date / version | (1) undated; the linked posts date from 2019-12 to 2020-05; fetched 2026-10-20 (2) November 2019 (URL); fetched 2026-10-20 |
| License | none stated on either page; the snoyman.com repo has no licence (`gh api`). Short quotes with citation only. |
| Scope & audience | Teams using Haskell in industry |
| Kind | community advice (position statements, not style guides) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/haskell-simple.md`, `vendor/pages/other-langs/haskell-boring-manifesto.md` |

## Summary
Two short position statements from 2019. Both argue that production code should use a simple, well-understood subset of Haskell rather than its newest features. Neither is a style guide; there are no layout or naming rules. They matter to this guide as support for its principles, and for the advice FPIL also gives against indexed families and other "fancy" types in APIs.

## Rules
Simple Haskell ([simplehaskell.org](https://www.simplehaskell.org/)):
> Industrial Haskell users are realizing that the key to delivering software on time and under budget is to keep it simple.

> **Accessibility.** Commercial software is a team endeavor. Fancy Haskell is costly to teams because it usually takes more time to understand and limits the pool of people who can effectively contribute.

> **Maturity.** Things that have been around longer will be more well-tested and understood by a larger group of people. Prefer tried and true techniques over the latest shiny library or language feature.

> **Leaking Complexity.** If you adopt a new thing, how much of its complexity will spread throughout the rest of your codebase?

Boring Haskell Manifesto ([The Boring Haskell Manifesto](https://www.snoyman.com/blog/2019/11/boring-haskell-manifesto/#the-boring-haskell-manifesto), [Power-to-weight ratio](https://www.snoyman.com/blog/2019/11/boring-haskell-manifesto/#power-to-weight-ratio)):
> for many cases of software engineering, a simple, well-defined subset of Haskell's language and ecosystem will deliver large value for a project, while introducing little to no risk compared to alternative options.

> we want to choose features which provide lots of benefits while minimizing costs.

The costs it lists are the learning curve, ongoing cognitive overhead, ongoing tweaking, slower compile times and poor performance. Its example of a good trade is sum types.

## Reasons given
Team cost (time to understand, who can contribute), maturity (well-tested, widely understood) and containment (how far complexity spreads).

## What transfers to general-purpose Lean
- Supports the guide's principles: established practice, and spending on types only where the benefit is clear.
- Supports the rule against indexed families in APIs, and restraint with macros and custom notation.
- Doesn't transfer: the specific Haskell 98 subset, and the `rio` library recommendation.

## Caveats and unverified items
- The quotes on simplehaskell.org were not traced to their original posts.
- The manifesto marks its second half as "draft quality at best". Only the first half is cited.
