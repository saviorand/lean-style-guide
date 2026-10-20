# Johan Tibell's Haskell Style Guide

| Field | Value |
|---|---|
| URL | https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md |
| Author / org | Johan Tibell (tibbe) |
| Date / version | repo HEAD `0d4fea64a87195192faa376696ea094d1aed4baa`, last commit 2015-11-06 |
| License | none stated (default copyright). Looked in: repo file list (README, `haskell-style.md`, `haskell-style.el`, no LICENSE file), `gh repo view` licenseInfo = null. **Cannot be quoted at length or adapted without permission.** |
| Scope & audience | Style of Tibell's own projects (containers, network, etc.); "preferred coding style for this project" |
| Kind | community advice (project-level, widely imitated) |
| Lean version | n/a (Haskell) |
| Raw copy | `vendor/pages/other-langs/haskell-tibell.md` |

## Summary
A short (420-line) guide to formatting, imports, comments, naming and strictness for Haskell. Mostly layout: 80 columns, 4-space indent, aligned constructors, `where` indented two spaces. The non-layout rules that matter are strict constructor fields by default, explicit/qualified imports, comment every top-level definition, and "avoid over-using point-free style". It defers to local consistency when the guide is silent. Sets the template that Kowainik's guide later modernized.

## Rules
Intro, [link](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L1-L12):
> When something isn't covered by this guide you should stay consistent with the code in the other modules.

Formatting ([L14-L60](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L14-L60)):
> Maximum line length is *80 characters*.
> Tabs are illegal.  Use spaces for indenting.  Indent your code blocks with *4 spaces*.  Indent the `where` keyword two spaces to set it apart from the rest of the code and indent the definitions in a `where` clause 2 spaces.
> One blank line between top-level definitions.  No blank lines between type signatures and function definitions.

If/case ([If-then-else](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L155-L160)):
> Generally, guards and pattern matches should be preferred over if-then-else clauses, where possible.

Imports ([section](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L224-L239)):
> Always use explicit import lists or `qualified` imports for standard and third party libraries.  This makes the code more robust against changes in these libraries.  Exception: The Prelude.
Imports are grouped stdlib / third party / local, blank line between groups, sorted alphabetically within a group.

Comments ([section](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L240-L318)):
> Comment every top level function (particularly exported functions), and provide a type signature; use Haddock syntax in the comments. Comment every exported data type.
> For functions the documentation should give enough information to apply the function without looking at the function's definition.
> Write proper sentences; start with a capital letter and use proper punctuation.

Naming ([section](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L319-L333)):
> For readability reasons, don't capitalize all letters when using an abbreviation.  For example, write `HttpServer` instead of `HTTPServer`.  Exception: Two letter abbreviations, e.g. `IO`.
> Use singular when naming modules e.g. use `Data.Map` and `Data.ByteString.Internal` instead of `Data.Maps` and `Data.ByteString.Internals`.

Laziness ([section](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L335-L404)):
> By default, use strict data types and lazy functions.
> Constructor fields should be strict, unless there's an explicit reason to make them lazy.

Misc ([L405-L420](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/haskell-style.md#L407-L420)):
> Avoid over-using point-free style.  For example, this is hard to read: `f = (g .) . h`
> Code should be compilable with `-Wall -Werror`.  There should be no warnings.

## Reasons given
- Consistency: "It is much easier to understand a large codebase when all the code in it is in a consistent style." ([intro](https://github.com/tibbe/haskell-style-guide/blob/0d4fea64a87195192faa376696ea094d1aed4baa/README))
- Strict fields: "avoids many common pitfalls caused by too much laziness and reduces the number of brain cycles the programmer has to spend thinking about evaluation order."
- Explicit imports: robustness against upstream changes.
- Most layout rules (80 cols, 4 spaces, tabs) get no reason; the guide often says "use your judgement".

## What transfers to general-purpose Lean
- Doc-comment all exported definitions; docs sufficient to use without reading the body.
- Explicit/qualified imports idea maps to `open ... in`, `open ... (names)`, `open ... hiding`, and avoiding blanket `open`.
- Strict-by-default-data is moot in Lean (strict language), but the spirit (state evaluation-order or representation commitments explicitly, `@[unbox]`/`@[specialize]` etc. only with reason) is a possible hook. (analysis)
- Warnings-as-errors for CI maps to `-DwarningAsError=true` / linter settings.
- Layout rules (alignment of constructors, hanging lambdas) are partly irrelevant; Lean has no formatter yet, so these remain open.

## Caveats and unverified items
- No license: use for ideas only, not quotation beyond fair-use snippets.
- Last updated 2015; GHC-era advice (`NOUNPACK`, GHC 7.4) is dated.
