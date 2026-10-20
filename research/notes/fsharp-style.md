# F# style guide: principles, formatting, coding conventions

| Field | Value |
|---|---|
| URL | https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/ (index), `/formatting`, `/conventions` |
| Author / org | Microsoft (.NET docs team) with the F# community |
| Date / version | Source in dotnet/docs `docs/fsharp/style-guide/`: `conventions.md` last commit `e72182e511d875108edeb0ac8e98b2b6a102b512` (2025-05-21); `formatting.md` `8160867c5c96e15eeb0b997b1eca5b7783790ae4` (2026-08-27). Pages fetched 2026-10-17. |
| License | Documentation text: **CC BY 4.0** (dotnet/docs `LICENSE` begins "Attribution 4.0 International"); code samples: MIT (`LICENSE-CODE` exists, content not read, **unverified**). Attribution required. |
| Scope & audience | F# developers on .NET, "large codebases with a diverse group of programmers" |
| Kind | normative/community advice (vendor-published) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/fsharp-style.md`, `fsharp-formatting.md`, `fsharp-conventions.md` |

## Summary
The most principled of the general-purpose guides: five explicit principles from which "every piece of guidance ... stems", then separate pages for formatting (default settings of the Fantomas formatter), coding conventions (organizing code, error management, point-free, mutation, nulls) and component design (see `fsharp-component-design`). It takes firm positions on exceptions vs `Result`, partial application in public APIs, and name-length-insensitive formatting.

## Rules
Principles ([index](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/#five-principles-of-good-f-code)):
> Every piece of guidance in further articles stems from these five points.
> 1. Good F# code is succinct, expressive, and composable. 2. ... is interoperable. 3. ... makes use of object programming, not object orientation. 4. ... performs well without exposing mutation. 5. ... is toolable.
> Another is ... making sure you don't overdo it with a point-free style of programming, so that intermediate values can be inspected with a debugger. (paraphrase of principle 5)

Formatting ([formatting](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/formatting)):
> The Fantomas code formatter is the F# community standard tool for automatic code formatting. The default settings correspond to this style guide.
> **We recommend four spaces per indentation.** That said, indentation of programs is a subjective matter. Variations are OK, but the first rule you should follow is *consistency of indentation*.
> Seek to avoid indentation and alignment that is sensitive to naming ([Avoid formatting that is sensitive to name length](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/formatting#avoid-formatting-that-is-sensitive-to-name-length)): put the body on a new line rather than aligning to the end of `let myLongValueName =`.
> When using multiple lines, pipeline `|>` operators should go underneath the expressions they operate on.

Organization ([conventions](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/conventions#organizing-code)): "Prefer namespaces at the top level"; "Carefully apply [<AutoOpen>]"; "Use [<RequireQualifiedAccess>] whenever names could conflict"; "Sort open statements topologically".

Error management ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/conventions#error-management)):
> Represent error cases and illegal state in types intrinsic to your domain (discriminated union for withdrawal result).
> Use exceptions when errors cannot be represented with types.
> The `failwith` and `failwithf` functions should generally be avoided because they raise the base `Exception` type, not a specific exception.
> Do not use monadic error handling to replace exceptions: "Exceptions are often seen as taboo in the pure functional paradigm. ... In general, write code on the assumption that most things aren't pure or total, to minimize unpleasant surprises."
Cited advantages of exceptions: detailed diagnostics; understood by runtime and other languages; "reduce significant boilerplate". Warns against nested `Result<Result<MyType, string>, string list>` and string-typed errors, and against `try ... with _ -> None` which discards the cause.

Point-free ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/conventions#partial-application-and-point-free-programming)):
> point-free programming is not a virtue in and of itself, and can add a significant cognitive barrier for people who are not immersed in the style.
> Do not use partial application and currying in public APIs ... Curried functions do not label their arguments. This has tooling implications.
> Consider partial application as a technique to reduce internal boilerplate.

Mutation: "Wrap mutable code in immutable interfaces"; "Prefer let mutable to ref". Nulls: "Avoid the use of the AllowNullLiteral attribute", "If you check for null inputs, raise exceptions at first opportunity". Types: "Prefer composition over inheritance"; "Avoid using Type Abbreviations to represent your domain" ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/conventions#consider-type-abbreviations-to-shorten-signatures)).

## Reasons given
Every rule traces back to the five principles; many have short explicit reasons ("hard to debug", "tooling implications", "cognitive barrier"). Formatting rules cite diffs/name-length sensitivity; the guide admits indentation "is a subjective matter".

## What transfers to general-purpose Lean
- Principles-first structure, and the claim that each rule must derive from a principle.
- The formatting rule "avoid formatting that is sensitive to name length" (same reasoning as Elm, Rust block indent): applicable to Lean `:=` bodies, `match` alignment, `where` structures.
- Exceptions vs `Result`: Lean has both (`Except`, `IO` errors, `panic!`); F# says use types for domain errors and exceptions for the rest, and not to wrap everything in `Result`. This is the sharpest cross-language split to put in the guide's error-handling topic.
- Point-free: toolability argument (intermediate values inspectable) applies to Lean's `#eval`, infoview, and goal display.
- Namespace/`open` policy: `RequireQualifiedAccess`/`AutoOpen` analogues are Lean `open` and `export`; "sort opens" parallels import ordering.
- Mutation behind immutable interfaces: Lean's `ST`/`StateM`, `Array` in-place update.

## Caveats and unverified items
- Heavily .NET-interop oriented. Date of last edit differs per page; the index page date not checked.
