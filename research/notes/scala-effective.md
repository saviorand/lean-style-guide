# Effective Scala (Twitter)

| Field | Value |
|---|---|
| URL | https://twitter.github.io/effectivescala/ |
| Author / org | Marius Eriksen, Twitter, Inc. |
| Date / version | Repo twitter/effectivescala `31dadf21eb1bb8bd7cdf376edddbcb9119e9e440`, last commit 2021-10-08; text copyright 2012. Fetched 2026-10-17. |
| License | **CC BY 3.0 Unported** ("Copyright 2012 Twitter, Inc. Licensed under the CC-BY 3.0", repo README; `LICENSE` file is the CC BY 3.0 legal text). Attribution only; adaptation allowed. |
| Scope & audience | Twitter engineers; "we assume the reader is familiar with the language" |
| Kind | community advice (company-internal practice published) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/scala-effective.md` |

## Summary
An opinionated usage guide for a large, multi-paradigm language, organized by feature (formatting, types, collections, concurrency, control structures, functional programming, OO, error handling). The introduction is a statement of values: readability above brevity, use simple features, avoid esoteric type-system machinery, be aware of trade-offs. Highly relevant to Lean as another language with powerful, abusable features (implicits ~ instances/coercions, type-level programming).

## Rules
Values ([Introduction](https://twitter.github.io/effectivescala/#Introduction)):
> Scala provides many tools that enable succinct expression. Less typing is less reading, and less reading is often faster reading, and thus brevity enhances clarity. However brevity is a blunt tool that can also deliver the opposite effect: After correctness, think always of the reader.
> Above all, *program in Scala*. You are not writing Java, nor Haskell, nor Python
> Always favor readability; write generic code but not at the expensive of clarity; take advantage of simple language features that afford great power but avoid the esoteric ones (especially in the type system). Above all, be always aware of the trade offs you make.

Naming ([Formatting-Naming](https://twitter.github.io/effectivescala/#Formatting-Naming)):
> Use short names for small scopes ... Use longer names for larger scopes. External APIs should have longer and explanatory names that confer meaning. `Future.collect` not `Future.all`.
> Use common abbreviations but eschew esoteric ones
> Don't rebind names for different uses

Types ([Return type annotations](https://twitter.github.io/effectivescala/#Types%20and%20Generics-Return%20type%20annotations)):
> While Scala allows these to be omitted, such annotations provide good documentation: this is especially important for public methods. Where a method is not exposed and its return type obvious, omit them.

Options and errors ([Options](https://twitter.github.io/effectivescala/#Functional%20programming-Options), [Error handling](https://twitter.github.io/effectivescala/#Error%20handling)):
> The `Option` type ... provides a safe alternative to the use of `null`, and should be used instead of null whenever possible.
> Scala provides an exception facility, but do not use it for commonplace errors, when the programmer must handle errors properly for correctness. Instead, encode such errors explicitly: using `Option` or `com.twitter.util.Try` are good, idiomatic choices, as they harness the type system to ensure that the user is properly considering error handling.
> `trait Repository[Key, Value] { def get(key: Key): Option[Value] }` ... "This interface makes it obvious that the repository may not contain every key, and that the programmer must handle missing keys."
> some exceptions are *fatal* and should never be caught; the code `catch { case _ => ... }` is almost always wrong ... use the `com.twitter.util.NonFatal` extractor ([Handling exceptions](https://twitter.github.io/effectivescala/#Error%20handling-Handling%20exceptions))

Contracts ([require and assert](https://twitter.github.io/effectivescala/#Control%20structures-require%20and%20assert)):
> `assert` is used for *invariants* that the code assumes ... Whereas `require` is used to express API contracts

Comments: Scaladoc with a specific asterisk-aligned style ([Comments](https://twitter.github.io/effectivescala/#Formatting-Comments)). Pattern matching: "Use pattern matching directly in function definitions whenever applicable". Partial functions: section describing `PartialFunction` as a first-class construct (Scala `PartialFunction` is a different notion from Lean partiality).

## Reasons given
The guide gives short prose reasons per section, and says up front that it is a living document of "best practices" with stable core ideas. The `Option` vs exception rule is justified by type-system enforcement ("statically enforces that `username` must be checked").

## What transfers to general-purpose Lean
- The value statement ("after correctness, think always of the reader"; avoid esoteric type-level features; "program in X, not Y") translates directly.
- "Errors that callers must handle go in the type; exceptions are for the rest": Lean's `Option`/`Except` vs `panic!`/`throw`. Contrasts with Databricks (see `scala-databricks`) and F# (see `fsharp-style`) which lean the other way for APIs.
- Short names in small scopes, long in large ones; public return types annotated.
- `require` vs `assert` distinction: public-contract check vs internal invariant; Lean analogue is `assert!`/`panic!` vs hypotheses in argument types.

## Caveats and unverified items
- Mostly Twitter-specific (Futures, Offer/Broker, Java collections) and 2012-era; Scala 2.
- Anchor URLs are inferred from the page's own table of contents (`#Section-Subsection`), not tested in a browser.
