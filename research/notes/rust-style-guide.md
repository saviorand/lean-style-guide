# The Rust Style Guide (default rustfmt style)

| Field | Value |
|---|---|
| URL | https://doc.rust-lang.org/style-guide/ (source: https://github.com/rust-lang/rust/tree/master/src/doc/style-guide) |
| Author / org | Rust Style Team (rust-lang) |
| Date / version | rust-lang/rust `158f79d5c24d262f820fa45da96e7b77bc29a338` (2026-10-17); guide files under `src/doc/style-guide/src/` |
| License | Apache-2.0 OR MIT (`LICENSE-APACHE`, `LICENSE-MIT` at repo root; `license-metadata.json` lists "Apache-2.0 OR MIT" for Rust Project Developers). |
| Scope & audience | Rust programmers and formatting-tool authors |
| Kind | normative for the default style (tool reference), not mandatory for users |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/rust-style-guide.md`, `rust-style-principles.md`, `rust-style-advice.md` |

## Summary
Defines the *default Rust style* that rustfmt implements. Notable for its explicit prioritized principles, its motivation for having a formatter at all, its status paragraph ("recommends" the default, does not forbid non-default styles or tool options), and the rule that a mismatch between guide and tool is a bug in one of them. Content: indentation, blank lines, trailing commas, sorting, then per-construct layout (items, statements, expressions, types) and a short non-formatting "advice" page and Cargo.toml conventions.

## Rules
Motivation ([README L3-L21](https://github.com/rust-lang/rust/blob/158f79d5c24d262f820fa45da96e7b77bc29a338/src/doc/style-guide/src/README.md#L3-L21)):
> Formatting code is a mostly mechanical task which takes both time and mental effort. By using an automatic formatting tool, a programmer is relieved of this task and can concentrate on more important things.
> Furthermore, by sticking to an established style guide ... programmers don't need to formulate ad hoc style rules, nor do they need to debate with other programmers what style rules should be used
> there are productivity benefits to using a formatting tool, and even larger benefits by using a community-consistent formatting, typically by using a formatting tool's default settings.

Status ([README L22-L45](https://github.com/rust-lang/rust/blob/158f79d5c24d262f820fa45da96e7b77bc29a338/src/doc/style-guide/src/README.md#L22-L45)):
> The Rust Style Guide defines the default Rust style, and *recommends* that developers and tools follow the default Rust style.
> This should not be interpreted as forbidding developers from following a non-default style, or forbidding tools from adding any particular configuration options.
> If the style guide differs from rustfmt, that may represent a bug in rustfmt, or a bug in the style guide

Principles, in rough priority order ([principles.md](https://github.com/rust-lang/rust/blob/158f79d5c24d262f820fa45da96e7b77bc29a338/src/doc/style-guide/src/principles.md)):
> readability (scan-ability; avoiding misleading formatting; accessibility; readability of code in contexts without syntax highlighting or IDE assistance, such as rustc error messages, diffs, grep, and other plain-text contexts)
> aesthetics (sense of 'beauty'; consistent with other languages/tools)
> specifics (compatibility with version control practices - preserving diffs, merge-friendliness; preventing rightward drift; minimising vertical space)
> application (ease of manual application; ease of implementation; internal consistency; simplicity of formatting rules)

Layout rules ([README L48-L120](https://github.com/rust-lang/rust/blob/158f79d5c24d262f820fa45da96e7b77bc29a338/src/doc/style-guide/src/README.md#L48-L120)):
> Use spaces, not tabs. Each level of indentation must be 4 spaces ... The maximum width for a line is 100 characters.
> Prefer block indent over visual indent ... This makes for smaller diffs (e.g., if `a_function_call` is renamed in the above example) and less rightward drift.
> In comma-separated lists of any kind, use a trailing comma when followed by a newline
Sorting ([README L123-L212](https://github.com/rust-lang/rust/blob/158f79d5c24d262f820fa45da96e7b77bc29a338/src/doc/style-guide/src/README.md#L123-L212)): "version sorting" so that `x8` comes before `x16`.

Names ([advice.md](https://github.com/rust-lang/rust/blob/158f79d5c24d262f820fa45da96e7b77bc29a338/src/doc/style-guide/src/advice.md)): "Types shall be `UpperCamelCase`... Function and method names shall be `snake_case` ... Constants ... `SCREAMING_SNAKE_CASE`"; "When a name is forbidden because it is a reserved word (such as `crate`), either use a raw identifier (`r#crate`) or use a trailing underscore (`crate_`). Don't misspell the word (`krate`)." Expression orientation: "Prefer to use Rust's expression oriented nature where possible".

## Reasons given
Principles page is the rationale; block indent justified by diffs and drift; formatting justified by debate-avoidance and pattern matching ("Humans comprehend information through pattern matching").

## What transfers to general-purpose Lean
- Guide structure: motivation, status ("default style" vs mandate), bug policy between guide and tool, ordered principles. Directly reusable pattern for a Lean guide that may precede a formatter.
- Principles list as a tie-breaker order (readability above aesthetics above specifics above tooling convenience), including "readable in plain-text contexts" which matters for Lean's error messages and `#print` output.
- Block indent over visual indent, trailing-comma rule (Lean has no trailing commas in most lists; check), version sorting for `import`s.
- Reserved-word renaming rule: Lean has `«name»` escaping; the analogous rule (avoid `«»` and misspellings like `type'`) could be adopted.

## Caveats and unverified items
- Only README, principles and advice were read; `items.md`, `expressions.md`, `statements.md`, `types.md`, `cargo.md` not extracted (mostly Rust-syntax layout).
- Line ranges are approximate to the checked-out files.
