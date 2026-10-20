# Google's Haskell Style Guide

| Field | Value |
|---|---|
| URL | https://google.github.io/styleguide/haskellguide.html (source: https://github.com/google/styleguide/blob/24cfcced577a82c4c455909515fa05682c8d2fa8/haskellguide.md) |
| Author / org | Google |
| Date / version | "Revision 1.01"; source file `haskellguide.md` last changed in `24cfcce` (2026-10-17, `gh-pages` branch) |
| License | CC BY 3.0 Unported (repo `LICENSE`; GitHub metadata says "Other") |
| Scope & audience | "Open-source projects developed by Google should conform to the requirements in this guide." |
| Kind | normative (for Google's open-source Haskell projects) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/haskell-google.md` (defuddle, 2026-10-20) |

## Summary
A short guide, about 3,800 words, covering structure (Haddock, exports, imports, pragmas, warnings), style, idioms, naming and formatting. It describes itself as "somewhat less prescriptive than most", because Haskell leaves "fewer arbitrary choices". It was found on 2026-10-20 while looking for Haskell counterparts to the Clojure citations. Several of its idioms match rules in this guide closely, especially those on partial functions, inline pragmas and warnings. Its layout rules (80 columns, 4-space indent, aligned arrows) don't transfer.

## Rules
Anchors are on the rendered page, `https://google.github.io/styleguide/haskellguide.html#<id>`.

- [Haddock](https://google.github.io/styleguide/haskellguide.html#haddock): "The module and all exported top-level elements should have Haddock." Very obvious declarations are exempt.
- [Pragmas](https://google.github.io/styleguide/haskellguide.html#pragmas): "`INLINE`, `INLINEABLE`, and similar pragmas should only be used when you've tested that they actually improve speed in cases that you care about." Language extensions beyond a listed set "should be avoided, as they may or may not be stable, increase the burden on readers to know them, and may force clients to use them."
- [Warnings](https://google.github.io/styleguide/haskellguide.html#warnings): "Code should compile cleanly with no warnings from GHC." It should compile with "both `-Wall` and `-Werror`".
- [Type declarations](https://google.github.io/styleguide/haskellguide.html#type-declarations): "All top level functions should have type declarations." The reason given: "type declarations provide good documentation". "Where reasonable, use the most polymorphic possible type."
- [Comments](https://google.github.io/styleguide/haskellguide.html#comments): Haddock should "explain the purpose of the function, not the implementation". Comments in the code should "explain any non-obvious reasoning for why something was done a particular way".
- [Partial functions](https://google.github.io/styleguide/haskellguide.html#partial-functions):
  - "Strenuously avoid partial functions from the `Prelude` and base libraries." They're acceptable where nearby logic makes the call certain to be safe.
  - "Do not write partial functions." The exception: "If a function internal to a module should never reach some case due to invariants maintained by the module, then it is acceptable to call `error` for those cases, and preferred to returning inaccurate results".
- [Point-free](https://google.github.io/styleguide/haskellguide.html#point-free): fine, "However, avoid over-using it", for example `f = (g .) . h`.
- [QuickCheck](https://google.github.io/styleguide/haskellguide.html#quickcheck): "Tests should be written with QuickCheck whenever possible." Use HUnit for special cases.
- [Abbreviations](https://google.github.io/styleguide/haskellguide.html#abbreviations): mixed case, as in `HttpResponse` and `IpBlock`, with an exception for established spellings.
- [Exports](https://google.github.io/styleguide/haskellguide.html#exports): every module has an explicit export list. Re-exporting from `Internal` modules is acceptable.
- [Parting words](https://google.github.io/styleguide/haskellguide.html#parting-words): "Use common sense and *BE CONSISTENT*." It adds: "look at the code around you and determine its style, and mirror it".

## Reasons given
Readers come first throughout: documentation, explicit types and fewer extensions all reduce "the burden on readers". It gives performance as the condition for pragmas, and test effectiveness for QuickCheck ("surprisingly effective").

## What transfers to general-purpose Lean
- Direct matches, now cited in the guide:
  - inline pragmas only after measurement;
  - no partial functions, with an exception for module invariants (Lean's `panic!` and `!`);
  - signatures on top-level functions;
  - docs on modules and exports;
  - warning-free builds;
  - point-free restraint;
  - property tests first;
  - comments that explain why.
- Conflicts:
  - it allows aligning `->` "when it helps readability";
  - it writes `IpBlock`, where Lean keeps acronyms of up to three letters in one case;
  - it allows primes for altered values (`fib'`), while this guide forbids them only in public API names;
  - its 80-column limit.

## Caveats and unverified items
- "Revision 1.01" is undated. The commit date is the last change to the source file, not necessarily to the content.
- QuickCheck, HUnit and Test Framework are Haskell libraries. Plausible is Lean's closest equivalent to QuickCheck.
