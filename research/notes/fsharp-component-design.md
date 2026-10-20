# F# component design guidelines

| Field | Value |
|---|---|
| URL | https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines |
| Author / org | Microsoft; originally the F# team's "F# Component Design Guidelines" |
| Date / version | Source `docs/fsharp/style-guide/component-design-guidelines.md` in dotnet/docs, last commit `5452826ad2021ef434c11870669d4fc6e2884e89` (2025-01-22); fetched 2026-10-17 |
| License | Documentation: CC BY 4.0 (dotnet/docs `LICENSE`); code samples MIT per `LICENSE-CODE` (not read, **unverified**) |
| Scope & audience | Library authors: F#-facing libraries and libraries for other .NET languages |
| Kind | normative / community advice |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/fsharp-component-design.md` |

## Summary
The API-design counterpart to the F# style pages: naming tables, how to organize modules vs types, when to hide representations, how to treat exceptions, units, operators and type abbreviations. Half of it concerns interop with C#/VB and does not transfer. The F#-facing half is a compact checklist of public-API design decisions in a language with modules and curried functions, which is close to Lean.

## Rules
General ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines#general-guidelines)):
> Add XML documentation comments to your code ... on public APIs.
> Consider using explicit signature files (.fsi) for stable library and component APIs ... Signature files add friction to changing the public API, by requiring changes to be made in both the implementation and signature files.

Naming ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines#naming-conventions)): PascalCase for types, union tags, methods, properties; camelCase for parameters; a table by construct.
> Boolean properties generally use Is and Can and should be affirmative, as in IsEndOfFile, not IsNotEndOfFile.
> Avoid abbreviations: "This guideline is sometimes ignored for functional programming; for example, `List.iter` uses an abbreviation for 'iterate'."
> Use PascalCase for generic parameter names in public APIs ... names like `T`, `U`, `T1`, `T2` ... (but not for example, `TKey`).
> camelCase is used for public functions that are designed to be used unqualified ... and for the "standard collection functions" (for example, List.map). In both these cases, the function names act much like keywords in the language.

Type and module design ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines#object-type-and-module-design)):
> Use a module to group functions that act on collections ... If you include such a module, follow the standard naming conventions for functions found in FSharp.Core.
> Consider using RequireQualifiedAccess and carefully apply AutoOpen attributes ... Requiring qualified access can greatly increase the long-term maintainability and evolvability of a library.
> Overuse of `[<AutoOpen>]` leads to polluted namespaces
> Hide the representations of record and union types if the design of these types is likely to evolve.
> Avoid the use of implementation inheritance for extensibility.
> Use discriminated unions instead of class hierarchies for tree-structured data.
> Avoid defining custom symbolic operators ... it is best to publish your functionality as named functions and members, and additionally expose operators for this functionality only if the notational benefits outweigh the documentation and cognitive cost of having them.
> Carefully use type abbreviations ... / Avoid type abbreviations for public types whose members and properties should be intrinsic to what the type represents.
> Avoid using member constraints to simulate type classes and duck typing.

Signatures ([section](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines#function-and-member-signatures)): "Use tuples for return values when returning a small number of multiple unrelated values"; for .NET-facing code: "Avoid the use of currying of parameters. Instead, use .NET calling conventions" and "Use the TryGetValue pattern instead of returning F# option values" (interop-driven).

Errors: defers to the conventions page ([Exceptions](https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines#exceptions)).

## Reasons given
Mostly short rationale per rule: interop expectations, evolvability (hidden representations, qualified access), cognitive cost (operators), friction as a feature (signature files).

## What transfers to general-purpose Lean
- Public-API checklist items: hide representation if it may evolve (Lean `structure` with `private mk`, `opaque`, `@[irreducible]`, structure-eta concerns); qualified access by default with `open` opt-in; limit custom notation (`infixl`, `notation`, `macro`) to cases where benefit beats documentation cost.
- Library functions for a collection type live in a namespace with standard names (`List.map`, `Array.foldl`), echoing Lean's `Foo.bar` namespace convention.
- Signature files = no direct Lean equivalent; closest are `private`/`protected`, `namespace` exports, `.lean` interface modules; a guide topic on "what is public".
- The .NET interop half (delegates, null handling, CLIEvent) is irrelevant, though the FFI half of Lean (`@[extern]`) has an analogue.

## Caveats and unverified items
- Appendix with end-to-end example (L748+) not read. Windows/.NET-specific rules ignored.
