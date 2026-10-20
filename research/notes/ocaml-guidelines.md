# OCaml Programming Guidelines (ocaml.org)

| Field | Value |
|---|---|
| URL | https://ocaml.org/docs/guidelines |
| Author / org | OCaml.org docs; text derives from Pierre Weis and collaborators' French guidelines, translated by Ruchira Datta ([Credits](https://ocaml.org/docs/guidelines#credits)) |
| Date / version | Fetched 2026-10-17; no publication date on the page (**unverified**) |
| License | Content: **CC BY-SA 4.0** (ocaml/ocaml.org `LICENSE`: "Content is released under CC BY-SA 4.0"; code examples within content: UNLICENSE). ShareAlike: adapted text must carry the same licence. |
| Scope & audience | OCaml programmers, "consensus among veteran OCaml programmers" |
| Kind | community advice |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/ocaml-guidelines.md` |

## Summary
A long guide (general, programming, development, formatting, indentation) that says formatting can now be delegated to OCamlFormat and concentrates on what tools do not automate. Several rules come with an explicit "Justification" blockquote, a format worth copying. Key themes: readability first, no abbreviations for globals, exhaustive matches without catch-alls, avoid `hd`/`tl`, never `try ... with _`, prefer immutable data.

## Rules
Intro ([section](https://ocaml.org/docs/guidelines#ocaml-programming-guidelines)):
> This is a set of reasonable guidelines for writing OCaml programs that reflect the consensus among veteran OCaml programmers.
> OCaml source code can be formatted automatically with OCamlFormat, so you don't have to worry about formatting it by hand. You can speed up code review by just focusing on the important parts. Nevertheless, some best practices are not automated, so they're documented in this article.

Readability ([Be Simple and Readable](https://ocaml.org/docs/guidelines#be-simple-and-readable)):
> **Writing programs law**: A program is written once, modified ten times, and read 100 times. So it's beneficial to simplify its writing, always keep future modifications in mind, and never jeopardize readability.

Identifiers ([How to Choose Identifiers](https://ocaml.org/docs/guidelines#how-to-choose-identifiers)):
> Global identifiers (including the names of functions) can be long because it's important to understand what purpose they serve far from their definition.
> Separate words by underscores: (int_of_string, not intOfString)
> Always give the same name to function arguments which have the same meaning
> Local identifiers can be brief and should be reused from one function to another
> Avoid using identifiers whose appearance can lead to confusion, such as `l` or `O`

Pattern matching ([Compiler Warnings](https://ocaml.org/docs/guidelines#compiler-warnings)):
> Compiler warnings are meant to prevent potential errors, which is why you absolutely must heed them and correct your programs if compiling them produces such warnings.
> For nonexhaustive pattern-matching, you must complete the corresponding pattern-matching construct without adding a default case "catch-all", such as `| _ -> ...`, but rather with an explicit constructor list not examined by the rest of the construct
> **Justification**: ... the addition of a new constructor to the datatype matched will produce an alert anew, which will allow the programmer to add a clause corresponding to the new construct.

Partial accessors ([The hd and tl Functions](https://ocaml.org/docs/guidelines#the-hd-and-tl-functions)):
> Don't use the `hd` and `tl` functions, but rather pattern-match the list argument explicitly.
> **Justification**: This is just as brief as and much clearer than using `hd` and `tl`, which must be protected by `try... with...` to catch the exception that might be raised by these functions.

Exceptions ([Exceptions](https://ocaml.org/docs/guidelines#exceptions)):
> Handling all exceptions by `try ... with _ ->` is usually reserved for the program's main function. If you must catch every exception in order to maintain an algorithm's invariant, be careful to name the exception and re-raise it after having reset the invariant.
> **Justification**: `try ... with _ ->` silently catches all exceptions, even those which have nothing to do with the computation at hand (for example, an interruption will be captured and the computation will continue anyway!).
> every search function that fails should raise the predefined exception `Not_found`. (paraphrase of the same section: reuse predefined exceptions)

Mutables ([When to Use Mutables](https://ocaml.org/docs/guidelines#when-to-use-mutables)):
> Mutable values are useful and sometimes indispensable for simple and clear programming. Nevertheless, you must use them with discernment because OCaml's normal data structures are immutable. They are preferred for the clarity and safety of programming they allow.

Other sections (not extracted): comments and assertions, module subdivision and `open` policy, loops, iterators, optimisation, classes vs modules, readability "dangers", and a long formatting/indentation part.

## Reasons given
Rules are often followed by "Justification" blocks (pattern matching, `hd`/`tl`, `try with _`). Other rules (underscores, abbreviations) give a language-specific reason: capitalised words are reserved for constructors and modules, so camel case cannot mark word boundaries.

## What transfers to general-purpose Lean
- The "Justification" blockquote as a rule-format option alongside bbatsov-style rationale text.
- No catch-all `_` when the type may grow: relevant to Lean `match` on inductives, and to `deriving` of cases. Lean's missing-cases error already forces exhaustiveness, but wildcard use is a style choice.
- Avoid partial list/array accessors where pattern matching is as short: parallels `head!`, `get!`, `xs[i]!`.
- Catch-all exception handling restricted to the top-level: parallels catching `IO.Error` broadly.
- Global names descriptive, local names short and reused.
- Formatting parts are OCaml/indentation specific and mostly irrelevant.

## Caveats and unverified items
- No date; the page may have been revised since its Weis-era origin. OCaml-specific ("warnings", `Not_found`).
