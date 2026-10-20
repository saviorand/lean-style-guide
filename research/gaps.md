# Remaining gaps

Status on 2026-10-20, when research was declared sufficient for a first draft. Each item names the note or file it belongs to. The rule for anything below: check it while drafting if a rule depends on it, otherwise leave it.

## Closed on 2026-10-20

- **Testing (Q21):** mechanisms, FRO practice, community adoption and a 34-repo sample of test drivers ([testing-practice](notes/testing-practice.md)).
- **Program code from many authors:**
  - The directory-based survey mixed authors, while Lake and Std.Http each come mostly from a single author. [author-survey.md](author-survey.md) splits 395k lines of FRO program code into nine author columns.
  - It separates shared conventions from choices that vary by author. For example, `@[inline]` density and Std.Http's 98.5% docstring coverage turned out to vary by author rather than reflect FRO convention.
  - Script: `scripts/authors.py`. Survey columns can now be file lists (`scripts/leanlex.py`).
- **Lean Reference, unread sections:**
  - the module-system guidance for library authors;
  - the `IO`/`Task`/`Async` rule for concurrency;
  - instance agreement (`BEq`/`Hashable`);
  - notation output (unexpanders);
  - FFI stability;
  - `#guard_msgs` as a test driver.

  All in [lean-reference](notes/lean-reference.md).
- **Macros:** the metaprogramming book gives two rules of thumb with reasons ([mpbook](notes/mpbook.md)). The cookbook has nothing on macro style but covers application topics ([mprecipes](notes/mprecipes.md)).

## Skipped by decision (would not change a rule)

- **TPIL:** a tutorial on how the language works, with no style positions ([tpil](notes/tpil.md)). For proofs about programs, the guide draws on core-style's tactic section, Std's `Lemmas.lean` practice, FPIL's final chapters, CSLib and Mathlib's proof linters (Q0b).
- **FRO blog posts after 2024, roadmaps Y1–Y3, MIL, the FAQ.** At most, skim titles for formatter, module-system or Std.Http news.
- **Other community formatters**, and the rest of leanfmt's `design.md`.
- **Jane Street's prose page, elm-format's "no config" quote, PureScript, Rocq naming**, QED at Large in full, the Iris SHA, Isabelle/ACL2/Liquid Haskell, Harper's "Boolean blindness", Wlaschin's book, and Brady beyond the free extracts.
- **The testing sections of the Ruby and Clojure guides, and the Rust per-construct pages.**
- **Lean core housekeeping:** whether `AGENTS.md` is binding, what "the line length limit" refers to, the history of `doc/std`, and lean-lang.org licences. Paraphrase rather than quote those pages.
- **Per-section `Q#` evidence counts** in open-questions.md.
- **The survey's "Not measured" layout items** (structure-instance and `if`/`else` layout, operator position, orphaned parentheses). The layout chapter should stay short until the formatter ships (Q5).

## Do while drafting, not before

- **Quotes:** no second pass has checked the agents' quotes against the sources. Check each quote when it is used, through the permalinks in the notes.
- **The two untested FPIL claims** (`JSON.asString` termination; dot notation through `abbrev`): check them in Lean if a rule relies on them ([fpil](notes/fpil.md#caveats-and-unverified-items)).
- **Good/bad pairs (Q0c):**
  - Write each pair and compile it.
  - Look for outside evidence only for contested rules. Mathlib's linter tests in `MathlibTest/` are an in-repo source of flagged code.
  - Leave mining PR review comments for v2.
- **Q0b:** settle how much proof style the guide includes. The suggestion is one short chapter on proofs about programs.

## Still open (decide, or research only if a chapter needs it)

- **Chapters missing from [proposed-toc.md](proposed-toc.md).** For each, decide whether it gets a thin chapter or is out of scope for v1:
  - **Macros and notation.** The material is in hand: [mpbook](notes/mpbook.md), the Reference's notation-output rule, and core-style's RFC and scoped-syntax rules.
  - **Dependencies, toolchains and releases:** pinning, `require` and tags, `warningAsError` in libraries breaking downstream builds, Reservoir. No note covers this. The only evidence is the Lake README and one application's lakefile (`lean-realworld-example-app`).
  - **Concurrency and FFI.** The Reference's rules are in [lean-reference](notes/lean-reference.md#concurrency-read-2026-10-20). Resource handling (`withFile`, `finally`) still has no Lean source.
- **Testing details (Q21):** a rule for property tests, and whether to mention Errata before it is released on its own.
- **Author survey limits:**
  - The `Authors:` header names the creator, not later editors.
  - Most of the code of authors A, C and G is compiler code running in `MetaM`, so their error-handling numbers do not describe application code.
  - Verso and doc-gen4 are measured only through the author columns, not as an "applications" column of their own.
- **The "wild" column:** still three libraries and no applications.
