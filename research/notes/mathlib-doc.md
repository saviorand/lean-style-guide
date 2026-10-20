# Mathlib documentation standards

| Field | Value |
|---|---|
| URL | https://leanprover-community.github.io/contribute/doc.html |
| Author / org | Lean community / Mathlib maintainers (`templates/contribute/doc.md`) |
| Date / version | Served 2026-10-17; source last changed 2026-09-03, [`31f5fe4`](https://github.com/leanprover-community/leanprover-community.github.io/blob/31f5fe4e58912d3a9260419e6372c9d2e94a116d/templates/contribute/doc.md) |
| License | MIT (repo metadata) |
| Scope & audience | Mathlib pull requests ("All pull requests must meet the following documentation standards") |
| Kind | normative (Mathlib) |
| Lean version | Lean 4 (though the doc-string example for `docBlame` is a `#lint` command; the Reference "Linting" section is partly from Lean 3 times, **unverified**) |
| Raw copy | `vendor/pages/community/mathlib-doc.md` |

## Summary
Requires a header comment plus module docstring, "Implementation notes", "References" and "Tags" sections in module docs, doc strings on every definition and major theorem, Markdown/LaTeX conventions, sectioning comments, citation format, and American/British English allowances. It is oriented to mathematical content: doc strings "should convey the mathematical meaning of the definition" and "are allowed to lie slightly about the actual implementation".

## Rules
> Every definition and major theorem is required to have a doc string. (Doc strings on lemmas are also encouraged, particularly if the lemma has any mathematical content or might be useful in another file.) ... If a doc string is a complete sentence, then it should end in a period. Named theorems ... should be bold faced. ([Doc strings](https://leanprover-community.github.io/contribute/doc.html#doc-strings))

> Doc strings should convey the mathematical meaning of the definition. They are allowed to lie slightly about the actual implementation.

> Tactics should have a docstring that matches the Lean documentation style guide ... The docstring should start with a full sentence that has the tactic as the subject. ([Tactic documentation](https://leanprover-community.github.io/contribute/doc.html#tactic-documentation))

> We generally put references to Lean declarations or variables in between backticks. Writing the fully-qualified name ... will turn the name into a link on our online docs. ... Raw URLs should be enclosed in angle brackets `<...>` ([LaTeX and Markdown](https://leanprover-community.github.io/contribute/doc.html#latex-and-markdown))

> Third-level headers `###` should be used for titles inside sectioning comments. If the comment is more than one line long, the delimiters `/-!` and `-/` should appear on their own lines. ([Sectioning comments](https://leanprover-community.github.io/contribute/doc.html#sectioning-comments))

Linters named: `docBlame`, `docBlameThm`, `tacticDocs` (see `notes/mathlib-linters.md`). Module docstring layout and the "Implementation notes" section are also specified.

## Reasons given
Mostly tooling: names in backticks and fully qualified become links in doc-gen4 output; angle-bracket URLs so they are clickable; sectioning comments appear in generated docs. No stated reason for "may lie slightly" beyond keeping the mathematical meaning primary.

## What transfers to general-purpose Lean
- Transfers: doc string on every public definition; backtick/qualified-name references; `/-! -/` module docs with title and summary; sectioning with `###`; tactic docstring shape (defers to Lean core).
- Does not transfer: "convey the mathematical meaning ... may lie slightly about implementation" (for programs, docs must describe behaviour, complexity, panics); LaTeX/MathJax; bibliography/Tags; references to mathematical databases.
- Missing for programs: documenting preconditions, panic behaviour (`!`), `partial`, performance, examples/`#eval`, and when a docstring should be imperative or indicative mood. (Mood: Lean core's `doc/std/style.md` line 189 says "Documentation comments must be written in the indicative mood. Use American orthography."; Zulip thread [style guide for comments, 2024-05-15](https://leanprover-community.github.io/archive/stream/270676-lean4/topic/style.20guide.20for.20comments.3F.html) shows the community asking for this to be written down.)

## Caveats and unverified items
- Section "Language" (British spelling allowed in docs, American in names) was read via the naming page cross-reference only.
- Lean 3 remnants possible in the `#lint` examples.
