# Lean FRO pages, blog and roadmap

| Field | Value |
|---|---|
| URL | https://lean-lang.org/fro/ ; https://lean-lang.org/blog/ ; https://lean-lang.org/fro/roadmap/y4-1/ ; https://lean-lang.org/blog/2024-1-11-recursive-definitions-in-lean ; https://lean-lang.org/blog/2024-12-16-introducing-the-lean-language-reference |
| Author / org | Lean FRO; "Recursive definitions in Lean" by Joachim Breitner (named on the page) |
| Date / version | FRO page undated; roadmap Y4 part 1 covers "September 2026 to February 2027"; recursion post dated 2024-01-11 (edited Feb 2024 for Lean 4.6 `termination_by` syntax); Language Reference post 2024-12-16. Fetched 2026-10-17 |
| License | none stated on pages (**unverified**) |
| Scope & audience | General Lean users and FRO funders/community |
| Kind | descriptive |
| Lean version | Lean 4 (posts reference 4.6 to 4.14; roadmap is current) |
| Raw copy | `vendor/pages/lean-official/fro-fro.md`, `fro-blog.md`, `fro-fro-roadmap-y4-1.md`, `fro-blog-2024-1-11-recursive-definitions-in-lean.md`, `fro-blog-2024-12-16-introducing-the-lean-language-reference.md` |

## Summary
Searching the FRO site for style guidance found almost none. The FRO page lists mission areas (usability, documentation, proof automation). The blog index as served (defuddle) stops at December 2024 and lists release posts, "Recursive definitions in Lean", "Functional induction", and the Reference announcement; none is a style post. Two items matter for this project: Joachim Breitner's recursion post is the only FRO text that compares structural recursion, well-founded recursion and `partial`/`unsafe`; and the Year 4 roadmap announces a code formatter, new linters and stdlib quality metrics. Stdlib design goals are in `lean-core-vision`, not on the blog.

## Rules / statements
### Termination (Breitner, 2024-01-11)
Post sets out three options: "writing *structurally recursive* functions; proving that your functions terminate, using *well-founded recursion*; not worrying about recursion and mark your functions as *partial* or even *unsafe*" ([post](https://lean-lang.org/blog/2024-1-11-recursive-definitions-in-lean)).
> In general, if you plan to prove theorems about your functions, a structurally recursive definition is most pleasant to work with, for two reasons: [induction follows the definition; the defining equation holds definitionally]

> That is because the *type* of a `partial` function must be inhabited, or else allowing proofs to merely *mention* the function causes havoc

On `unsafe`: "Lean will, however, prevent you from using unsafe definitions in theorems and proofs, so that soundness is preserved." Use `#print fib` and look for `brecOn` to check whether structural recursion was used. These are described options, not ranked recommendations beyond the quoted preference for theorem-proving contexts.

### Roadmap Y4-1 (Sept 2026 to Feb 2027) ([page](https://lean-lang.org/fro/roadmap/y4-1/))
- "We will ship the code formatter and refine it continuously in communication with the community." (Tooling) No formatter rules are given; once shipped it would be a de facto layout authority (observation).
- Stdlib: "we will introduce infrastructure to ensure the quality of material nearing stabilization: additional linters, quantitative quality metrics to observe library quality over time, and manual tracking of global consistency properties using our QA tool Grove." Also "providing improved alternative APIs for the legacy I/O modules."
- Verification: "we will complete the new do notation, including first-class support for intrinsic verification".
- Mentions AI agents (lean-beam, Hex, Palomar); not style relevant.

### Reference announcement (2024-12-16)
Describes the Reference as "a comprehensive, concise, and accurate description of Lean", built with Verso, "includes tests that help us keep it up to date".

## Reasons given
Breitner gives soundness reasons for `partial` (inhabited types) and proof-ergonomics reasons for structural recursion. Roadmap items give goals (stability, quality), not code rules.

## What transfers to general-purpose Lean
- A termination ladder (structural, then well-founded, then `partial`) with proof-ergonomics as the criterion appears here and in FPIL (`fpil`) and the Reference (`lean-reference`); none says what a non-proving application author should choose.
- The formatter is the most important pending development: rules depending on layout should be checked against it when released.
- No FRO blog post on program design (naming, errors, Array vs List, tests) was found.

## Caveats and unverified items
- The blog index fetched was a stale snapshot ending Dec 2024 (links go through web.archive.org); newer posts (2025-2026) were not enumerated. Not read: the "Functional induction" post, "Year 1 in Review", release posts, Leo de Moura's blog (leodemoura.github.io/blog), and the older roadmaps (y1-y3, y4-1 is the only one fetched; y5/y6 URLs return 404).
- lean-lang.org/fro/roadmap/y1 to y3 might contain stdlib design goals (unfetched leads).
