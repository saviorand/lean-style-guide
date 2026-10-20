# Type-Driven Development with Idris (Brady, Manning 2017)

| Field | Value |
|---|---|
| URL | https://www.manning.com/books/type-driven-development-with-idris |
| Author / org | Edwin Brady (Manning Publications) |
| Date / version | March 2017, ISBN 9781617293023, 480 pp. (Idris 1; updates for Idris 2 are in the Idris 2 docs, `docs/source/typedd/typedd.rst`) |
| License | Book: commercial, all rights reserved (publisher page; no licence stated). Free livebook extract quoted briefly under fair use. Interview post: no licence found. |
| Scope & audience | Programmers learning dependent types |
| Kind | community advice (book) |
| Lean version | n/a (Idris 1) |
| Raw copy | `vendor/pages/proof-assistants/tddi-chapter-1.md`, `tddi-chapter-3.md`, `tddi-about.md`, `manning-tddi.md`, `brady-serokell.md` |

## Summary
Only public material was read: the publisher page, the free livebook extracts of chapters 1 and 3 (a few paragraphs each), and an interview with Brady. That is enough to capture the method ("type, define, refine"), the claim that types complement tests, and the stance that the type is a plan that may be revised. The book's detailed design advice (state machines, safe printf, and the like) was **not read**.

## Rules
The method:
> In type-driven development, we follow the process of "type, define, refine." [...] ***Type—*** Either write a type to begin the process, or inspect the type of a hole to decide how to continue the process. ***Define—*** Create the structure of a function definition either by creating an outline of a definition or breaking it down into smaller components. ***Refine—*** Improve an existing definition either by filling in a hole or making its type more precise.
(`vendor/pages/proof-assistants/tddi-chapter-3.md`; online at https://livebook.manning.com/book/type-driven-development-with-idris/chapter-3)

> We put the *type* first, treating it as a plan for a program, and use the compiler and type checker as our assistant [...]
([chapter 1](https://livebook.manning.com/book/type-driven-development-with-idris/chapter-1))

On types versus tests:
> unlike tests, which can usually only be used to show the *presence* of errors, types (used appropriately) can show the *absence* of errors. But although types *reduce* the need for tests, they rarely eliminate it entirely.
([chapter 1](https://livebook.manning.com/book/type-driven-development-with-idris/chapter-1))

Revising the type (Brady, interview):
> We in type-driven development put the type first, but that doesn't necessarily mean the type is the final type. As we write the program, we're going to learn more about the problem, we'll refine the type a bit more [...] maybe we decide that the type needs to be more precise, maybe we decide it needs to be less precise, but all of that needs to be done with tool support.
([Serokell interview](https://serokell.io/blog/from-whitespace-to-idris))

On proof burden (Brady, interview):
> the decisions we make, the design choices we make are all about getting to a point where you've actually got no excuse – just to prove the properties you care about of your program because it's easier than not doing so.
(same interview)

## Reasons given
Types as a construction tool give guidance during development; "the more expressive the type is that we give up front, the more confidence we can have" in the result (chapter 1, truncated in the extract; remainder **unverified**).

## What transfers to general-purpose Lean
- "Type, define, refine" maps onto Lean workflow: signature first, `sorry`/`_` holes as the "define" skeleton, then fill. A guide could recommend always committing a type-correct skeleton and writing signatures before bodies.
- The "types do not replace tests" position supports a guide that keeps both tests and proofs and says which is for what.
- The explicit point that the type may be made less precise guards against over-indexing everything.

## Caveats and unverified items
- Book content beyond the extracts is unverified. The Idris 2 docs say the book "will mostly work in Idris 2" with changes (typedd.rst), so some examples are Idris 1 specific.
- Do not use unofficial PDF copies that turn up in search results; none were read.
- Unverified leads: Brady's JFP 2013 paper "Idris, a general-purpose dependently typed programming language: Design and implementation" (design rationale); the TDD-with-Idris chapters on state machines and "type-level functions".
