# Lean standard library vision, README and Grove (`doc/std/`)

| Field | Value |
|---|---|
| URL | https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/vision.md |
| Author / org | Lean FRO stdlib maintainers: Henrik Böving, Markus Himmel (community contact), Kim Morrison, Paul Reichert, Sofia Rodrigues (as listed in the file) |
| Date / version | lean4 commit `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` (2026-10-17) |
| License | Apache 2.0 (lean4 `LICENSE`) |
| Scope & audience | Stdlib contributors and prospective contributors; also states what the stdlib is for |
| Kind | descriptive (goals) plus process |
| Lean version | Lean 4 |
| Raw copy | `vendor/pages/lean-official/lean-core-vision.md` |

## Summary
`vision.md` states the stdlib's guiding principles, an outline of its contents, which parts will be verified, and a call for contributions. It is not a style guide, but it is the only official statement of design goals for the library whose code style FRO prescribes. `README.md` in the directory is a three-line index to `vision.md`, `style.md`, `naming.md`. `grove/` is not a style document: it holds data files for Grove, a QA tool.

## Rules (design goals, not code rules)
Link base: `https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/vision.md`
> The standard library is a public API that contains the components listed in the standard library outline below. Not all public APIs in the Lean distribution are part of the standard library, and the standard library does not correspond to a certain directory within the Lean source repository (like `Std`).

Guiding principles ([L25-L32](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/vision.md#L25)):
> * Provide comprehensive, verified building blocks for real-world software.
> * Build a public API of the highest quality with excellent internal consistency.
> * Carefully optimize components that may be used in performance-critical software.
> * Ensure smooth adoption and maintenance for users.
> * Offer excellent documentation, example projects, and guides.
> * Provide a reliable and extensible basis that libraries for software development, software verification and mathematics can build on.

Verification scope:
> The material covered in the first three sections (core types and operations, language constructs and libraries) will be verified, with the exception of floating point numbers and the parts of the libraries that interface with the operating system

Outline sections: core types (basic types, numerics, containers, strings and formatting); language constructs (ranges and iterators; comparison, ordering, hashing; basic monad infrastructure); libraries (random numbers, dates and times); OS abstractions (concurrency, async I/O, FFI helpers, environment/file system/processes, locales).

Contribution process:
> All code in the standard library is expected to strictly adhere to the [standard library coding conventions](./style.md).

> The Lean standard library has a very precise scope and it has very high quality standards, so at the moment we are mostly interested in contributions that expand upon existing material rather than introducing novel concepts.

> PRs are much more likely to be merged if they are preceded by an RFC or if you discussed your planned contribution with a member of the standard library maintainer team.

### `README.md` and `grove/`
- `README.md`: "The user-facing documentation of the standard library is part of the Lean Language Reference" and lists vision, style guide, naming conventions.
- `grove/README.md` (one line): "This directory contains the Grove data files for the standard library" (title "Standard library QA"). Grove is https://github.com/TwoFX/grove. The FRO roadmap mentions "manual tracking of global consistency properties using our QA tool Grove" ([roadmap y4-1](https://lean-lang.org/fro/roadmap/y4-1/)). Not a style source.

## Reasons given
- Stated rationale for strictness: the library is a "public API of the highest quality with excellent internal consistency" and must be maintainable for downstream users.
- The conventions themselves are not justified here.

## What transfers to general-purpose Lean
- The principles (consistency, verified building blocks, performance care, smooth adoption) show what FRO values in library code; the verification-by-default stance is stdlib-specific.
- "Public API" vs implementation distinction and the `Internal` convention are relevant to library authors.
- Useful as evidence that the FRO treats stdlib style as stdlib-only policy, not as language-wide policy.

## Caveats and unverified items
- Maintainer list is a point-in-time snapshot.
- The outline lists planned components; not all exist (unverified).
