# Cornell CS 3110 OCaml Style Guide

| Field | Value |
|---|---|
| URL | https://www.cs.cornell.edu/courses/cs3110/2018sp/handouts/style.html |
| Author / org | Cornell University CS 3110 course staff |
| Date / version | Spring 2018 handout (other years exist: 2009-2017). The current textbook site has no style chapter at the URLs tried (404). |
| License | none stated (default copyright). Looked in: page text and footer of the saved copy. |
| Scope & audience | Undergraduate functional-programming students; also grading criteria |
| Kind | normative for the course; community advice for OCaml |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/ocaml-cs3110.md` |

## Summary
A teaching style guide with the explicit priority "Readability is Priority #1". Formatting rules (80 columns, no tabs, 2 or 4 spaces) are brief; most content is on patterns to avoid: needless `if`/`match` on booleans, rewrapped functions, `List.hd/tl/nth`, projections instead of patterns, duplicate computation. Examples are Bad/Good code pairs.

## Rules
> The most important goal is for your code to be readable by other humans. All the guidelines below are in service of that goal. ([Readability](https://www.cs.cornell.edu/courses/cs3110/2018sp/handouts/style.html#readability))
> **80 Column Limit.** A good rule to follow is to keep nearly all lines of code under 80 columns.
> **No Tab Characters.** ... we generally recommend 2 spaces per indent, but 4 is also fine.
> **Avoid Useless Comments.** Avoid comments that merely repeat the code they reference or state the obvious. Comments should state the invariants, the non-obvious, or any references that have more information about the code.
> **Naming Conventions.** Most importantly, be consistent within your own code base, and to the extent possible, with any libraries that you use. ... snake_case for values and types; CamelCase for constructors and modules.
> **Type Synonyms.** You are encouraged to use type synonyms to convey intent.
> **Mutable Variables.** Mutable variables are at odds with the philosophy of functional programming and should be used sparingly. In particular, global mutable variables cause many problems.
> **Pipeline.** A deeply nested chain of function applications such as f4 (f3 (f2 (f1 x))) should be rewritten with the pipeline operator as x |> f1 |> f2 |> f3 |> f4.
> **Inexhaustive Pattern Matches.** ... you should take seriously.
> **Use Pattern Matching in Function Arguments.** / **Avoid Unnecessary Projections.**
> **Combine nested match Expressions.**
> **Avoid the use of List.hd, List.tl, and List.nth.** These functions raise exceptions and are the cause of many coding errors. It is better to avoid them altogether.
> **Avoid breaking expressions over multiple lines.** If a tuple consists of more than two or three elements, you should consider using a record instead of a tuple.
> **Don't Rewrite Library Functions.** / **Misusing if Expressions** (do not use `if` to produce a Boolean) / **Don't Rewrap Functions** (pass `f`, not `fun x -> f x`) / **Avoid Computing Values Twice.**

Section anchors are not published; headings in the order: File Submission, File Format, Comments, Naming and Declarations, Indenting, Parentheses, Pattern Matching, Factoring, Verbosity.

## Reasons given
Brief, mostly one-line ("The width of a tab is not uniform across all editors"; "causes many coding errors"). Bad/Good pairs do the explaining.

## What transfers to general-purpose Lean
- The "Verbosity" list (boolean `if`, `match` on Bool, eta-expanded wrappers, recomputation) is language-neutral and maps to Lean idioms (`if h : ...`, `fun x => f x`, `let` sharing).
- "Records not 3+-tuples" maps to `structure` vs product types.
- Tuple-pattern combination of nested matches; `|>` pipeline (Lean has `|>`, `<|`, `∘`).
- "Consistent within your codebase, and with libraries you use" mirrors the bbatsov consistency note.

## Caveats and unverified items
- Course handout, 2018; teaching-oriented and strict about "code must compile". No licence. Only the 2018sp version was read.
