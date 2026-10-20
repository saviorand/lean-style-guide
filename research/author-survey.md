# FRO program code by author (cross-author survey)

This survey asks whether a pattern in FRO program code is a convention shared by many authors or a choice that varies between them. [stdlib-survey.md](stdlib-survey.md) measures by directory, which mixes authors. Here the same measurements are split by each file's first author. Authors appear as letters, because the point is to compare conventions, not people.

## Provenance and method

- **Corpus:** lean4 `3a685e6` (`src/Init`, `src/Std`, `src/Lean`, `src/lake/Lake`), Verso `76c3f3c` (`src`), doc-gen4 `0656b7e` and lean4-cli `34d2eff`. All are shallow clones in `vendor/repos/`.
- **Program files:** a file counts if it has at least 3 defs and theorems are at most 25% of its defs plus theorems. That gives 1,558 files and 395,526 nonblank lines.
- **Attribution:** each file goes to the first name in its `Authors:` header, which records who created the file, not who edits it now. The creation year comes from the copyright line. The clones are shallow, so there is no `git blame`.
- **FRO membership:** the team page, fetched 2026-10-20 to `vendor/pages/lean-official/fro-team.md`.
- **Labels:** authors are lettered by their share of program lines, A being the largest.
- **Columns:**
  - A24 and Aold: author A's files from 2024 on, and from before 2024.
  - B to G: the next six FRO authors by program lines, one column each.
  - Others: nine further FRO authors, pooled.

  The table below shows which directories each author's code is in.
- **Reproduce:**

  ```sh
  cd vendor/repos
  python3 ../../scripts/authors.py
  python3 ../../scripts/authors.py --write-columns
  python3 ../../scripts/survey.py --cols A24,Aold,B,C,D,E,F,G,Others \
    baseline naming lambda helpers format do errors termination data attrs visibility docs
  ```

  `--write-columns` writes `scripts/author-columns.json`, and the survey picks it up as extra columns.
- **Caveats:**
  - The lexer is regex-based, as in stdlib-survey.md.
  - Most of the code of authors A, C and G is elaborator or compiler code running in `MetaM`. Their error-handling numbers (`throwError`, `unreachable!`, `[i]!`) reflect that domain, not application code.
  - The authors closest to application code are B (mostly Verso), D (`Std.Http`, `Std.Time`, `Std.Async`) and E (Lake).

## Who wrote the program code

Program files: 1558, nonblank lines: 395526

| first author | FRO | files | nonblank | % | defs | thms | years (min–median–max) | main dirs (by lines) |
|---|---|---|---|---|---|---|---|---|
| A | yes | 606 | 163734 | 41.4 | 14093 | 172 | 2016–2022–2026 | `lean4/src/Lean/Meta` 67507, `lean4/src/Lean/Elab` 36492, `lean4/src/Lean/Compiler` 11636 |
| B | yes | 172 | 54317 | 13.7 | 3836 | 22 | 2023–2025–2026 | `verso/src` 41534, `lean4/src/Lean/DocString` 5852, `lean4/src/Lean/Elab` 4296 |
| C | yes | 95 | 25503 | 6.4 | 2093 | 11 | 2021–2025–2026 | `lean4/src/Lean/Compiler` 7615, `lean4/src/Lean/Meta` 6464, `lean4/src/Init/Data` 3742 |
| D | yes | 88 | 22668 | 5.7 | 2414 | 33 | 2024–2025–2026 | `lean4/src/Std/Http` 10501, `lean4/src/Std/Time` 9053, `lean4/src/Std/Async` 1339 |
| E | yes | 115 | 19267 | 4.9 | 2543 | 15 | 2021–2022–2025 | `lean4/src/lake/Lake` 19019, `lean4/src/Lean/LoadDynlib.lean` 101, `lean4/src/Lean/Elab` 93 |
| F | yes | 45 | 14689 | 3.7 | 1306 | 0 | 2017–2021–2026 | `lean4/src/Lean/PrettyPrinter` 3546, `lean4/src/Lean/Server` 1838, `lean4/src/lake/Lake` 1616 |
| G | yes | 48 | 9269 | 2.3 | 604 | 5 | 2025–2026–2026 | `lean4/src/Lean/Elab` 8733, `lean4/src/Std/Do` 185, `lean4/src/Init/Internal` 121 |
| H | yes | 41 | 8945 | 2.3 | 1539 | 61 | 2024–2025–2026 | `lean4/src/Std/Data` 6368, `lean4/src/Init/Data` 2340, `lean4/src/Lean/Elab` 83 |
| I | yes | 26 | 8083 | 2.0 | 467 | 0 | 2020–2021–2026 | `lean4/src/Lean/Data` 3880, `lean4/src/Lean/Server` 2448, `lean4/src/Lean/Elab` 1009 |
| J | yes | 49 | 8062 | 2.0 | 622 | 40 | 2025–2025–2026 | `lean4/src/Init/Data` 5817, `lean4/src/Std/Data` 1382, `lean4/src/Lean/PostprocessTraces` 502 |
| K | yes | 29 | 6763 | 1.7 | 509 | 0 | 2020–2020–2025 | `lean4/src/Lean/Server` 4538, `lean4/src/Lean/Data` 2080, `lean4/src/Lean/Util` 93 |
| L | yes | 26 | 6447 | 1.6 | 295 | 0 | 2023–2025–2026 | `lean4/src/Lean/Meta` 3284, `lean4/src/Lean/Elab` 2908, `lean4/src/Lean/DefEqAttrib.lean` 170 |
| M |  | 29 | 5929 | 1.5 | 557 | 1 | 2017–2021–2022 | `lean4/src/lake/Lake` 2715, `lean4/src/Lean/Meta` 1137, `lean4/src/Lean/Data` 1058 |
| N | yes | 25 | 5318 | 1.3 | 329 | 0 | 2021–2024–2026 | `lean4/src/Lean/Elab` 2182, `lean4/src/Lean/Meta` 1071, `lean4/src/Lean/LibrarySuggestions` 834 |
| O | yes | 23 | 4519 | 1.1 | 268 | 0 | 2023–2024–2026 | `lean4/src/Lean/Elab` 2660, `lean4/src/Lean/Meta` 1385, `lean4/src/Lean/PrettyPrinter` 339 |
| P |  | 23 | 3801 | 1.0 | 212 | 0 | 2025–2026–2026 | `lean4/src/Lean/Meta` 1531, `lean4/src/Lean/Linter` 1109, `lean4/src/Lean/Elab` 642 |
| (none) |  | 11 | 2768 | 0.7 | 275 | 0 | ? | `lean4-cli/Cli` 1604, `doc-gen4/DocGen4` 956, `verso/src` 208 |
| Q |  | 15 | 2739 | 0.7 | 222 | 7 | 2014–2022–2026 | `lean4/src/Lean/Elab` 905, `lean4/src/lake/Lake` 743, `lean4/src/Init/Data` 445 |
| R |  | 8 | 2466 | 0.6 | 515 | 17 | 2025–2025–2025 | `lean4/src/Std/Data` 2381, `lean4/src/Init/GrindInstances` 56, `lean4/src/Init/Grind` 29 |
| S |  | 6 | 2021 | 0.5 | 203 | 31 | 2023–2024–2024 | `lean4/src/Lean/Meta` 1118, `lean4/src/Init/Data` 823, `lean4/src/Lean/Elab` 80 |
| T |  | 4 | 1936 | 0.5 | 131 | 0 | 2019–2021–2021 | `lean4/src/Lean/Meta` 1302, `lean4/src/Lean/PrettyPrinter` 529, `lean4/src/Init/Data` 66 |
| U |  | 16 | 1874 | 0.5 | 137 | 0 | 2022–2022–2022 | `lean4/src/Lean/Elab` 1227, `lean4/src/Lean/Data` 253, `lean4/src/Lean/Linter` 245 |
| V |  | 2 | 1843 | 0.5 | 275 | 0 | 2022–2022–2022 | `lean4/src/Lean/Compiler` 1843 |
| W |  | 1 | 1552 | 0.4 | 172 | 0 | 2017–2017–2017 | `lean4/src/Init/System` 1552 |
| X |  | 7 | 1481 | 0.4 | 99 | 0 | 2021–2021–2022 | `lean4/src/Lean/Meta` 688, `lean4/src/Lean/Elab` 424, `lean4/src/Std/Internal` 369 |
| Y | yes | 2 | 1157 | 0.3 | 78 | 0 | 2021–2022–2022 | `lean4/src/Lean/Server` 784, `lean4/src/Lean/Data` 373 |
| Z |  | 7 | 1122 | 0.3 | 77 | 0 | 2022–2022–2022 | `lean4/src/Lean/Widget` 605, `lean4/src/Lean/Meta` 228, `lean4/src/Lean/Server` 146 |
| AA | yes | 4 | 921 | 0.2 | 19 | 0 | 2023–2025–2025 | `verso/src` 681, `lean4/src/Lean/IdentifierSuggestion.lean` 146, `lean4/src/Lean/Elab` 94 |
| AB |  | 4 | 857 | 0.2 | 61 | 0 | 2024–2025–2026 | `lean4/src/Lean/Compiler` 857 |
| AC |  | 3 | 760 | 0.2 | 20 | 0 | 2025–2025–2025 | `lean4/src/Lean/Meta` 488, `lean4/src/Lean/ErrorExplanation.lean` 151, `lean4/src/Lean/Elab` 121 |

## Consistent across authors

These hold in all nine columns, or in all but one (the exception is named).

- **Lambdas:** `fun x =>` in 93.6–99.4% of lambdas; `↦` 0–0.2%, `λ` about 0. Unicode `←`, almost never `<-` (at most 0.15 per thousand lines).
- **Indentation:**
  - 88–98% of indent increases are +2, and bodies after `:=`/`by`/`do` are +2 in 97.8–99.7%.
  - Match arms sit at the `match` column in 96.9–99.7%.
  - Split headers continue at +4 in seven of nine columns (91–99%). Column E (Lake) uses +2 (92%) and starts 174 header lines with `:`; column F is mixed (69% +4).
- **Line length:** p95 is 84–100 for every author, and every author has 1–5% of lines over 100. A strict 100-column limit, as Mathlib lints, is stricter than FRO practice.
- **Helpers:**
  - `where` helpers outnumber `let rec` in eight of nine columns (column D uses them equally), and `go` is the most common helper name everywhere.
  - Author A's code moved from `let rec` (1.64 per thousand lines, with `loop` the top name) before 2024 to `where` (6.24, against 0.99 for `let rec`) from 2024, with `go` used 139 times as a `where` helper.
- **Instances:** anonymous. Named instances are 0–14% in eight columns, 39% in column G.
- **Termination:**
  - Every author uses `partial` in program code, on 1.3–8.0% of defs.
  - `termination_by` appears at most 0.34 per thousand lines, `partial_fixpoint` never, fuel rarely.
- **Failure:** `panic!` is rare everywhere (0.1–1.3 per thousand lines). `Option` appears at a similar rate in every column (12.5–17 per thousand lines).

## Author-dependent (no FRO convention)

- **`@[inline]`:**
  - per thousand lines: B 0.13, G 1.2, A24 2.2, F 3.7, Aold 8.4, C 15.6, Others 23, D 34, E 36;
  - `@[specialize]` is at most 1.4 per thousand lines everywhere.
  - So the high density in `Std.Http` (column D) is not a convention shared across FRO code.
- **Docstring coverage of public defs:** 34–57% in eight columns, 98.5% in column D.
- **Docstring first word:** columns A, C, D and Others most often lead with a verb ("Returns", "Creates", "Converts"). Columns B, E, F and G more often lead with a noun phrase ("The", "A"). Both forms are FRO practice (Q19).
- **`return` vs `pure`:** `return` outnumbers `pure` in every column, by a ratio from 1.2 (B) to 10 (A24). FPIL's code prefers `pure`.
- **let-else (`let some x ← … | …`):** common in A24 (8.8 per thousand lines, up from 1.9 in Aold), C (4.4) and G (4.1); rare in B (0.17), D (0.13) and E (0.36).
- **Visibility:**
  - `private` on 0.2% (E) to 26% (A24) of declarations.
  - Column E marks `public` declaration by declaration (80.6%), and B does so for 22.9%. The other columns use `public section`.
- **Indexing in IO-facing code:** columns D and E prefer `[i]?` and almost never use `[i]!` (0.05–0.22 per thousand lines). Compiler code uses `[i]!` at 4–7.
- **Errors in IO-facing code:**
  - Columns B, D and E use `throw` with `IO.userError` and `Except` (2.2–4.0 per thousand lines).
  - `MonadExcept` appears at most 0.34 per thousand lines in any column, and only in compiler code; columns B, D and E use it 0–1 times. FPIL's advice to write against `MonadExcept` is not FRO practice.
- **`unreachable!`:** 1.7–2.6 per thousand lines in compiler code, about 0 in columns B, D and E.

## Full tables

The survey output follows unchanged, apart from relabelled columns and headings moved down one level. These sections print counts only, with no example locations; to spot-check a count, run the `ex_*` helpers in `survey.py` on the same columns.

### baseline
| col | files | lines | nonblank | `module` files | decls parsed |
|---|---|---|---|---|---|
| A24 | 239 | 56405 | 50648 | 239 | 4304 |
| Aold | 367 | 130103 | 113086 | 367 | 11178 |
| B | 172 | 62324 | 54317 | 154 | 4317 |
| C | 95 | 29298 | 25503 | 81 | 2303 |
| D | 88 | 27407 | 22668 | 88 | 2614 |
| E | 115 | 22967 | 19267 | 115 | 2725 |
| F | 45 | 16659 | 14689 | 45 | 1432 |
| G | 48 | 10365 | 9269 | 48 | 669 |
| Others | 225 | 58791 | 50215 | 222 | 4739 |

### 1 naming: case convention of the last name component, by declaration kind

### def
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 3412 | 0.4% | 89.7% | 9.3% | 0.1% | 0.0% | 0.0% | 0.5% |
| Aold | 8533 | 0.6% | 84.4% | 14.7% | 0.3% | 0.0% | 0.0% | 0.0% |
| B | 3024 | 1.0% | 77.4% | 20.5% | 0.7% | 0.0% | 0.0% | 0.3% |
| C | 1567 | 0.8% | 79.5% | 19.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 1750 | 2.2% | 73.4% | 24.3% | 0.1% | 0.0% | 0.0% | 0.0% |
| E | 1760 | 0.7% | 79.3% | 19.9% | 0.0% | 0.0% | 0.0% | 0.1% |
| F | 1097 | 0.5% | 76.9% | 22.4% | 0.1% | 0.0% | 0.0% | 0.0% |
| G | 502 | 1.4% | 89.0% | 9.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 3207 | 0.7% | 76.9% | 22.3% | 0.0% | 0.1% | 0.0% | 0.1% |

### abbrev
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 299 | 38.8% | 52.2% | 9.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Aold | 420 | 59.5% | 28.6% | 11.7% | 0.2% | 0.0% | 0.0% | 0.0% |
| B | 97 | 81.4% | 10.3% | 8.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 96 | 71.9% | 22.9% | 5.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 25 | 92.0% | 0.0% | 8.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 282 | 47.2% | 32.3% | 20.2% | 0.0% | 0.0% | 0.0% | 0.4% |
| F | 37 | 89.2% | 5.4% | 5.4% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 22 | 72.7% | 13.6% | 13.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 95 | 82.1% | 13.7% | 4.2% | 0.0% | 0.0% | 0.0% | 0.0% |

### theorem
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 7 | 0.0% | 14.3% | 14.3% | 0.0% | 71.4% | 0.0% | 0.0% |
| Aold | 165 | 0.0% | 2.4% | 6.7% | 58.2% | 32.7% | 0.0% | 0.0% |
| B | 22 | 0.0% | 18.2% | 4.5% | 22.7% | 54.5% | 0.0% | 0.0% |
| C | 11 | 0.0% | 0.0% | 45.5% | 9.1% | 45.5% | 0.0% | 0.0% |
| D | 33 | 0.0% | 0.0% | 9.1% | 39.4% | 51.5% | 0.0% | 0.0% |
| E | 15 | 0.0% | 0.0% | 0.0% | 20.0% | 80.0% | 0.0% | 0.0% |
| F | 0 | – | – | – | – | – | – | – |
| G | 5 | 0.0% | 0.0% | 0.0% | 80.0% | 0.0% | 0.0% | 20.0% |
| Others | 101 | 0.0% | 15.8% | 13.9% | 31.7% | 38.6% | 0.0% | 0.0% |

### instance
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 0 | – | – | – | – | – | – | – |
| Aold | 54 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 17 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 10 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 2 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 5 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| F | 1 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 28 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 118 | 0.0% | 99.2% | 0.0% | 0.8% | 0.0% | 0.0% | 0.0% |

### structure
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 235 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Aold | 518 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 346 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 153 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 111 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 89 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| F | 95 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 42 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 385 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### class
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 13 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Aold | 123 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 24 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 5 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 9 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 41 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| F | 12 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 3 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 34 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### class inductive
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 0 | – | – | – | – | – | – | – |
| Aold | 1 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 0 | – | – | – | – | – | – | – |
| C | 0 | – | – | – | – | – | – | – |
| D | 0 | – | – | – | – | – | – | – |
| E | 0 | – | – | – | – | – | – | – |
| F | 0 | – | – | – | – | – | – | – |
| G | 0 | – | – | – | – | – | – | – |
| Others | 0 | – | – | – | – | – | – | – |

### inductive
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 77 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Aold | 169 | 99.4% | 0.0% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 86 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 41 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 47 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 29 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| F | 19 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 15 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 89 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### opaque
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 46 | 10.9% | 73.9% | 15.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| Aold | 256 | 3.5% | 57.4% | 39.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 34 | 0.0% | 97.1% | 2.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 114 | 3.5% | 46.5% | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 30 | 10.0% | 40.0% | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 16 | 37.5% | 37.5% | 18.8% | 0.0% | 0.0% | 0.0% | 6.2% |
| F | 18 | 5.6% | 66.7% | 27.8% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 9 | 22.2% | 77.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 5 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### axiom
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 0 | – | – | – | – | – | – | – |
| Aold | 11 | 0.0% | 81.8% | 18.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 0 | – | – | – | – | – | – | – |
| C | 0 | – | – | – | – | – | – | – |
| D | 0 | – | – | – | – | – | – | – |
| E | 1 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| F | 0 | – | – | – | – | – | – | – |
| G | 0 | – | – | – | – | – | – | – |
| Others | 0 | – | – | – | – | – | – | – |

### namespace
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 897 | 99.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| Aold | 1069 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| B | 503 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| C | 390 | 99.7% | 0.0% | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% |
| D | 421 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| E | 212 | 98.1% | 0.0% | 1.4% | 0.0% | 0.0% | 0.0% | 0.5% |
| F | 129 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| G | 180 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Others | 706 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### suffixes and primes (last component; defs = def/abbrev/opaque, thms = theorem)

#### defs
| suffix (count, % of kind) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| ends `'` (primed) | 74 (2.0%) | 96 (1.0%) | 37 (1.2%) | 17 (1.0%) | 14 (0.8%) | 19 (0.9%) | 10 (0.9%) | 2 (0.4%) | 25 (0.8%) |
| ends `?` | 343 (9.1%) | 548 (6.0%) | 66 (2.1%) | 34 (1.9%) | 60 (3.3%) | 185 (9.0%) | 41 (3.6%) | 59 (11.1%) | 293 (8.9%) |
| ends `!` | 7 (0.2%) | 112 (1.2%) | 8 (0.3%) | 4 (0.2%) | 35 (1.9%) | 2 (0.1%) | 3 (0.3%) | 0 (0.0%) | 171 (5.2%) |
| ends lower+`D` (getD-style) | 0 (0.0%) | 28 (0.3%) | 3 (0.1%) | 0 (0.0%) | 5 (0.3%) | 8 (0.4%) | 2 (0.2%) | 0 (0.0%) | 73 (2.2%) |
| ends `Impl` | 24 (0.6%) | 64 (0.7%) | 8 (0.3%) | 6 (0.3%) | 3 (0.2%) | 4 (0.2%) | 3 (0.3%) | 5 (0.9%) | 8 (0.2%) |
| ends `Aux` | 8 (0.2%) | 178 (1.9%) | 7 (0.2%) | 5 (0.3%) | 0 (0.0%) | 2 (0.1%) | 9 (0.8%) | 1 (0.2%) | 11 (0.3%) |
| ends `Core` | 79 (2.1%) | 145 (1.6%) | 4 (0.1%) | 3 (0.2%) | 1 (0.1%) | 33 (1.6%) | 16 (1.4%) | 3 (0.6%) | 16 (0.5%) |
| ends `Unsafe`/`unsafe` | 2 (0.1%) | 41 (0.4%) | 28 (0.9%) | 2 (0.1%) | 0 (0.0%) | 0 (0.0%) | 4 (0.3%) | 2 (0.4%) | 4 (0.1%) |
| ends `TR` | 0 (0.0%) | 2 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends lower+`M` (monadic) | 52 (1.4%) | 189 (2.1%) | 27 (0.9%) | 58 (3.3%) | 2 (0.1%) | 34 (1.7%) | 24 (2.1%) | 9 (1.7%) | 108 (3.3%) |
| is `go` | 3 (0.1%) | 3 (0.0%) | 1 (0.0%) | 1 (0.1%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| is `loop` | 1 (0.0%) | 3 (0.0%) | 0 (0.0%) | 2 (0.1%) | 0 (0.0%) | 1 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| is `aux` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `_eq` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `_iff` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `_def` | 1 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| contains `_of_` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `_spec` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

#### thms
| suffix (count, % of kind) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| ends `'` (primed) | 0 (0.0%) | 4 (2.4%) | 2 (9.1%) | 0 (0.0%) | 0 (0.0%) | 1 (6.7%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `?` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 1 (1.0%) |
| ends `!` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends lower+`D` (getD-style) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `Impl` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `Aux` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `Core` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `Unsafe`/`unsafe` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `TR` | 0 (0.0%) | 1 (0.6%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends lower+`M` (monadic) | 0 (0.0%) | 1 (0.6%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| is `go` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| is `loop` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| is `aux` | 0 (0.0%) | 1 (0.6%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |
| ends `_eq` | 0 (0.0%) | 23 (13.9%) | 0 (0.0%) | 2 (18.2%) | 4 (12.1%) | 0 (0.0%) | 0 (–) | 1 (20.0%) | 7 (6.9%) |
| ends `_iff` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 14 (13.9%) |
| ends `_def` | 0 (0.0%) | 1 (0.6%) | 0 (0.0%) | 0 (0.0%) | 7 (21.2%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 4 (4.0%) |
| contains `_of_` | 0 (0.0%) | 32 (19.4%) | 0 (0.0%) | 0 (0.0%) | 3 (9.1%) | 2 (13.3%) | 0 (–) | 0 (0.0%) | 7 (6.9%) |
| ends `_spec` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (–) | 0 (0.0%) | 0 (0.0%) |

### `?`/`!`/`D` families among defs (qualified names)
| col | X? defs | X! defs | XD defs | X? with X! | X? with XD | X? with plain X | X! without X? | all four |
|---|---|---|---|---|---|---|---|---|
| A24 | 342 | 7 | 0 | 0 | 0 | 29 | 7 | 0 |
| Aold | 548 | 112 | 28 | 19 | 12 | 55 | 93 | 8 |
| B | 66 | 8 | 3 | 2 | 1 | 6 | 6 | 0 |
| C | 34 | 4 | 0 | 2 | 0 | 6 | 2 | 0 |
| D | 60 | 35 | 5 | 27 | 2 | 9 | 8 | 2 |
| E | 185 | 2 | 8 | 0 | 7 | 36 | 2 | 0 |
| F | 41 | 3 | 2 | 1 | 0 | 7 | 2 | 0 |
| G | 59 | 0 | 0 | 0 | 0 | 3 | 0 | 0 |
| Others | 293 | 171 | 73 | 137 | 73 | 101 | 34 | 55 |

A24 complete families (sample): 

Aold complete families (sample): Std.DHashMap.Internal.AssocList.get, Std.DHashMap.Internal.AssocList.getCast, Std.DHashMap.Internal.AssocList.getEntry, Std.DHashMap.Internal.AssocList.getKey, Std.DHashMap.Internal.Raw₀.Const.get, Std.DHashMap.Internal.Raw₀.get, Std.DHashMap.Internal.Raw₀.getEntry, Std.DHashMap.Internal.Raw₀.getKey

### 2 lambda syntax
| col | `fun` (per k) | `λ` (per k) | binder ends `=>` (% of fun+λ) | binder ends `↦` | `fun |` alts | `·` not line-initial (≈ sections) (per k) | `·` line-initial (focus dot) (per k) |
|---|---|---|---|---|---|---|---|
| A24 | 1569 (30.98) | 0 (0.00) | 1559 (99.4%) | 0 (0.0%) | 10 (0.6%) | 527 (10.41) | 0 (0.00) |
| Aold | 4009 (35.45) | 1 (0.01) | 3924 (97.9%) | 0 (0.0%) | 78 (1.9%) | 937 (8.29) | 2 (0.02) |
| B | 1793 (33.01) | 0 (0.00) | 1711 (95.4%) | 0 (0.0%) | 82 (4.6%) | 1247 (22.96) | 0 (0.00) |
| C | 686 (26.90) | 0 (0.00) | 642 (93.6%) | 0 (0.0%) | 44 (6.4%) | 345 (13.53) | 26 (1.02) |
| D | 241 (10.63) | 1 (0.04) | 229 (94.6%) | 0 (0.0%) | 13 (5.4%) | 103 (4.54) | 59 (2.60) |
| E | 479 (24.86) | 0 (0.00) | 464 (96.9%) | 0 (0.0%) | 15 (3.1%) | 427 (22.16) | 9 (0.47) |
| F | 582 (39.62) | 0 (0.00) | 560 (96.2%) | 1 (0.2%) | 21 (3.6%) | 244 (16.61) | 0 (0.00) |
| G | 345 (37.22) | 0 (0.00) | 336 (97.4%) | 0 (0.0%) | 5 (1.4%) | 132 (14.24) | 0 (0.00) |
| Others | 1532 (30.51) | 0 (0.00) | 1480 (96.6%) | 0 (0.0%) | 52 (3.4%) | 607 (12.09) | 146 (2.91) |

### 3 local helpers
| col | `where` helpers (per k) | `let rec` (per k) | private defs | top-level `X.go`/`X.loop`/`X.aux` defs | `go` share | `loop` share | `aux` share |
|---|---|---|---|---|---|---|---|
| A24 | 316 (6.24) | 50 (0.99) | 1065 (28.3% of defs) | 0 | 45.4% | 2.5% | 0.0% |
| Aold | 581 (5.14) | 186 (1.64) | 1432 (15.6% of defs) | 1 | 21.6% | 13.3% | 0.1% |
| B | 507 (9.33) | 21 (0.39) | 590 (18.7% of defs) | 0 | 6.8% | 2.1% | 0.2% |
| C | 312 (12.23) | 9 (0.35) | 88 (5.0% of defs) | 0 | 24.3% | 1.9% | 0.0% |
| D | 18 (0.79) | 18 (0.79) | 339 (18.8% of defs) | 0 | 25.0% | 25.0% | 0.0% |
| E | 69 (3.58) | 5 (0.26) | 6 (0.3% of defs) | 0 | 14.9% | 5.4% | 0.0% |
| F | 99 (6.74) | 9 (0.61) | 79 (6.9% of defs) | 0 | 14.8% | 6.5% | 0.0% |
| G | 29 (3.13) | 8 (0.86) | 61 (11.4% of defs) | 0 | 16.2% | 8.1% | 0.0% |
| Others | 249 (4.96) | 13 (0.26) | 226 (6.8% of defs) | 0 | 27.1% | 1.1% | 0.0% |

A24 where-helper names top: [('go', 139), ('visit', 9), ('goEq', 4), ('loop', 3), ('main', 3), ('goVar', 3), ('go?', 3), ('getOriginal?', 3)]; let rec top: [('go', 27), ('loop', 6), ('visit', 5), ('simp', 1), ('mkValueLoop', 1), ('mkAppBVars', 1)]

Aold where-helper names top: [('go', 140), ('loop', 22), ('visit', 21), ('fn', 7), ('mkNat', 7), ('visitApp', 5), ('process', 5), ('mkAlts', 3)]; let rec top: [('loop', 80), ('go', 26), ('visit', 17), ('parse', 8), ('fold', 6), ('map', 4)]

B where-helper names top: [('go', 30), ('}', 9), ('text', 7), ('decorateOut', 4), ('reportFail', 4), ('opener', 3), ('"', 3), (']', 3)]; let rec top: [('loop', 8), ('go', 6), ('attempt', 5), ('check', 1), ('aux', 1)]

C where-helper names top: [('go', 76), ('goFVar', 4), ('phase', 4), ('start', 3), ('install', 3), ('mkAuxDecl', 2), ('mkSlowPath', 2), ('mkFastPath', 2)]; let rec top: [('loop', 4), ('go', 2), ('scanDir', 1), ('lowerNonObjectFields', 1), ('intersperseDefault', 1)]

D where-helper names top: [('username', 1), ('password', 1), ('asterisk', 1), ('origin', 1), ('absoluteFromScheme', 1), ('absoluteHttp', 1), ('absolute', 1), ('authority', 1)]; let rec top: [('loop', 9), ('go', 9)]

E where-helper names top: [('go', 11), ('invalidEndpointConfig', 2), ('logError', 2), ('fn', 2), ('replay', 1), ('doBuild', 1), ('setMTime', 1), ('parseTarget', 1)]; let rec top: [('loop', 4), ('takeRest', 1)]

F where-helper names top: [('go', 15), ('modify', 2), ('mkAlts', 2), ('loop', 2), ('nameComps', 2), ('postCallback', 2), ('compute', 2), ('collectDecl', 1)]; let rec top: [('loop', 5), ('visit', 1), ('insertEmpty', 1), ('go', 1), ('visitLambda', 1)]

G where-helper names top: [('go', 6), ('stM', 3), ('elabDoMatchExprNoMeta', 1), ('mkUnknownMonadResult', 1), ('mutVarNames', 1), ('getσ', 1), ('collectHyps', 1), ('label', 1)]; let rec top: [('loop', 2), ('$decls', 1), ('elabMatch', 1), ('extract?', 1), ('$_', 1), ('collectDomains', 1)]

Others where-helper names top: [('go', 66), ('doRealize', 4), ('throwError', 4), ('loop', 3), ('getIndType', 2), ('useCtor', 2), ('extraDeps', 2), ('visit', 2)]; let rec top: [('go', 5), ('visit', 2), ("go'", 1), ('highlightReturn?', 1), ('popStack', 1), ('popRanges', 1)]

### 4 formatting
### line length (code points, nonblank raw lines incl. comments)
| col | p50 | p95 | p99 | max | >100 | >120 | lines with tab | trailing ws |
|---|---|---|---|---|---|---|---|---|
| A24 | 39 | 98 | 126 | 278 | 2082 (4.1%) | 684 (1.4%) | 0 | 0 |
| Aold | 41 | 100 | 130 | 374 | 5517 (4.9%) | 1874 (1.7%) | 0 | 0 |
| B | 37 | 98 | 126 | 436 | 1776 (3.3%) | 694 (1.3%) | 0 | 0 |
| C | 35 | 95 | 107 | 303 | 439 (1.7%) | 124 (0.5%) | 0 | 0 |
| D | 29 | 90 | 106 | 188 | 398 (1.8%) | 77 (0.3%) | 0 | 0 |
| E | 39 | 84 | 101 | 158 | 196 (1.0%) | 18 (0.1%) | 0 | 0 |
| F | 42 | 99 | 121 | 258 | 599 (4.1%) | 152 (1.0%) | 0 | 0 |
| G | 46 | 99 | 116 | 242 | 317 (3.4%) | 72 (0.8%) | 0 | 0 |
| Others | 37 | 95 | 111 | 295 | 1025 (2.0%) | 269 (0.5%) | 0 | 2 |

### indentation (code lines; deltas = increase from previous code line)
| col | odd indent | +2 | +4 | other increase |
|---|---|---|---|---|
| A24 | 0.4% | 97.5% | 1.8% | 0.6% |
| Aold | 0.9% | 95.7% | 2.7% | 1.6% |
| B | 0.5% | 94.7% | 4.3% | 1.0% |
| C | 0.2% | 94.7% | 4.8% | 0.5% |
| D | 0.3% | 96.5% | 2.8% | 0.6% |
| E | 0.3% | 97.9% | 0.7% | 1.4% |
| F | 0.3% | 95.4% | 3.2% | 1.4% |
| G | 0.3% | 92.1% | 5.4% | 2.5% |
| Others | 0.2% | 88.1% | 10.7% | 1.3% |

### `match ... with` followed by `|` arms on the next line
| col | match starts line: n | `|` = match col | `|` +2 | match mid-line: n | `|` = line indent | `|` = line indent+2 | `|` under `match` | `match … with |` inline | arms with padded `=>` (aligned) |
|---|---|---|---|---|---|---|---|---|---|
| A24 | 587 | 99.3% | 0.7% | 130 | 10.8% | 87.7% | 0.8% | 2 | 351/3845 (9.1%) |
| Aold | 1948 | 99.3% | 0.6% | 264 | 6.8% | 88.6% | 0.4% | 26 | 2617/8873 (29.5%) |
| B | 722 | 99.2% | 0.8% | 77 | 5.2% | 88.3% | 2.6% | 10 | 8/4103 (0.2%) |
| C | 351 | 99.4% | 0.3% | 6 | 66.7% | 33.3% | 0.0% | 1 | 14/1830 (0.8%) |
| D | 264 | 99.2% | 0.8% | 10 | 10.0% | 90.0% | 0.0% | 4 | 134/1557 (8.6%) |
| E | 299 | 99.7% | 0.0% | 7 | 0.0% | 100.0% | 0.0% | 9 | 98/1143 (8.6%) |
| F | 149 | 98.7% | 1.3% | 35 | 11.4% | 82.9% | 0.0% | 10 | 234/909 (25.7%) |
| G | 96 | 96.9% | 3.1% | 48 | 2.1% | 95.8% | 0.0% | 15 | 27/533 (5.1%) |
| Others | 513 | 97.5% | 2.3% | 100 | 9.0% | 84.0% | 1.0% | 7 | 361/2907 (12.4%) |

### `|` lines directly after a def/abbrev/instance header (equation compiler) and after `inductive`
| col | def arms: n | +2 | +0 | other | inductive ctors: n | +2 | +0 | other |
|---|---|---|---|---|---|---|---|---|
| A24 | 70 | 94.3% | 0.0% | 5.7% | 77 | 98.7% | 1.3% | 0.0% |
| Aold | 790 | 99.9% | 0.1% | 0.0% | 166 | 98.8% | 1.2% | 0.0% |
| B | 316 | 98.7% | 0.0% | 1.3% | 85 | 100.0% | 0.0% | 0.0% |
| C | 65 | 58.5% | 41.5% | 0.0% | 40 | 90.0% | 10.0% | 0.0% |
| D | 68 | 100.0% | 0.0% | 0.0% | 47 | 100.0% | 0.0% | 0.0% |
| E | 51 | 11.8% | 88.2% | 0.0% | 29 | 13.8% | 86.2% | 0.0% |
| F | 78 | 98.7% | 0.0% | 1.3% | 19 | 89.5% | 10.5% | 0.0% |
| G | 25 | 100.0% | 0.0% | 0.0% | 15 | 100.0% | 0.0% | 0.0% |
| Others | 184 | 99.5% | 0.5% | 0.0% | 84 | 98.8% | 1.2% | 0.0% |

### declaration headers split over lines
| col | multi-line headers | 2nd line +4 | 2nd line +2 | other | header line starting `:` | header line ending ` :` | bodies after `:=`/`:= by`/`:= do` EOL | body +2 | body other |
|---|---|---|---|---|---|---|---|---|---|
| A24 | 197 | 91.7% | 6.4% | 1.9% | 30 | 23 | 2991 | 99.7% | 0.3% |
| Aold | 679 | 93.8% | 4.9% | 1.3% | 30 | 142 | 6172 | 99.6% | 0.4% |
| B | 344 | 97.7% | 2.3% | 0.0% | 5 | 150 | 1856 | 97.8% | 2.2% |
| C | 296 | 98.9% | 1.1% | 0.0% | 0 | 110 | 1123 | 99.4% | 0.6% |
| D | 137 | 93.9% | 4.9% | 1.2% | 9 | 39 | 1656 | 99.3% | 0.7% |
| E | 350 | 4.9% | 92.3% | 2.8% | 174 | 10 | 1483 | 99.4% | 0.6% |
| F | 121 | 68.6% | 31.4% | 0.0% | 23 | 28 | 720 | 99.7% | 0.3% |
| G | 97 | 90.9% | 9.1% | 0.0% | 2 | 47 | 386 | 99.7% | 0.3% |
| Others | 884 | 98.5% | 1.4% | 0.1% | 91 | 412 | 2811 | 99.5% | 0.5% |

### 5 do notation (program code: lines inside def/abbrev/instance/opaque/type declarations)
| pattern (count, per kLOC) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| `do` | 4388 (86.64) | 6765 (59.82) | 3026 (55.71) | 1649 (64.66) | 542 (23.91) | 936 (48.58) | 967 (65.83) | 752 (81.13) | 2388 (47.56) |
| `Id.run do` | 88 (1.74) | 121 (1.07) | 158 (2.91) | 28 (1.10) | 7 (0.31) | 14 (0.73) | 28 (1.91) | 3 (0.32) | 126 (2.51) |
| `let mut` | 369 (7.29) | 752 (6.65) | 512 (9.43) | 161 (6.31) | 46 (2.03) | 36 (1.87) | 88 (5.99) | 121 (13.05) | 348 (6.93) |
| `for … in` | 417 (8.23) | 743 (6.57) | 546 (10.05) | 170 (6.67) | 16 (0.71) | 32 (1.66) | 100 (6.81) | 90 (9.71) | 318 (6.33) |
| `while` | 8 (0.16) | 14 (0.12) | 76 (1.40) | 9 (0.35) | 11 (0.49) | 0 (0.00) | 2 (0.14) | 8 (0.86) | 31 (0.62) |
| `repeat` (term/do) | 32 (0.63) | 3 (0.03) | 27 (0.50) | 0 (0.00) | 3 (0.13) | 0 (0.00) | 2 (0.14) | 7 (0.76) | 3 (0.06) |
| `break` | 22 (0.43) | 24 (0.21) | 67 (1.23) | 10 (0.39) | 19 (0.84) | 0 (0.00) | 4 (0.27) | 11 (1.19) | 17 (0.34) |
| `continue` | 35 (0.69) | 70 (0.62) | 60 (1.10) | 35 (1.37) | 14 (0.62) | 3 (0.16) | 14 (0.95) | 28 (3.02) | 72 (1.43) |
| `return` | 4903 (96.81) | 5119 (45.27) | 1282 (23.60) | 1934 (75.83) | 334 (14.73) | 623 (32.34) | 633 (43.09) | 597 (64.41) | 1749 (34.83) |
| `pure` | 482 (9.52) | 1331 (11.77) | 1088 (20.03) | 157 (6.16) | 178 (7.85) | 110 (5.71) | 248 (16.88) | 113 (12.19) | 472 (9.40) |
| guard return `then return`/`do return` | 1356 (26.77) | 1213 (10.73) | 362 (6.66) | 433 (16.98) | 86 (3.79) | 164 (8.51) | 197 (13.41) | 167 (18.02) | 453 (9.02) |
| `(← …)` nested action | 4368 (86.24) | 4594 (40.62) | 1204 (22.17) | 832 (32.62) | 195 (8.60) | 353 (18.32) | 620 (42.21) | 451 (48.66) | 930 (18.52) |
| `←` total | 8216 (162.22) | 10548 (93.27) | 3933 (72.41) | 2453 (96.18) | 650 (28.67) | 1318 (68.41) | 1629 (110.90) | 1561 (168.41) | 3162 (62.97) |
| `<-` ASCII | 0 (0.00) | 0 (0.00) | 8 (0.15) | 1 (0.04) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `unless` | 529 (10.44) | 621 (5.49) | 177 (3.26) | 69 (2.71) | 4 (0.18) | 68 (3.53) | 46 (3.13) | 73 (7.88) | 159 (3.17) |
| `if let` | 626 (12.36) | 825 (7.30) | 577 (10.62) | 188 (7.37) | 66 (2.91) | 226 (11.73) | 158 (10.76) | 131 (14.13) | 292 (5.81) |
| `if h :` | 131 (2.59) | 314 (2.78) | 165 (3.04) | 71 (2.78) | 59 (2.60) | 92 (4.78) | 18 (1.23) | 10 (1.08) | 78 (1.55) |
| `match ← `/`match (← ` | 86 (1.70) | 356 (3.15) | 65 (1.20) | 54 (2.12) | 25 (1.10) | 56 (2.91) | 22 (1.50) | 22 (2.37) | 66 (1.31) |
| `let some x ← … |` (let-else) | 445 (8.79) | 214 (1.89) | 9 (0.17) | 111 (4.35) | 3 (0.13) | 7 (0.36) | 18 (1.23) | 38 (4.10) | 38 (0.76) |
| `let … := … |` (pure let-else) | 317 (6.26) | 142 (1.26) | 51 (0.94) | 139 (5.45) | 7 (0.31) | 7 (0.36) | 17 (1.16) | 47 (5.07) | 54 (1.08) |
| `try` | 93 (1.84) | 218 (1.93) | 116 (2.14) | 22 (0.86) | 21 (0.93) | 27 (1.40) | 23 (1.57) | 32 (3.45) | 95 (1.89) |
| `catch` | 59 (1.16) | 169 (1.49) | 97 (1.79) | 11 (0.43) | 15 (0.66) | 26 (1.35) | 23 (1.57) | 30 (3.24) | 86 (1.71) |
| `finally` | 16 (0.32) | 65 (0.57) | 23 (0.42) | 8 (0.31) | 10 (0.44) | 2 (0.10) | 0 (0.00) | 2 (0.22) | 11 (0.22) |

### line-initial `return` followed by less-indented continuing code (≈ early return, approximate)
| col | count (per k) |
|---|---|
| A24 | 532 (10.50) |
| Aold | 783 (6.92) |
| B | 176 (3.24) |
| C | 192 (7.53) |
| D | 59 (2.60) |
| E | 89 (4.62) |
| F | 166 (11.30) |
| G | 105 (11.33) |
| Others | 367 (7.31) |

### 6 error handling (program code only; see second table for theorem statements)
| pattern (count, per kLOC) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| `Except` (type/namespace) | 6 (0.12) | 112 (0.99) | 120 (2.21) | 49 (1.92) | 59 (2.60) | 77 (4.00) | 24 (1.63) | 12 (1.29) | 144 (2.87) |
| `ExceptT` | 4 (0.08) | 26 (0.23) | 2 (0.04) | 4 (0.16) | 0 (0.00) | 6 (0.31) | 2 (0.14) | 12 (1.29) | 9 (0.18) |
| `EIO` | 2 (0.04) | 9 (0.08) | 5 (0.09) | 23 (0.90) | 4 (0.18) | 18 (0.93) | 8 (0.54) | 2 (0.22) | 24 (0.48) |
| `IO` (type) | 49 (0.97) | 215 (1.90) | 398 (7.33) | 101 (3.96) | 138 (6.09) | 78 (4.05) | 56 (3.81) | 5 (0.54) | 156 (3.11) |
| `IO.Error` | 0 (0.00) | 4 (0.04) | 6 (0.11) | 24 (0.94) | 25 (1.10) | 0 (0.00) | 0 (0.00) | 1 (0.11) | 15 (0.30) |
| `.userError` | 8 (0.16) | 55 (0.49) | 79 (1.45) | 20 (0.78) | 32 (1.41) | 4 (0.21) | 20 (1.36) | 2 (0.22) | 32 (0.64) |
| `throw` | 58 (1.15) | 251 (2.22) | 220 (4.05) | 56 (2.20) | 42 (1.85) | 123 (6.38) | 35 (2.38) | 12 (1.29) | 127 (2.53) |
| `throwError` | 305 (6.02) | 688 (6.08) | 210 (3.87) | 58 (2.27) | 0 (0.00) | 15 (0.78) | 26 (1.77) | 110 (11.87) | 195 (3.88) |
| `MonadExcept` | 2 (0.04) | 25 (0.22) | 0 (0.00) | 2 (0.08) | 1 (0.04) | 0 (0.00) | 5 (0.34) | 0 (0.00) | 0 (0.00) |
| `Option` (type) | 728 (14.37) | 1411 (12.48) | 786 (14.47) | 338 (13.25) | 363 (16.01) | 329 (17.08) | 202 (13.75) | 158 (17.05) | 862 (17.17) |
| `panic!` | 11 (0.22) | 146 (1.29) | 49 (0.90) | 16 (0.63) | 20 (0.88) | 3 (0.16) | 9 (0.61) | 1 (0.11) | 42 (0.84) |
| `unreachable!` | 110 (2.17) | 202 (1.79) | 1 (0.02) | 67 (2.63) | 0 (0.00) | 2 (0.10) | 25 (1.70) | 2 (0.22) | 26 (0.52) |
| `assert!` | 103 (2.03) | 69 (0.61) | 0 (0.00) | 24 (0.94) | 1 (0.04) | 0 (0.00) | 1 (0.07) | 3 (0.32) | 61 (1.21) |
| `dbg_trace`/`dbgTrace` | 0 (0.00) | 20 (0.18) | 6 (0.11) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 2 (0.14) | 3 (0.32) | 0 (0.00) |
| `sorry` | 8 (0.16) | 2 (0.02) | 1 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 6 (0.41) | 0 (0.00) | 0 (0.00) |
| `.get!` | 107 (2.11) | 53 (0.47) | 27 (0.50) | 19 (0.75) | 6 (0.26) | 2 (0.10) | 9 (0.61) | 2 (0.22) | 52 (1.04) |
| `.getD` | 58 (1.15) | 138 (1.22) | 347 (6.39) | 44 (1.73) | 48 (2.12) | 62 (3.22) | 32 (2.18) | 22 (2.37) | 134 (2.67) |
| `.get?` | 10 (0.20) | 72 (0.64) | 131 (2.41) | 12 (0.47) | 13 (0.57) | 52 (2.70) | 20 (1.36) | 2 (0.22) | 68 (1.35) |
| `[i]!` | 267 (5.27) | 494 (4.37) | 82 (1.51) | 127 (4.98) | 5 (0.22) | 1 (0.05) | 59 (4.02) | 64 (6.90) | 305 (6.07) |
| `[i]?` | 151 (2.98) | 298 (2.64) | 151 (2.78) | 69 (2.71) | 7 (0.31) | 109 (5.66) | 30 (2.04) | 133 (14.35) | 115 (2.29) |
| `[i]'h` | 0 (0.00) | 13 (0.11) | 12 (0.22) | 5 (0.20) | 7 (0.31) | 9 (0.47) | 1 (0.07) | 0 (0.00) | 0 (0.00) |
| other `x!` calls | 594 (11.73) | 1065 (9.42) | 130 (2.39) | 193 (7.57) | 89 (3.93) | 28 (1.45) | 84 (5.72) | 112 (12.08) | 748 (14.90) |
| `Inhabited` (derive/inst/binder) | 150 (2.96) | 501 (4.43) | 113 (2.08) | 94 (3.69) | 132 (5.82) | 77 (4.00) | 41 (2.79) | 22 (2.37) | 251 (5.00) |

### same accessors inside theorem/example declarations
| pattern (count, per kLOC) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| `Option` (type) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 18 (0.36) |
| `.get!` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `.getD` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `.get?` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `[i]!` | 0 (0.00) | 4 (0.04) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `[i]?` | 0 (0.00) | 4 (0.04) | 1 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 2 (0.04) |
| `[i]'h` | 0 (0.00) | 1 (0.01) | 0 (0.00) | 2 (0.08) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| other `x!` calls | 0 (0.00) | 0 (0.00) | 2 (0.04) | 0 (0.00) | 2 (0.09) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 6 (0.12) |

### 7 termination
| col | defs+instances | `partial` | `termination_by` (per k) | … `structural` | `decreasing_by` (per k) | `partial_fixpoint` | `unsafe` decls | `implemented_by` | `nonrec` | `fuel` tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| A24 | 3913 | 207 (5.3%) | 5 (0.10) | 0 | 0 (0.00) | 0 | 22 (0.6%) | 9 | 0 | 0 |
| Aold | 10180 | 689 (6.8%) | 38 (0.34) | 2 | 20 (0.18) | 0 | 172 (1.7%) | 100 | 1 | 23 |
| B | 3836 | 283 (7.4%) | 15 (0.28) | 0 | 8 (0.15) | 0 | 46 (1.2%) | 38 | 0 | 6 |
| C | 2093 | 130 (6.2%) | 8 (0.31) | 0 | 1 (0.04) | 0 | 2 (0.1%) | 2 | 0 | 0 |
| D | 2414 | 32 (1.3%) | 4 (0.18) | 0 | 1 (0.04) | 0 | 0 (0.0%) | 0 | 0 | 0 |
| E | 2543 | 44 (1.7%) | 5 (0.26) | 0 | 2 (0.10) | 0 | 8 (0.3%) | 5 | 20 | 0 |
| F | 1306 | 105 (8.0%) | 0 (0.00) | 0 | 0 (0.00) | 0 | 14 (1.1%) | 7 | 0 | 0 |
| G | 604 | 32 (5.3%) | 1 (0.11) | 0 | 0 (0.00) | 0 | 7 (1.2%) | 7 | 0 | 17 |
| Others | 4126 | 166 (4.0%) | 16 (0.32) | 0 | 5 (0.10) | 0 | 13 (0.3%) | 5 | 3 | 0 |

### 8 data modelling
| col | structure | inductive | class | class inductive | abbrev | abbrev UpperCamel (≈type) | def UpperCamel (≈type) | instances | named instances | named `inst…` | deriving clauses |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A24 | 235 | 77 | 13 | 0 | 299 | 116 | 14 | 156 | 0 (0.0%) | 0 | 129 |
| Aold | 518 | 169 | 123 | 1 | 420 | 250 | 50 | 971 | 54 (5.6%) | 32 | 366 |
| B | 347 | 86 | 24 | 0 | 97 | 79 | 30 | 681 | 17 (2.5%) | 17 | 297 |
| C | 153 | 41 | 5 | 0 | 96 | 69 | 12 | 316 | 10 (3.2%) | 10 | 79 |
| D | 111 | 47 | 9 | 0 | 25 | 23 | 39 | 609 | 2 (0.3%) | 2 | 128 |
| E | 89 | 29 | 41 | 0 | 282 | 133 | 12 | 485 | 5 (1.0%) | 1 | 59 |
| F | 95 | 19 | 12 | 0 | 37 | 33 | 6 | 154 | 1 (0.6%) | 0 | 64 |
| G | 42 | 15 | 3 | 0 | 22 | 16 | 7 | 71 | 28 (39.4%) | 28 | 21 |
| Others | 385 | 89 | 34 | 0 | 95 | 78 | 22 | 819 | 118 (14.4%) | 112 | 283 |

### derived classes (top 12)
- A24: Inhabited 111, BEq 16, Repr 15, Hashable 13, Nonempty 1, DecidableEq 1
- Aold: Inhabited 297, BEq 89, Repr 69, Hashable 27, Nonempty 22, TypeName 15, DecidableEq 14, ToJson 8, FromJson 5, EmptyCollection 4, ToString 1, Ord 1
- B: Repr 163, Inhabited 90, BEq 83, FromJson 64, ToJson 61, DecidableEq 40, Hashable 36, TypeName 35, Ord 29, ToBinary 19, FromBinary 19, Quote 17
- C: Inhabited 62, Repr 17, DecidableEq 14, Hashable 12, BEq 8, Nonempty 7, FromJson 4, ToJson 4, ToBinary 1, FromBinary 1, Lean.FromJson 1, Lean.ToJson 1
- D: Repr 105, Inhabited 80, DecidableEq 49, BEq 28, LE 20, LT 20, Add 9, Sub 9, Neg 9, ToString 9, Nonempty 5, Ord 3
- E: Inhabited 43, Repr 25, DecidableEq 17, Ord 6, ToJson 4, FromJson 4, Nonempty 3, Hashable 1, Lean.ToJson 1, TypeName 1, BEq 1
- F: FromJson 33, ToJson 32, Inhabited 25, BEq 8, Nonempty 6, Repr 4, TypeName 4, Hashable 3
- G: Inhabited 19, BEq 4, Nonempty 1, Ord 1, DecidableEq 1
- Others: ToJson 173, FromJson 167, Inhabited 92, BEq 45, Repr 25, Hashable 21, DecidableEq 17, RpcEncodable 13, Ord 10, TypeName 7, EmptyCollection 2, ToExpr 1

### 9 attributes (`@[…]` on declarations plus `attribute […]` commands)
| attribute (count, per kLOC) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| `inline` | 113 (2.23) | 951 (8.41) | 7 (0.13) | 397 (15.57) | 772 (34.06) | 700 (36.33) | 55 (3.74) | 11 (1.19) | 1171 (23.32) |
| `always_inline` | 14 (0.28) | 113 (1.00) | 0 (0.00) | 0 (0.00) | 12 (0.53) | 35 (1.82) | 5 (0.34) | 6 (0.65) | 147 (2.93) |
| `noinline` | 0 (0.00) | 20 (0.18) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `macro_inline` | 1 (0.02) | 18 (0.16) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 10 (0.52) | 2 (0.14) | 0 (0.00) | 0 (0.00) |
| `specialize` | 9 (0.18) | 162 (1.43) | 1 (0.02) | 36 (1.41) | 6 (0.26) | 20 (1.04) | 5 (0.34) | 0 (0.00) | 27 (0.54) |
| `simp` | 3 (0.06) | 47 (0.42) | 7 (0.13) | 3 (0.12) | 5 (0.22) | 6 (0.31) | 0 (0.00) | 0 (0.00) | 20 (0.40) |
| `grind` | 0 (0.00) | 25 (0.22) | 14 (0.26) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 15 (0.30) |
| `extern` | 32 (0.63) | 457 (4.04) | 1 (0.02) | 237 (9.29) | 28 (1.24) | 4 (0.21) | 13 (0.89) | 0 (0.00) | 22 (0.44) |
| `implemented_by` | 9 (0.18) | 98 (0.87) | 38 (0.70) | 2 (0.08) | 0 (0.00) | 5 (0.26) | 6 (0.41) | 7 (0.76) | 5 (0.10) |
| `csimp` | 0 (0.00) | 5 (0.04) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `reducible` | 0 (0.00) | 21 (0.19) | 12 (0.22) | 0 (0.00) | 0 (0.00) | 9 (0.47) | 0 (0.00) | 0 (0.00) | 1 (0.02) |
| `irreducible` | 0 (0.00) | 2 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 1 (0.02) |
| `semireducible` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `expose` | 13 (0.26) | 219 (1.94) | 51 (0.94) | 17 (0.67) | 46 (2.03) | 32 (1.66) | 124 (8.44) | 3 (0.32) | 121 (2.41) |
| `inherit_doc` | 14 (0.28) | 140 (1.24) | 70 (1.29) | 24 (0.94) | 8 (0.35) | 108 (5.61) | 5 (0.34) | 0 (0.00) | 595 (11.85) |
| `export` | 20 (0.39) | 132 (1.17) | 0 (0.00) | 1 (0.04) | 0 (0.00) | 3 (0.16) | 10 (0.68) | 0 (0.00) | 5 (0.10) |
| `instance` | 0 (0.00) | 6 (0.05) | 14 (0.26) | 5 (0.20) | 1 (0.04) | 1 (0.05) | 0 (0.00) | 1 (0.11) | 7 (0.14) |
| `ext` | 0 (0.00) | 2 (0.02) | 0 (0.00) | 0 (0.00) | 9 (0.40) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 5 (0.10) |
| `deprecated` | 1 (0.02) | 45 (0.40) | 24 (0.44) | 6 (0.24) | 1 (0.04) | 29 (1.51) | 6 (0.41) | 0 (0.00) | 21 (0.42) |
| `builtin_doc` | 1 (0.02) | 120 (1.06) | 30 (0.55) | 1 (0.04) | 0 (0.00) | 0 (0.00) | 8 (0.54) | 2 (0.22) | 5 (0.10) |
| `spec` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 1 (0.11) | 0 (0.00) |
| `simps` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `to_additive` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `match_pattern` | 0 (0.00) | 39 (0.34) | 20 (0.37) | 0 (0.00) | 0 (0.00) | 18 (0.93) | 0 (0.00) | 0 (0.00) | 1 (0.02) |
| `never_extract` | 0 (0.00) | 16 (0.14) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 3 (0.06) |
| `init` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `builtin_init` | 0 (0.00) | 2 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 1 (0.07) | 0 (0.00) | 0 (0.00) |
| `elab_as_elim` | 0 (0.00) | 1 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `induction_eliminator` | 0 (0.00) | 1 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `cases_eliminator` | 0 (0.00) | 1 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `wf_preprocess` | 0 (0.00) | 1 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `congr` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `norm_cast` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `aesop` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `nospecialize` | 0 (0.00) | 2 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 5 (0.26) | 1 (0.07) | 0 (0.00) | 0 (0.00) |
| `local` | 3 (0.06) | 1 (0.01) | 1 (0.02) | 0 (0.00) | 1 (0.04) | 1 (0.05) | 0 (0.00) | 0 (0.00) | 2 (0.04) |
| `scoped` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 1 (0.05) | 0 (0.00) | 1 (0.11) | 3 (0.06) |

### grind variants (top 10)
- A24: 
- Aold: `=` 24, `(plain)` 1
- B: `=` 10, `.` 3, `→` 1
- C: 
- D: 
- E: 
- F: 
- G: 
- Others: `=` 10, `hom` 3, `hom_pred` 2

### other modifiers (decl counts)
| col | `unsafe` decls | `noncomputable` decls | `noncomputable section` | `attribute [..]` cmds | `(priority := …)` |
|---|---|---|---|---|---|
| A24 | 22 | 0 | 0 | 3 | 2 |
| Aold | 172 | 12 | 0 | 62 | 39 |
| B | 46 | 0 | 0 | 3 | 0 |
| C | 2 | 0 | 0 | 5 | 1 |
| D | 0 | 0 | 0 | 1 | 0 |
| E | 8 | 1 | 0 | 5 | 28 |
| F | 14 | 0 | 0 | 0 | 5 |
| G | 7 | 1 | 0 | 2 | 0 |
| Others | 13 | 0 | 0 | 19 | 22 |

### 10 visibility and scoping
| col | decls | `private` | `protected` | explicit `public` | effectively public (est.) | files with `public section` | files with `@[expose] public section` |
|---|---|---|---|---|---|---|---|
| A24 | 4304 | 1117 (26.0%) | 39 (0.9%) | 254 (5.9%) | 2449 (56.9%) | 168 | 0 |
| Aold | 11178 | 1485 (13.3%) | 272 (2.4%) | 63 (0.6%) | 9454 (84.6%) | 347 | 6 |
| B | 4317 | 619 (14.3%) | 29 (0.7%) | 988 (22.9%) | 2940 (68.1%) | 89 | 0 |
| C | 2303 | 98 (4.3%) | 123 (5.3%) | 237 (10.3%) | 1728 (75.0%) | 36 | 5 |
| D | 2614 | 369 (14.1%) | 11 (0.4%) | 12 (0.5%) | 2219 (84.9%) | 87 | 3 |
| E | 2725 | 6 (0.2%) | 204 (7.5%) | 2196 (80.6%) | 2210 (81.1%) | 4 | 0 |
| F | 1432 | 80 (5.6%) | 30 (2.1%) | 81 (5.7%) | 1262 (88.1%) | 39 | 0 |
| G | 669 | 61 (9.1%) | 2 (0.3%) | 109 (16.3%) | 508 (75.9%) | 29 | 3 |
| Others | 4739 | 251 (5.3%) | 20 (0.4%) | 225 (4.7%) | 4276 (90.2%) | 182 | 43 |

| pattern (count, per kLOC) | A24 | Aold | B | C | D | E | F | G | Others |
|---|---|---|---|---|---|---|---|---|---|
| top-level `open X` (not `in`) | 125 (2.47) | 187 (1.65) | 520 (9.57) | 76 (2.98) | 93 (4.10) | 109 (5.66) | 53 (3.61) | 74 (7.98) | 220 (4.38) |
| `open … in` (line ends `in` or `in decl`) | 29 (0.57) | 55 (0.49) | 440 (8.10) | 21 (0.82) | 9 (0.40) | 9 (0.47) | 11 (0.75) | 11 (1.19) | 56 (1.12) |
| indented `open … in` (inside terms) | 3 (0.06) | 3 (0.03) | 72 (1.33) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 3 (0.32) | 3 (0.06) |
| `open scoped` | 0 (0.00) | 2 (0.02) | 3 (0.06) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 3 (0.32) | 1 (0.02) |
| `namespace` | 279 (5.51) | 683 (6.04) | 240 (4.42) | 228 (8.94) | 339 (14.96) | 194 (10.07) | 79 (5.38) | 53 (5.72) | 395 (7.87) |
| `section` | 191 (3.77) | 382 (3.38) | 172 (3.17) | 42 (1.65) | 89 (3.93) | 8 (0.42) | 44 (3.00) | 30 (3.24) | 235 (4.68) |
| `variable` | 19 (0.38) | 64 (0.57) | 59 (1.09) | 13 (0.51) | 3 (0.13) | 11 (0.57) | 18 (1.23) | 2 (0.22) | 103 (2.05) |
| `universe` | 0 (0.00) | 28 (0.25) | 0 (0.00) | 0 (0.00) | 1 (0.04) | 0 (0.00) | 1 (0.07) | 3 (0.32) | 22 (0.44) |
| `set_option … in` | 180 (3.55) | 178 (1.57) | 19 (0.35) | 0 (0.00) | 8 (0.35) | 12 (0.62) | 5 (0.34) | 1 (0.11) | 26 (0.52) |
| top-level `set_option` | 1 (0.02) | 34 (0.30) | 99 (1.82) | 16 (0.63) | 68 (3.00) | 7 (0.36) | 6 (0.41) | 4 (0.43) | 92 (1.83) |
| `prelude` | 239 (4.72) | 366 (3.24) | 19 (0.35) | 81 (3.18) | 88 (3.88) | 115 (5.97) | 45 (3.06) | 48 (5.18) | 222 (4.42) |
| `public import` | 393 (7.76) | 801 (7.08) | 596 (10.97) | 207 (8.12) | 245 (10.81) | 238 (12.35) | 100 (6.81) | 125 (13.49) | 471 (9.38) |
| `public meta import` | 3 (0.06) | 5 (0.04) | 88 (1.62) | 0 (0.00) | 3 (0.13) | 7 (0.36) | 3 (0.20) | 0 (0.00) | 13 (0.26) |
| `meta import` | 2 (0.04) | 16 (0.14) | 25 (0.46) | 0 (0.00) | 0 (0.00) | 24 (1.25) | 4 (0.27) | 19 (2.05) | 2 (0.04) |
| plain `import` | 722 (14.26) | 406 (3.59) | 307 (5.65) | 262 (10.27) | 37 (1.63) | 209 (10.85) | 37 (2.52) | 89 (9.60) | 252 (5.02) |
| `import all` | 1 (0.02) | 13 (0.11) | 16 (0.29) | 0 (0.00) | 4 (0.18) | 3 (0.16) | 0 (0.00) | 2 (0.22) | 5 (0.10) |

### file size (nonblank lines per file)
| col | files | p50 | p90 | p99 | max | >1000 | >1500 |
|---|---|---|---|---|---|---|---|
| A24 | 239 | 126 | 451 | 1464 | 1967 | 6 | 2 |
| Aold | 367 | 152 | 629 | 2323 | 5059 | 22 | 12 |
| B | 172 | 189 | 741 | 1729 | 2092 | 10 | 4 |
| C | 95 | 187 | 617 | 1441 | 1683 | 3 | 1 |
| D | 88 | 204 | 502 | 1030 | 1479 | 2 | 0 |
| E | 115 | 101 | 354 | 1005 | 1345 | 2 | 0 |
| F | 45 | 187 | 700 | 1616 | 1616 | 2 | 2 |
| G | 48 | 111 | 463 | 968 | 968 | 0 | 0 |
| Others | 225 | 129 | 505 | 1364 | 2208 | 3 | 2 |

### 11 documentation
| col | public defs documented | public types documented | public theorems documented | public named instances documented | private defs documented | files with module doc | module docs per file | module docs starting with `#` |
|---|---|---|---|---|---|---|---|---|
| A24 | 847/1981 (42.8%) +14 inherit_doc | 145/265 (54.7%) +0 inherit_doc | 2/5 (40.0%) +0 inherit_doc | 0/0 (–) +0 inherit_doc | 35.6% | 79/239 (33.1%) | 0.47 | 34.8% |
| Aold | 3245/7558 (42.9%) +69 inherit_doc | 421/754 (55.8%) +0 inherit_doc | 23/158 (14.6%) +0 inherit_doc | 9/54 (16.7%) +0 inherit_doc | 34.0% | 94/367 (25.6%) | 0.43 | 52.5% |
| B | 1058/1913 (55.3%) +64 inherit_doc | 237/414 (57.2%) +0 inherit_doc | 0/11 (0.0%) +0 inherit_doc | 0/15 (0.0%) +0 inherit_doc | 49.6% | 37/172 (21.5%) | 0.50 | 37.2% |
| C | 721/1270 (56.8%) +24 inherit_doc | 102/141 (72.3%) +0 inherit_doc | 0/10 (0.0%) +0 inherit_doc | 0/10 (0.0%) +0 inherit_doc | 19.5% | 56/95 (58.9%) | 0.64 | 14.8% |
| D | 1419/1440 (98.5%) +6 inherit_doc | 146/149 (98.0%) +0 inherit_doc | 1/21 (4.8%) +2 inherit_doc | 0/2 (0.0%) +0 inherit_doc | 39.2% | 46/88 (52.3%) | 0.52 | 69.6% |
| E | 899/1643 (54.7%) +107 inherit_doc | 89/127 (70.1%) +0 inherit_doc | 3/10 (30.0%) +0 inherit_doc | 0/5 (0.0%) +0 inherit_doc | 18.8% | 61/115 (53.0%) | 1.62 | 95.7% |
| F | 341/992 (34.4%) +5 inherit_doc | 51/120 (42.5%) +0 inherit_doc | 0/0 (–) +0 inherit_doc | 0/1 (0.0%) +0 inherit_doc | 38.8% | 21/45 (46.7%) | 0.60 | 40.7% |
| G | 185/379 (48.8%) +0 inherit_doc | 29/53 (54.7%) +0 inherit_doc | 3/5 (60.0%) +0 inherit_doc | 8/28 (28.6%) +0 inherit_doc | 68.2% | 22/48 (45.8%) | 0.52 | 48.0% |
| Others | 1565/2898 (54.0%) +576 inherit_doc | 239/481 (49.7%) +7 inherit_doc | 3/92 (3.3%) +0 inherit_doc | 0/118 (0.0%) +0 inherit_doc | 41.3% | 131/225 (58.2%) | 0.90 | 54.0% |

### def docstring form
| col | def docstrings | contain backticks | single-line | text starts on next line | end with period | start with code | top first words |
|---|---|---|---|---|---|---|---|
| A24 | 1480 | 88.2% | 48.7% | 59.5% | 86.6% | 4.0% | Returns 355, Given 93, The 52, Helper 40, Similar 39, Adds 31, If 30, Simplifies 29, Creates 28, Return 28 |
| Aold | 3806 | 82.4% | 40.7% | 65.7% | 79.5% | 6.0% | Returns 262, Return 262, The 154, Given 149, Converts 128, If 97, Internal 84, Creates 78, Similar 71, A 68 |
| B | 1674 | 48.0% | 58.1% | 60.2% | 95.8% | 1.3% | The 259, A 187, Parses 77, Runs 55, Whether 52, Adds 44, Returns 41, Builds 34, Renders 34, An 29 |
| C | 820 | 77.6% | 43.2% | 90.2% | 84.4% | 1.2% | Converts 71, The 43, Creates 41, Bitwise 25, Returns 24, Runs 23, Gets 21, Add 18, If 17, Obtain 16 |
| D | 1562 | 65.5% | 69.0% | 99.6% | 92.1% | 2.5% | Creates 205, Converts 140, Returns 89, Parses 77, Checks 70, Adds 69, Convert 55, Subtracts 46, Gets 43, The 43 |
| E | 977 | 53.3% | 71.6% | 28.6% | 96.7% | 1.3% | The 184, Returns 101, A 82, Build 28, Whether 26, Get 23, Fetch 20, Run 19, Try 18, Compute 16 |
| F | 403 | 75.2% | 55.1% | 43.4% | 94.0% | 1.0% | The 47, Returns 25, Creates 11, Checks 11, Return 11, Recursively 11, Adds 10, Delaborates 9, Computes 8, A 7 |
| G | 290 | 93.4% | 39.7% | 29.0% | 98.3% | 3.1% | The 50, Strategy 17, A 13, Build 12, Given 8, Elaborate 7, Create 7, Whether 6, Register 5, Return 5 |
| Others | 1734 | 71.0% | 45.1% | 61.4% | 85.7% | 1.1% | Returns 224, Implementation 94, Given 91, Converts 79, Tries 57, The 54, Computes 39, A 36, If 34, Checks 33 |

