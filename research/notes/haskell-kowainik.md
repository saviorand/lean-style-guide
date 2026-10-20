# Kowainik Haskell Style Guide

| Field | Value |
|---|---|
| URL | https://kowainik.github.io/posts/2019-02-06-style-guide |
| Author / org | Kowainik (authors not named on the page) |
| Date / version | Post dated 2019-02-06 (URL). Source file `style-guide.md` in kowainik/org at `820ab655e295d27f73dab298c007e7db62579e6e` (repo last commit 2021-05-16). Page snapshot fetched 2026-10-17. |
| License | Source repo kowainik/org: **MPL-2.0** (`gh repo view`, LICENSE file begins "Mozilla Public License Version 2.0"). The rendered web post states no separate license. MPL-2.0 is file-level copyleft: quoting short excerpts with attribution is safe; adapting whole files requires keeping them under MPL. |
| Scope & audience | Kowainik's own Haskell projects; offered "inspired by commercial and free open source Haskell libraries and applications" |
| Kind | community advice |
| Lean version | n/a (Haskell) |
| Raw copy | `vendor/pages/other-langs/haskell-kowainik.md` (rendered), `haskell-kowainik-source.md` (repo source) |

## Summary
A modernized, more complete successor to Tibell's guide: explicit goals, 4-space indent, 90-column limit, naming rules including record-field prefixes and `un`-prefixed newtype fields, import policy, strict fields, deriving, if/case/let layout, GHC warning list. Its distinguishing feature is a stated list of four goals plus a rule that style changes be committed separately from functional changes.

## Rules
Goals ([section](https://kowainik.github.io/posts/2019-02-06-style-guide#style-guide-goals)):
> 1. Make code **easier to understand:** ideas for solutions should not be hidden behind complex and obscure code.
> 3. Make code **easier to write:** developers should think about code formatting rules as little as possible.
> 4. Make code **easier to maintain:** this style guide aims to reduce the burden of maintaining packages using version control systems unless this conflicts with the previous points.

Existing code ([section](https://kowainik.github.io/posts/2019-02-06-style-guide#rule-of-thumb-when-working-with-existing-source-code)):
> If you must make significant style modifications, then commit them independently from the functional changes so that someone looking back through the changelog can easily distinguish between them.

Layout: "Indent code blocks with *4 spaces*"; "The maximum allowed line length is *90 characters*"; "**No trailing whitespaces**".

Naming ([section](https://kowainik.github.io/posts/2019-02-06-style-guide#naming)):
> Try not to create new operators.
> Do not use ultra-short or indescriptive names like `a`, `par`, `g` unless the types of these variables are general enough.
> Do not introduce unnecessarily long names for variables.
> do not capitalize all letters when using an abbreviation as a part of a longer name. For example, write `TomlException` instead of `TOMLException`.
> It is usually a good idea to introduce a custom data type (enum or `newtype`) instead of using a commonly used data type (like `Int`, `String`, `Set Text`, etc.).
> `type` aliases are allowed only for specializing general types
> The field name for a `newtype` must be prefixed by `un` followed by the type name.
> Field names for the record data type should start with the full name of the data type.

Types/imports/strictness:
> Always use **explicit import lists** or **qualified imports**.
> All top-level functions *must* have type signatures.
> Fields of data type constructors should be strict. Specify strictness explicitly with `!`.
> Avoid abusing point-free style. Sometimes code is clearer when **not** written in point-free style
> Prefer `pure` over `return`.
> Write [Haddock documentation](...) for the top-level functions, function arguments and data type fields. The documentation should give enough information to apply the function without looking at its definition.

Warnings ([GHC options](https://kowainik.github.io/posts/2019-02-06-style-guide#ghc-options)): code should compile warning-free with `-Wall -Wcompat -Widentities -Wincomplete-uni-patterns -Wincomplete-record-updates -Wredundant-constraints -Wmissing-export-lists -Wpartial-fields -Wmissing-deriving-strategies -Wunused-packages`.

Existing code ([Rule of thumb when working with existing source code](https://kowainik.github.io/posts/2019-02-06-style-guide#rule-of-thumb-when-working-with-existing-source-code), added 2026-10-20):
> The general rule is to stick to the same coding style that is already used in the file you are editing. If you must make significant style modifications, then commit them independently from the functional changes so that someone looking back through the changelog can easily distinguish between them.

## Reasons given
Reasons are given at goal level (understand/read/write/maintain) and for a few rules: strict fields "helps to avoid space leaks and gives you an error instead of a warning in case you forget to initialize some fields"; explicit imports "more maintainable and robust against changes in dependent libraries"; explicit signatures "help to avoid cryptic type errors". Most layout rules have none.

## What transfers to general-purpose Lean
- A goals list in the guide's front matter; the "separate style commits from functional commits" rule.
- Newtype/wrapper-over-primitive advice (`structure` wrappers instead of bare `Nat`/`String`) and "type aliases only for specialising".
- Naming: full type name as field prefix is Haskell-specific (Lean has namespaced projections `Foo.field`); the acronym-casing rule has a Lean analogue (`Json` vs `JSON`; check Lean core naming).
- `pure` over `return`: Lean has both; useful comparison point.
- Warning policy list = candidate "linter set" section.
- Partial-field warning (`-Wpartial-fields`) parallels Lean structure/inductive partial accessors.

## Caveats and unverified items
- Layout details (alignment, `where` placement) are Haskell syntax specific and are not extracted here.
- Rendered page has no explicit license statement; MPL-2.0 is from the source repo.
