# The Ruby Style Guide (bbatsov / RuboCop) - format model

| Field | Value |
|---|---|
| URL | https://rubystyle.guide/ ; source https://github.com/rubocop/ruby-style-guide |
| Author / org | Bozhidar Batsov and the RuboCop editor team |
| Date / version | `357eb786d6b7c2dbaaf57820bc997c03adb75c19`, 2026-07-20; started 2011 as an internal company guide ([History](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L6421)) |
| License | **CC BY 3.0 Unported** ([License](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L6484)) |
| Scope & audience | Ruby programmers; RuboCop is "based on this style guide" |
| Kind | community advice |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/bbatsov-ruby.adoc` |

## Summary
The original of the format that the Clojure guide copied ("the Clojure style guide is pretty similar in structure to the Ruby style guide"). About 6,500 lines and 301 rule-level headings; far longer than Clojure's because Ruby has more features. Same intro, same "Guiding Principles" and "A Note about Consistency" sections, same contribution and license footer. Each rule has an anchor, a short title, prose, and `# bad` / `# good` code pairs. Rules map to RuboCop cops, which is the main structural difference: every rule is a lint candidate.

## Structure (top-level table of contents)
Introduction; Source Code Layout; Naming Conventions; Flow of Control; Exceptions; Files; Assignment & Comparison; Blocks, Procs & Lambdas; Methods; Classes & Modules; Classes: Constructors; Comments; Comment Annotations; Magic Comments; Collections; Numbers; Strings; Heredocs; Date & Time; Regular Expressions; Percent Literals; Metaprogramming; API Documentation; Gemfile and Gemspec; Misc; Tools; History; Sources of Inspiration; Contributing; Colophon; License; Spread the Word. (`grep '^== '`; first section begins [L13](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L13), layout at [L130](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L130).)
The README has `:toc: preamble` with `:toclevels: 1` so the generated table of contents lists only top-level sections.

## How a rule is written
- `=== Title [[kebab-anchor]]`, e.g. `=== Predicate Methods Suffix [[bool-methods-qmark]]`.
- One or two sentences stating the rule, optional reason, then code with comment labels `# bad`, `# good`, `# okish`, `# good - because...`; labels may carry a clarification after a dash.
- Admonitions `NOTE:`/`TIP:`. The word "Rationale" appears only a handful of times; explanation is inline.
Samples ([Predicate Methods Prefix](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L1074-L1110)):
> Avoid prefixing predicate methods with the auxiliary verbs such as `is`, `does`, or `can`. These words are redundant and inconsistent with the style of boolean methods in the Ruby core library, such as `empty?` and `include?`.
[Dangerous Method Suffix](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L1112-L1138):
> The names of potentially _dangerous_ methods (i.e. methods that modify `self` or the arguments, `exit!` ... ) should end with an exclamation mark if there exists a safe version of that _dangerous_ method.
with the bad example "there is no matching 'safe' method". Followed by [Relationship between Safe and Dangerous Methods](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L1140-L1160): "Define the non-bang (safe) method in terms of the bang (dangerous) one if possible."

## Intro, principles, disagreement
Same wording as Clojure ([Intro L13-L63](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L13-L60), [Guiding Principles](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L64-L86), [Consistency](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L87-L112)). Additional lines:
> A style guide that reflects real-world usage gets used, while a style guide that holds to an ideal that has been rejected by the people it is supposed to help risks not getting used at all - no matter how good it is.
> There are some areas in which there is no clear consensus in the Ruby community regarding a particular style (like string literal quoting, spacing inside hash literals, dot position in multi-line method chaining, etc.). In such scenarios all popular styles are acknowledged and it's up to you to pick one and apply it consistently.
> Ruby is famously optimized for programmer happiness. We'd like to believe that this guide is going to help you optimize for maximum programmer happiness.

## Contribution and license setup
[Contributing](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L6447-L6476): "Nothing written in this guide is set in stone"; fork/branch/PR steps; sponsorship links. [License](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L6484): CC BY 3.0. [Colophon](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L6477): AsciiDoc, converted from Markdown in 2019. Companion guides (Rails, RSpec) listed in the intro; tool tie-in: "RuboCop is a static code analyzer (linter) and formatter, based on this style guide".

## Rules that transfer (verbatim samples)
- Predicate suffix `?` and no `is_`/`can_` prefixes (above) — compare Lean's `isFoo` convention (Bool) vs plain predicates.
- Bang/safe pair rule: `!` only if a safe counterpart exists; define safe via dangerous. Directly relevant to Lean's `get!` / `get?`: Lean uses `!` for panic-on-failure partial variants.
- [Exceptions](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L2029): "Prefer `raise` over `fail`", "Don't specify `RuntimeError` explicitly", prefer class and message as separate arguments.
- [No Single-line Methods](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L2960): shows the "okish" grading.
- [Unused Variables Prefix](https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc#L1163): "Prefix with `_` unused block parameters and local variables." (Lean: `_x` suppresses linter.)

## Reasons given
Brief ("redundant and inconsistent with the style of boolean methods in the Ruby core library"); appeals to core-library precedent are the most common justification.

## What transfers to general-purpose Lean
Same as `bbatsov-clojure`; additionally the practice of pairing a guide with a linter (RuboCop cops) so each rule is checkable; and the style of grading examples (bad / okish / good).

## Caveats and unverified items
- Line numbers are from the SHA above. Did not read the full guide; rules sampled from Naming, Exceptions, Methods only.
- Rationale-frequency claim is from a grep count (6 matches of "Rationale/rationale") and not a full audit.
