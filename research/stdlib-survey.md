# Lean standard library style survey (descriptive measurements)

Track: `survey`. Kind: descriptive. This file measures what the code does; it states no rules. Normative core docs (`lean4/doc/std/style.md`, `naming.md`) are cited only to say whether the code matches them.

## Provenance

Measured 2026-10-17. All counts come from `research/scripts/survey.py` (helpers in `research/scripts/leanlex.py`), run from `research/vendor/repos`:

```
cd research/vendor/repos
python3 ../../scripts/survey.py                    # every section (≈4 min, Mathlib dominates)
python3 ../../scripts/survey.py format --cols Init,Std
python3 ../../scripts/survey.py --samples Init '<regex>' 8   # print matching lines to spot-check
```

The lexer blanks comments, docstrings, string and char literals before matching, so counts are over code only (except line length, which uses raw lines). Lexed files are cached in `research/vendor/survey-cache/` (keyed by repo SHA).

| Column | Repo | Paths (relative to `research/vendor/repos`) | SHA | Commit date | Toolchain | License |
|---|---|---|---|---|---|---|
| Init, Std, Lake, Lean | leanprover/lean4 | `lean4/src/Init`, `lean4/src/Std`, `lean4/src/lake/Lake`, `lean4/src/Lean` | `3a685e6c855f0eb4ccabe92e21120f1b1ef81d24` | 2026-10-17 | master, 4.37.0 pre-release | Apache-2.0 |
| Batteries | leanprover-community/batteries | `batteries/Batteries` | `4453b52d2468f4c346a8711d728c0742e7483c9b` | 2026-10-14 | v4.36.0-rc1 | Apache-2.0 |
| Mathlib (contrast) | leanprover-community/mathlib4 | `mathlib4/Mathlib` | `7bb03b4c5313d552989ba5b1c6d3f0f436f65d73` | 2026-10-17 | v4.36.0-rc1 | Apache-2.0 |
| Wild | pandaman64/lean-regex | `lean-regex/regex/Regex`, `lean-regex/correctness/RegexCorrectness` | `32af6f33d80e1dad2b072da6981da58e92b08b9e` | 2026-09-30 | v4.34.0-rc1 (`regex/lean-toolchain`) | Apache-2.0 (LICENSE) |
| Wild | fgdorais/lean4-parser | `lean4-parser/Parser` | `473006727021275f42039a015b6296d86c9021f0` | 2026-10-15 | v4.36.0-rc1 | Apache-2.0 (LICENSE) |
| Wild | leanprover/lean4-cli | `lean4-cli/Cli` | `34d2efffcb6dc8d5f3537cf6a7f88bfaa999ec49` | 2026-10-14 | v4.36.0-rc1 | MIT (LICENSE) |

The wild libraries are the three with the most GitHub stars among the "Libraries" entries of [awesome-lean-programming](https://github.com/saviorand/awesome-lean-programming) (lean4-cli 123, lean-regex 111, lean4-parser 89, checked with `gh repo view` on 2026-10-17). lean4-cli lives in the `leanprover` org, so "wild" is only partly independent of core. The Wild column is small (13k nonblank lines, two thirds of it lean-regex), so treat its percentages as anecdotal.

An opt-in `FPIL` column covers the example code of *Functional Programming in Lean*: `fp-lean/examples`, without its `ExampleSupport.lean` infrastructure; commit `0abeea545d560a324e2561f7210fbd6ed154fa02`, 2026-08-13, Lean 4.33.0; 53 files, 14,546 nonblank lines. It is defined in `leanlex.py` as `EXTRA_SUBTREES` and left out of the default columns, so the tables below are unchanged. Select it with `--cols FPIL,…`. It contains deliberately broken examples and successive drafts. Its results are in [notes/fpil.md](notes/fpil.md#measured-the-books-example-code).

Size baseline (reproduced exactly by `survey.py baseline`; "per k" below always means per 1,000 nonblank lines of that column):

| col | files | lines | nonblank | `module` files | decls parsed |
|---|---|---|---|---|---|
| Init | 672 | 217040 | 178605 | 672 | 32290 |
| Std | 499 | 198284 | 162450 | 499 | 27368 |
| Lake | 164 | 31966 | 27001 | 164 | 3292 |
| Lean | 1250 | 288812 | 255617 | 1250 | 21229 |
| Batteries | 194 | 29569 | 24639 | 194 | 3394 |
| Mathlib | 8642 | 2344052 | 1882574 | 8642 | 260489 |
| Wild | 132 | 15565 | 13098 | 132 | 1515 |

Every library file in every column is a `module` file (new module system), including all three wild libraries; Mathlib marks a few with `module -- shake: keep-all`.

## Ten notable measurements

1. **Lambdas**: `fun x =>` is near universal in core (97–99% of `fun`/`λ` binders end in `=>`; `λ` appears 0–3 times per subtree). Mathlib is split 51% `=>` / 49% `↦` and is the only place `↦` and `λ` occur in volume.
2. **Theorem density splits the stdlib in two**: Init and Std have 5.5 and 4.6 theorems per def; Lake and Lean have essentially none (24 and 31 theorems). "Init/Std style" is largely proof style; programming style lives in Lake and Lean.
3. **`do`-notation density** differs by 30–50×: `do` occurs 1.5/k in Init and 5.3/k in Std program code, but 50/k in Lake and 74/k in Lean. Early `return`, `let mut`, `for`, `unless` and `if let` follow the same split.
4. **`?`/`!`/`D` families are a Std idiom**: Std has 233 `X?` defs that also have `X!` and 105 complete `X`/`X?`/`X!`/`XD` quadruples. Lean has 1,149 `X?` defs, of which 9 have a `!` twin: there `?` simply means "returns `Option`".
5. **Lake has its own layout**: `|` arms of equation-style defs and `inductive` constructors at column 0 (87.5% / 76.2% vs ≈98% indented +2 elsewhere); signature continuation at +2 (87%) rather than +4 (94–99% elsewhere); 202 headers put the `:` at the start of a line, which `style.md` forbids.
6. **Lines**: p95 is 86–99 code points everywhere, but Init (3.9%), Lean (4.0%) and Std (1.9%) have many lines over 100; Batteries (1 line) and Mathlib (430 of 1.9M) enforce 100. No tabs; trailing whitespace only 3 lines (all in Lean).
7. **Docstrings**: public defs are documented 73% (Init), 71% (+923 `inherit_doc`, Std), 56% (Lake), 39% (Lean), 97% (Batteries, Mathlib). Theorems are almost never documented in core (2–3%). Def docstrings in Init/Std open with a third-person verb ("Returns", "Converts", "Creates", "Checks").
8. **Visibility in the module system**: Init/Std/Lean mostly use a file-level `public section` (525/404/928 files); Lake instead marks 76% of declarations `public` one by one and has a `public section` in only 2 files. Std puts `@[expose]` on 241 of its `public section`s.
9. **Termination**: `partial` is rare in Init/Std (0.7–1.0% of defs and instances) but 7.7% in Lean; `termination_by` is 0.6–0.75/k in Init/Std; `partial_fixpoint` appears in no library code at all (only in 26 test files).
10. **Proofs about programs live in separate files**: Std's HashMap/TreeMap families keep definitions in `Basic.lean` (1 theorem each) and thousands of lemmas in `Lemmas.lean`/`RawLemmas.lean`; the bundled type is `structure DHashMap where inner : Raw α β; wf : inner.WF`. 108 Init files and 88 Std files are named `Lemmas.lean` or sit under `Lemmas/`.

## How to read the numbers (caveats common to all sections)

- **Declarations** are found by a line regex (`leanlex.DECL_RE`): optional `@[…]` attributes (multi-line attribute lists handled), modifiers (`private protected public noncomputable partial unsafe nonrec meta`, `scoped`/`local`), then `def theorem lemma abbrev instance structure class [inductive|abbrev] inductive coinductive opaque axiom example`. Declarations generated by commands (`macro`, `syntax`, `elab`, `register_option`, `initialize`, `deriving instance`, `builtin_initialize`, `notation`) are not counted. Declarations inside docstrings and comments are excluded (rg-based counts over raw text overcount; e.g. rg finds 81 `theorem` lines in `src/Lean`, the parser finds 31, the rest are in comments).
- **Program vs proof code** (sections 5–6): a line belongs to a declaration from its first attribute line up to the next unindented command line. "prog" = def/abbrev/instance/opaque/structure/class/inductive; "thm" = theorem/example. Commands between declarations (macros, `syntax`, `elab`) are attributed to nothing.
- **Public** (docs, visibility): in a `module` file a declaration counts as public if it is marked `public`, or it is inside a `public section` and not `private`. This follows `Visibility.isInferredPublic` in core ([DeclModifiers.lean L77-L89](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Lean/Elab/DeclModifiers.lean#L77-L89): `if env.isExporting || !env.header.isModule then !v.isPrivate else v.isPublic`). Scope tracking handles `namespace`/`section`/`mutual`/`end`, not `in`-suffixed commands.
- Regex counts were spot-checked by eye on samples (`--samples`); where a pattern is known to be loose, the section says so. All percentages are of parsed items, not of Lean's elaborated environment.

## 1. Naming

Script: `survey.py naming` (`s_naming`). Case classes apply to the last dotted component after stripping trailing `?`, `!`, `'` and subscripts: `UpperCamel`, `lowerCamel` (has an inner capital, no `_`), `lowerword` (one lowercase word, e.g. `map`, compatible with both lowerCamel and snake), `snake` (`_`, no capitals), `snake+camel` (`_` plus capitals, e.g. `getElem?_eq_none`, which `naming.md` prescribes for theorems about lowerCamel defs).

#### def
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 3884 | 1.9% | 58.5% | 33.3% | 4.6% | 1.7% | 0.0% | 0.0% |
| Std | 4353 | 2.5% | 68.4% | 28.8% | 0.3% | 0.0% | 0.0% | 0.0% |
| Lake | 2213 | 0.4% | 81.1% | 18.4% | 0.0% | 0.0% | 0.0% | 0.1% |
| Lean | 16741 | 0.6% | 86.9% | 12.1% | 0.2% | 0.1% | 0.0% | 0.1% |
| Batteries | 1053 | 4.8% | 64.8% | 29.2% | 0.7% | 0.3% | 0.0% | 0.3% |
| Mathlib | 33658 | 7.3% | 66.2% | 25.6% | 0.4% | 0.5% | 0.1% | 0.0% |
| Wild | 673 | 5.2% | 55.1% | 39.5% | 0.0% | 0.0% | 0.1% | 0.0% |

#### abbrev
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 367 | 24.0% | 41.4% | 28.9% | 5.7% | 0.0% | 0.0% | 0.0% |
| Std | 123 | 72.4% | 15.4% | 12.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 305 | 47.9% | 31.5% | 20.3% | 0.0% | 0.0% | 0.0% | 0.3% |
| Lean | 836 | 64.2% | 28.8% | 6.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| Batteries | 42 | 31.0% | 47.6% | 21.4% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 3684 | 24.9% | 48.1% | 26.4% | 0.2% | 0.3% | 0.1% | 0.0% |
| Wild | 21 | 76.2% | 9.5% | 14.3% | 0.0% | 0.0% | 0.0% | 0.0% |

#### theorem
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 24638 | 0.0% | 0.5% | 1.3% | 44.9% | 53.2% | 0.0% | 0.0% |
| Std | 20937 | 0.0% | 0.9% | 1.8% | 28.9% | 68.2% | 0.2% | 0.0% |
| Lake | 24 | 0.0% | 0.0% | 0.0% | 20.8% | 79.2% | 0.0% | 0.0% |
| Lean | 31 | 0.0% | 0.0% | 6.5% | 22.6% | 67.7% | 0.0% | 3.2% |
| Batteries | 2021 | 0.0% | 3.0% | 7.5% | 30.9% | 57.4% | 1.2% | 0.0% |
| Mathlib | 190733 | 0.0% | 2.5% | 4.9% | 41.6% | 49.6% | 1.3% | 0.0% |
| Wild | 648 | 0.0% | 5.1% | 21.1% | 45.7% | 28.1% | 0.0% | 0.0% |

#### instance
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 411 | 0.0% | 92.5% | 2.7% | 2.9% | 1.9% | 0.0% | 0.0% |
| Std | 114 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 5 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lean | 9 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Batteries | 9 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 12172 | 0.5% | 63.0% | 10.5% | 5.6% | 20.3% | 0.1% | 0.0% |
| Wild | 2 | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

#### structure
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 188 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Std | 301 | 99.0% | 1.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 128 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lean | 1478 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Batteries | 42 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 1712 | 98.9% | 0.6% | 0.4% | 0.1% | 0.0% | 0.1% | 0.0% |
| Wild | 32 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

#### class
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 289 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Std | 46 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 45 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lean | 69 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Batteries | 16 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 1999 | 99.8% | 0.1% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| Wild | 13 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

#### class inductive
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 1 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Std | 0 | – | – | – | – | – | – | – |
| Lake | 0 | – | – | – | – | – | – | – |
| Lean | 0 | – | – | – | – | – | – | – |
| Batteries | 0 | – | – | – | – | – | – | – |
| Mathlib | 7 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Wild | 0 | – | – | – | – | – | – | – |

#### inductive
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 108 | 97.2% | 0.0% | 2.8% | 0.0% | 0.0% | 0.0% | 0.0% |
| Std | 88 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 42 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lean | 412 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Batteries | 26 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 344 | 89.2% | 8.1% | 2.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| Wild | 30 | 96.7% | 3.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

#### opaque
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 210 | 3.8% | 44.8% | 51.4% | 0.0% | 0.0% | 0.0% | 0.0% |
| Std | 108 | 7.4% | 53.7% | 38.9% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 11 | 36.4% | 45.5% | 9.1% | 0.0% | 0.0% | 0.0% | 9.1% |
| Lean | 365 | 4.7% | 75.9% | 19.5% | 0.0% | 0.0% | 0.0% | 0.0% |
| Batteries | 1 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 2 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Wild | 0 | – | – | – | – | – | – | – |

#### axiom
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 12 | 0.0% | 75.0% | 25.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Std | 0 | – | – | – | – | – | – | – |
| Lake | 1 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lean | 0 | – | – | – | – | – | – | – |
| Batteries | 0 | – | – | – | – | – | – | – |
| Mathlib | 0 | – | – | – | – | – | – | – |
| Wild | 0 | – | – | – | – | – | – | – |

#### namespace
| col | n | UpperCamel | lowerCamel | lowerword | snake | snake+camel | Upper_snake | other |
|---|---|---|---|---|---|---|---|---|
| Init | 1190 | 99.3% | 0.2% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% |
| Std | 1872 | 95.7% | 1.7% | 2.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| Lake | 273 | 98.5% | 0.0% | 1.1% | 0.0% | 0.0% | 0.0% | 0.4% |
| Lean | 3979 | 99.9% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| Batteries | 291 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Mathlib | 16723 | 97.5% | 1.8% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| Wild | 331 | 95.5% | 4.2% | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% |

#### suffixes and primes (last component; defs = def/abbrev/opaque, thms = theorem)

#### defs
| suffix (count, % of kind) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| ends `'` (primed) | 87 (2.0%) | 32 (0.7%) | 21 (0.8%) | 218 (1.2%) | 27 (2.5%) | 1016 (2.7%) | 20 (2.9%) |
| ends `?` | 192 (4.3%) | 299 (6.5%) | 204 (8.1%) | 1152 (6.4%) | 74 (6.8%) | 131 (0.4%) | 36 (5.2%) |
| ends `!` | 54 (1.2%) | 274 (6.0%) | 3 (0.1%) | 117 (0.7%) | 20 (1.8%) | 15 (0.0%) | 35 (5.0%) |
| ends lower+`D` (getD-style) | 13 (0.3%) | 129 (2.8%) | 8 (0.3%) | 19 (0.1%) | 15 (1.4%) | 13 (0.0%) | 1 (0.1%) |
| ends `Impl` | 50 (1.1%) | 9 (0.2%) | 2 (0.1%) | 87 (0.5%) | 3 (0.3%) | 15 (0.0%) | 0 (0.0%) |
| ends `Aux` | 57 (1.3%) | 2 (0.0%) | 5 (0.2%) | 189 (1.1%) | 14 (1.3%) | 288 (0.8%) | 10 (1.4%) |
| ends `Core` | 9 (0.2%) | 5 (0.1%) | 35 (1.4%) | 285 (1.6%) | 6 (0.5%) | 63 (0.2%) | 3 (0.4%) |
| ends `Unsafe`/`unsafe` | 17 (0.4%) | 2 (0.0%) | 0 (0.0%) | 55 (0.3%) | 5 (0.5%) | 0 (0.0%) | 0 (0.0%) |
| ends `TR` | 42 (0.9%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 18 (1.6%) | 2 (0.0%) | 0 (0.0%) |
| ends lower+`M` (monadic) | 124 (2.8%) | 63 (1.4%) | 36 (1.4%) | 330 (1.8%) | 60 (5.5%) | 81 (0.2%) | 4 (0.6%) |
| is `go` | 5 (0.1%) | 1 (0.0%) | 0 (0.0%) | 6 (0.0%) | 0 (0.0%) | 1 (0.0%) | 0 (0.0%) |
| is `loop` | 1 (0.0%) | 0 (0.0%) | 3 (0.1%) | 4 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| is `aux` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 20 (0.1%) | 0 (0.0%) |
| ends `_eq` | 4 (0.1%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 1 (0.0%) | 0 (0.0%) |
| ends `_iff` | 2 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `_def` | 1 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| contains `_of_` | 20 (0.4%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 48 (0.1%) | 0 (0.0%) |
| ends `_spec` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

#### thms
| suffix (count, % of kind) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| ends `'` (primed) | 607 (2.5%) | 292 (1.4%) | 1 (4.2%) | 0 (0.0%) | 27 (1.3%) | 6975 (3.7%) | 34 (5.2%) |
| ends `?` | 200 (0.8%) | 657 (3.1%) | 0 (0.0%) | 0 (0.0%) | 49 (2.4%) | 27 (0.0%) | 0 (0.0%) |
| ends `!` | 25 (0.1%) | 627 (3.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 3 (0.0%) | 0 (0.0%) |
| ends lower+`D` (getD-style) | 22 (0.1%) | 318 (1.5%) | 0 (0.0%) | 0 (0.0%) | 9 (0.4%) | 25 (0.0%) | 0 (0.0%) |
| ends `Impl` | 6 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `Aux` | 15 (0.1%) | 4 (0.0%) | 0 (0.0%) | 0 (0.0%) | 9 (0.4%) | 91 (0.0%) | 5 (0.8%) |
| ends `Core` | 2 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 1 (0.0%) | 13 (0.0%) | 0 (0.0%) |
| ends `Unsafe`/`unsafe` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| ends `TR` | 40 (0.2%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 19 (0.9%) | 1 (0.0%) | 0 (0.0%) |
| ends lower+`M` (monadic) | 227 (0.9%) | 117 (0.6%) | 0 (0.0%) | 0 (0.0%) | 34 (1.7%) | 8 (0.0%) | 0 (0.0%) |
| is `go` | 0 (0.0%) | 4 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 2 (0.3%) |
| is `loop` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| is `aux` | 6 (0.0%) | 1 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 17 (0.0%) | 0 (0.0%) |
| ends `_eq` | 821 (3.3%) | 1266 (6.0%) | 2 (8.3%) | 1 (3.2%) | 96 (4.8%) | 4504 (2.4%) | 29 (4.5%) |
| ends `_iff` | 1712 (6.9%) | 584 (2.8%) | 0 (0.0%) | 5 (16.1%) | 70 (3.5%) | 10097 (5.3%) | 34 (5.2%) |
| ends `_def` | 108 (0.4%) | 18 (0.1%) | 0 (0.0%) | 0 (0.0%) | 10 (0.5%) | 1286 (0.7%) | 8 (1.2%) |
| contains `_of_` | 2921 (11.9%) | 4526 (21.6%) | 4 (16.7%) | 3 (9.7%) | 242 (12.0%) | 24553 (12.9%) | 132 (20.4%) |
| ends `_spec` | 14 (0.1%) | 6 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 122 (0.1%) | 2 (0.3%) |

#### `?`/`!`/`D` families among defs (qualified names)
| col | X? defs | X! defs | XD defs | X? with X! | X? with XD | X? with plain X | X! without X? | all four |
|---|---|---|---|---|---|---|---|---|
| Init | 192 | 54 | 13 | 26 | 6 | 61 | 28 | 3 |
| Std | 299 | 274 | 129 | 233 | 124 | 173 | 41 | 105 |
| Lake | 204 | 3 | 8 | 0 | 7 | 42 | 3 | 0 |
| Lean | 1149 | 117 | 19 | 9 | 5 | 87 | 108 | 0 |
| Batteries | 74 | 20 | 15 | 11 | 6 | 8 | 9 | 0 |
| Mathlib | 131 | 15 | 13 | 1 | 0 | 10 | 14 | 0 |
| Wild | 36 | 35 | 1 | 23 | 1 | 0 | 12 | 0 |

Init complete families (sample): List.getLast, List.head, List.tail

Std complete families (sample): Std.DHashMap.Const.get, Std.DHashMap.Internal.AssocList.get, Std.DHashMap.Internal.AssocList.getCast, Std.DHashMap.Internal.AssocList.getEntry, Std.DHashMap.Internal.AssocList.getKey, Std.DHashMap.Internal.Raw₀.Const.get, Std.DHashMap.Internal.Raw₀.get, Std.DHashMap.Internal.Raw₀.getEntry, Std.DHashMap.Internal.Raw₀.getKey, Std.DHashMap.Raw.Const.get, Std.DHashMap.Raw.get, Std.DHashMap.Raw.getEntry, Std.DHashMap.Raw.getKey, Std.DHashMap.get, Std.DHashMap.getEntry, Std.DHashMap.getKey, Std.DTreeMap.Const.entryAtIdx, Std.DTreeMap.Const.get, Std.DTreeMap.Const.getEntryGE, Std.DTreeMap.Const.getEntryGT, Std.DTreeMap.Const.getEntryLE, Std.DTreeMap.Const.getEntryLT, Std.DTreeMap.Const.maxEntry, Std.DTreeMap.Const.minEntry, Std.DTreeMap.Internal.Impl.Const.entryAtIdx

Observations:
- Defs are lowerCamel/lowerword in 92–99% of cases in every column; types, classes and namespaces are UpperCamel at 95–100%. Init's 4.6% snake defs are mostly Prop-valued or certificate functions in `Init/Grind`/`Init/Omega` (spot-checked, not counted).
- Theorems are snake (29–45%) or snake+camel (50–68%); Std's higher snake+camel share reflects names built from lowerCamel API names (`getKey?_insert`, `getD_eq_getD_get?`).
- Named instances in core are lowerCamel `inst…` names (Init 302 of 411 named instances start with `inst`); Mathlib has many snake-named instances (26%).
- Primes: 0.7–2.0% of core defs and 1.4–2.5% of Init/Std theorems end in `'`; Mathlib theorems 3.7%.
- Suffix families: `?` ends 4–8% of core defs; `!` is common only in Std (6.0%), where it pairs with `?` (233 pairs); Lean uses `!` mostly without a `?` twin (108 of 117). `TR` (tail-recursive twin, paired with `@[csimp]`) occurs only in Init (42) and Batteries (18). `Impl`, `Aux`, `Core` are each ≤1.6% of defs; `Core` is most frequent in Lake and Lean.

Examples:
- Std accessor family with docstrings pointing to notation: [Std/Data/HashMap/Basic.lean L130-L167](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/HashMap/Basic.lean#L130-L167): `@[inline] def get? (m : HashMap α β) (a : α) : Option β`, `def get … (h : a ∈ m) : β`, `def getD … (fallback : β) : β`, `def get! [Inhabited β] …` ("The notation `m[a]!` is preferred over calling this function directly.").
- Init list family: [Init/Data/List/Basic.lean L352-L391](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/List/Basic.lean#L352-L391) (`head : (as : List α) → as ≠ [] → α`, `head?`, `headD`); `head!` lives in [Init/Data/List/BasicAux.lean L79](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/List/BasicAux.lean#L79).
- `TR` twin plus `@[csimp]`: [Init/Data/List/Impl.lean L70-L79](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/List/Impl.lean#L70-L79) (`def setTR … := go l n #[] where …`, `@[csimp] theorem set_eq_setTR : @set = @setTR`).

Caveats: case classification of one-word names is ambiguous (reported separately as `lowerword`); qualified-name families use the namespace stack and ignore `_root_` edge cases and `export`.

## 2. Lambda syntax

Script: `survey.py lambda` (`s_lambda`, `_fun_arrows`): for each `fun`/`λ` token, scan forward at bracket depth 0 to the first `=>` or `↦`; `fun |` is a pattern-matching lambda. `·` is split into line-initial (tactic focusing dot) and other (≈ `(· + 1)` sections, but also `·` inside notation such as `·.map f`).

| col | `fun` (per k) | `λ` (per k) | binder ends `=>` (% of fun+λ) | binder ends `↦` | `fun |` alts | `·` not line-initial (≈ sections) (per k) | `·` line-initial (focus dot) (per k) |
|---|---|---|---|---|---|---|---|
| Init | 5069 (28.38) | 3 (0.02) | 4931 (97.2%) | 73 (1.4%) | 67 (1.3%) | 2639 (14.78) | 6230 (34.88) |
| Std | 7737 (47.63) | 1 (0.01) | 7683 (99.3%) | 2 (0.0%) | 53 (0.7%) | 538 (3.31) | 3179 (19.57) |
| Lake | 632 (23.41) | 0 (0.00) | 615 (97.3%) | 0 (0.0%) | 17 (2.7%) | 521 (19.30) | 9 (0.33) |
| Lean | 9113 (35.65) | 1 (0.00) | 8888 (97.5%) | 18 (0.2%) | 196 (2.2%) | 2889 (11.30) | 23 (0.09) |
| Batteries | 899 (36.49) | 3 (0.12) | 873 (96.8%) | 0 (0.0%) | 29 (3.2%) | 543 (22.04) | 597 (24.23) |
| Mathlib | 114301 (60.72) | 782 (0.42) | 58365 (50.7%) | 55836 (48.5%) | 111 (0.1%) | 14499 (7.70) | 54785 (29.10) |
| Wild | 206 (15.73) | 0 (0.00) | 190 (92.2%) | 0 (0.0%) | 16 (7.8%) | 62 (4.73) | 29 (2.21) |

- Core matches `style.md` ("use `fun a => f x` instead of `fun x ↦ f x` or `λ x => f x`"). Init's 73 `↦` sit mostly in proof files (largest counts: `Init/Data/Nat/Lemmas.lean` 9, `Init/Core.lean` 8, `Init/Data/Rat/Lemmas.lean` 7).
- Mathlib sets `pp.unicode.fun true` ("pretty-prints `fun a ↦ b`") in its lakefile ([lakefile.lean L43](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/lakefile.lean#L43)) and lints `λ` (`linter.style.lambdaSyntax`, section 15).
- `·` sections: Batteries 22/k, Lake 19/k, Init 15/k, Std 3.3/k. Example: [Std/Async/Basic.lean L431](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Async/Basic.lean#L431) `mk <| (·.map f prio sync) <$> self.toRawBaseIO`.

Caveat: the `·` split is approximate (a `·` continuing a wrapped term at line start would be misread as a focus dot).

## 3. Local helpers

Script: `survey.py helpers` (`s_helpers`, `where_helpers`). A `where` clause counts if it stands at the start of a line after a body (`:=` or `|` seen since the last declaration keyword); helper names are the identifiers at the first indentation level below it. `where finally` (discharges `?_` goals) is excluded. `let rec` is a regex over code.

| col | `where` helpers (per k) | `let rec` (per k) | private defs | top-level `X.go`/`X.loop`/`X.aux` defs | `go` share | `loop` share | `aux` share |
|---|---|---|---|---|---|---|---|
| Init | 139 (0.78) | 101 (0.57) | 124 (2.8% of defs) | 6 | 42.9% | 30.0% | 2.1% |
| Std | 111 (0.68) | 21 (0.13) | 415 (9.1% of defs) | 0 | 59.8% | 8.3% | 0.0% |
| Lake | 94 (3.48) | 7 (0.26) | 3 (0.1% of defs) | 0 | 11.9% | 5.0% | 0.0% |
| Lean | 1732 (6.78) | 246 (0.96) | 3048 (17.0% of defs) | 0 | 25.5% | 4.9% | 0.1% |
| Batteries | 56 (2.27) | 16 (0.65) | 47 (4.3% of defs) | 0 | 47.2% | 29.2% | 1.4% |
| Mathlib | 192 (0.10) | 23 (0.01) | 554 (1.5% of defs) | 17 | 19.5% | 3.7% | 2.3% |
| Wild | 54 (4.12) | 3 (0.23) | 67 (9.7% of defs) | 0 | 19.3% | 21.1% | 0.0% |

Init where-helper names top: [('go', 79), ('loop', 16), ('aux', 5), ('run', 2), ('elim', 2), ('consumeSpaces', 2), ('maybeEscape', 2), ('maybePseudoSyntax', 2)]; let rec top: [('loop', 56), ('go', 24), ('fold', 5), ('map', 5), ('find', 2), ('read', 2)]

Std where-helper names top: [('go', 69), ('size', 2), ('registerAux', 2), ('blast', 2), ('bindAsyncTask', 1), ('asterisk', 1), ('origin', 1), ('absoluteFromScheme', 1)]; let rec top: [('loop', 11), ('go', 10)]

Lake where-helper names top: [('go', 12), ('insert', 2), ('compute', 2), ('invalidEndpointConfig', 2), ('visitExpr', 2), ('logError', 2), ('mkDep', 2), ('replay', 1)]; let rec top: [('loop', 5), ('tryPrefix', 1), ('takeRest', 1)]

Lean where-helper names top: [('go', 437), ('visit', 44), ('loop', 32), ('process', 9), ('mkAlts', 8), ('go?', 8), ('visitApp', 7), ('doRealize', 7)]; let rec top: [('go', 68), ('loop', 65), ('visit', 27), ('parse', 7), ('attempt', 4), ('traverse', 3)]

Batteries where-helper names top: [('loop', 21), ('go', 20), ('trailingZeros', 2), ('visit', 2), ('isAutofillable', 1), ('collectFields', 1), ('aux', 1), ('left', 1)]; let rec top: [('go', 14), ('foo', 1), ('visitExpr', 1)]

Mathlib where-helper names top: [('go', 42), ('loop', 5), ('mkAlts', 4), ('aux', 3), ('forSide', 3), ('delabInsertArray', 2), ('step', 2), ('makeRHS', 2)]; let rec top: [('ratArm', 5), ('intArm', 4), ('loop', 3), ('nnratArm', 3), ('aux', 2), ('reduce', 1)]

Wild where-helper names top: [('go', 11), ('loop', 11), ('rest', 3), ('concat', 1), ('simple', 1), ('hexEscape', 1), ('unicodeEscape', 1), ('hexNumberVariable', 1)]; let rec top: [('go₂', 1), ('go₁', 1), ('loop', 1)]

- `go` is the dominant helper name everywhere (43–60% of helpers in Init/Std/Batteries), then `loop`; `let rec` prefers `loop` in Init (56 of 101). Lean uses `where` helpers heavily (6.8/k) and also `visit`.
- Private top-level defs are the other helper style: 17% of Lean defs and 9.1% of Std defs are `private`, versus 0.1% in Lake (Lake keeps helpers non-public by not marking them `public`; see section 10).
- Examples: `where go` on the same line as the first helper, [Init/Data/Array/Basic.lean L2057-L2059](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/Array/Basic.lean#L2057-L2059); `let rec loop`, [Init/Prelude.lean L3541-L3549](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Prelude.lean#L3541-L3549); `where finally`, [Init/Data/Char/Basic.lean L155-L161](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/Char/Basic.lean#L155-L161) (13 uses in Init, 2 Std, 3 Lean, 13 Mathlib, by `rg -c '^\s*where finally\b'`).

Caveats: this run predates a script fix that also recognises a trailing `… := body where` on the declaration line (≈108 such lines across core/Batteries/Mathlib by rg, e.g. `setTR` above), so `where` counts are slight undercounts; re-running `survey.py helpers` picks them up. A few body lines can still be misread as helper names (e.g. `throwError` ×5 in Lean).

## 4. Formatting

Script: `survey.py format` (`s_format`). Line length in code points over nonblank raw lines (comments included). Indentation deltas compare consecutive code lines. Match layout looks at `match … with` at end of line followed by a `|` line. Header analysis uses the declaration header (from the keyword line up to `:=`, a trailing `where`, a following `|` line, or a return to top level).

#### line length (code points, nonblank raw lines incl. comments)
| col | p50 | p95 | p99 | max | >100 | >120 | lines with tab | trailing ws |
|---|---|---|---|---|---|---|---|---|
| Init | 43 | 99 | 120 | 359 | 7000 (3.9%) | 1671 (0.9%) | 0 | 0 |
| Std | 42 | 94 | 109 | 279 | 3162 (1.9%) | 851 (0.5%) | 0 | 0 |
| Lake | 39 | 86 | 100 | 186 | 267 (1.0%) | 28 (0.1%) | 0 | 0 |
| Lean | 40 | 98 | 125 | 654 | 10146 (4.0%) | 3265 (1.3%) | 0 | 3 |
| Batteries | 46 | 92 | 98 | 140 | 1 (0.0%) | 1 (0.0%) | 0 | 0 |
| Mathlib | 49 | 94 | 99 | 224 | 430 (0.0%) | 213 (0.0%) | 0 | 0 |
| Wild | 37 | 103 | 137 | 228 | 722 (5.5%) | 277 (2.1%) | 0 | 0 |

#### indentation (code lines; deltas = increase from previous code line)
| col | odd indent | +2 | +4 | other increase |
|---|---|---|---|---|
| Init | 0.3% | 65.7% | 33.3% | 1.0% |
| Std | 0.2% | 47.3% | 52.3% | 0.5% |
| Lake | 0.4% | 96.8% | 1.2% | 2.1% |
| Lean | 0.7% | 95.0% | 3.5% | 1.5% |
| Batteries | 0.3% | 70.2% | 28.6% | 1.2% |
| Mathlib | 0.2% | 64.9% | 33.8% | 1.3% |
| Wild | 0.1% | 98.9% | 0.9% | 0.2% |

#### `match ... with` followed by `|` arms on the next line
| col | match starts line: n | `|` = match col | `|` +2 | match mid-line: n | `|` = line indent | `|` = line indent+2 | `|` under `match` | `match … with |` inline | arms with padded `=>` (aligned) |
|---|---|---|---|---|---|---|---|---|---|
| Init | 1203 | 99.8% | 0.1% | 194 | 11.9% | 82.5% | 0.0% | 67 | 673/8229 (8.2%) |
| Std | 653 | 99.4% | 0.6% | 147 | 5.4% | 90.5% | 0.0% | 18 | 155/4065 (3.8%) |
| Lake | 358 | 99.7% | 0.0% | 8 | 0.0% | 100.0% | 0.0% | 11 | 178/1412 (12.6%) |
| Lean | 3715 | 98.8% | 1.0% | 584 | 10.3% | 85.6% | 1.0% | 56 | 3709/19083 (19.4%) |
| Batteries | 265 | 100.0% | 0.0% | 88 | 30.7% | 68.2% | 0.0% | 17 | 104/1895 (5.5%) |
| Mathlib | 1739 | 97.1% | 2.9% | 353 | 22.1% | 72.2% | 0.8% | 157 | 238/22517 (1.1%) |
| Wild | 174 | 99.4% | 0.0% | 2 | 0.0% | 100.0% | 0.0% | 0 | 8/1252 (0.6%) |

#### `|` lines directly after a def/abbrev/instance header (equation compiler) and after `inductive`
| col | def arms: n | +2 | +0 | other | inductive ctors: n | +2 | +0 | other |
|---|---|---|---|---|---|---|---|---|
| Init | 463 | 98.7% | 0.9% | 0.4% | 95 | 98.9% | 1.1% | 0.0% |
| Std | 215 | 99.1% | 0.9% | 0.0% | 84 | 97.6% | 2.4% | 0.0% |
| Lake | 63 | 12.7% | 87.3% | 0.0% | 42 | 23.8% | 76.2% | 0.0% |
| Lean | 1048 | 98.2% | 1.2% | 0.6% | 411 | 98.5% | 1.5% | 0.0% |
| Batteries | 174 | 98.3% | 1.7% | 0.0% | 26 | 100.0% | 0.0% | 0.0% |
| Mathlib | 1326 | 98.7% | 1.0% | 0.3% | 342 | 95.3% | 4.7% | 0.0% |
| Wild | 49 | 95.9% | 4.1% | 0.0% | 30 | 96.7% | 3.3% | 0.0% |

#### declaration headers split over lines
| col | multi-line headers | 2nd line +4 | 2nd line +2 | other | header line starting `:` | header line ending ` :` | bodies after `:=`/`:= by`/`:= do` EOL | body +2 | body other |
|---|---|---|---|---|---|---|---|---|---|
| Init | 12591 | 98.1% | 1.2% | 0.7% | 360 | 10454 | 20449 | 99.5% | 0.5% |
| Std | 19720 | 98.8% | 1.0% | 0.2% | 25 | 17805 | 23400 | 99.6% | 0.4% |
| Lake | 424 | 10.6% | 87.2% | 2.3% | 202 | 21 | 1873 | 96.3% | 3.7% |
| Lean | 1737 | 93.8% | 5.6% | 0.6% | 159 | 500 | 12551 | 99.4% | 0.6% |
| Batteries | 1363 | 97.6% | 1.8% | 0.6% | 4 | 1075 | 1838 | 99.7% | 0.3% |
| Mathlib | 128234 | 99.6% | 0.3% | 0.1% | 5 | 106694 | 194619 | 99.8% | 0.2% |
| Wild | 456 | 0.2% | 99.8% | 0.0% | 5 | 413 | 1039 | 99.8% | 0.2% |

- Match arms: when `match` starts its line, arms sit at the `match` column in 97–100% of cases in every column (as `style.md` prescribes); when `match` is mid-line (`let x ← match …`, `| a => match …`), arms go at line indent +2 (68–100%). Aligned `=>` (padding before `=>`) is a minority style: 19% of arms in Lean, 8% Init, 4% Std, 1% Mathlib. Example of aligned arms: [Init/Prelude.lean L3543-L3547](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Prelude.lean#L3543-L3547).
- Signatures: Init/Std/Lean/Batteries/Mathlib continue headers at +4 (94–99.6%) and bodies at +2 (99%+). In Init/Std/Batteries/Mathlib the colon ends the first header line (` :` at end of line in 10,454 Init and 17,805 Std headers); Init still has 360 headers with a line starting with `:` (older code, e.g. [Init/Control/Lawful/Instances.lean L51-L56](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Control/Lawful/Instances.lean#L51-L56)).
- Lake: binders at +2 and `: T :=` at column 0, e.g. [lake/Lake/Build/Common.lean L138-L140](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Build/Common.lean#L138-L140) and [lake/Lake/Build/Topological.lean L76-L78](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Build/Topological.lean#L76-L78); equation arms at column 0, [lake/Lake/Load/Toml.lean L116-L120](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Load/Toml.lean#L116-L120).
- The wild libraries put header continuations at +2 (99.8%).
- Indentation is even in ≥99.3% of code lines everywhere; increases are +2 or +4 in ≥98%.

Caveats: line length counts docstring/comment lines too (URLs in docs inflate the tail); `match` detection ignores `match` whose `with` is not at end of line (counted separately as inline) and `induction … with`/`cases … with`.

## 5. `do` notation

Script: `survey.py do` (`s_do`), program code only (theorem/example extents excluded).

| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| `do` | 263 (1.47) | 861 (5.30) | 1341 (49.66) | 18813 (73.60) | 448 (18.18) | 4159 (2.21) | 220 (16.80) |
| `Id.run do` | 10 (0.06) | 39 (0.24) | 23 (0.85) | 418 (1.64) | 12 (0.49) | 59 (0.03) | 17 (1.30) |
| `let mut` | 12 (0.07) | 78 (0.48) | 115 (4.26) | 2103 (8.23) | 80 (3.25) | 422 (0.22) | 22 (1.68) |
| `for … in` | 11 (0.06) | 58 (0.36) | 114 (4.22) | 2057 (8.05) | 77 (3.13) | 428 (0.23) | 14 (1.07) |
| `while` | 1 (0.01) | 14 (0.09) | 0 (0.00) | 103 (0.40) | 1 (0.04) | 9 (0.00) | 1 (0.08) |
| `repeat` (term/do) | 3 (0.02) | 3 (0.02) | 1 (0.04) | 64 (0.25) | 0 (0.00) | 51 (0.03) | 2 (0.15) |
| `break` | 3 (0.02) | 22 (0.14) | 0 (0.00) | 123 (0.48) | 0 (0.00) | 15 (0.01) | 2 (0.15) |
| `continue` | 4 (0.02) | 19 (0.12) | 11 (0.41) | 288 (1.13) | 16 (0.65) | 107 (0.06) | 2 (0.15) |
| `return` | 147 (0.82) | 560 (3.45) | 867 (32.11) | 16242 (63.54) | 329 (13.35) | 3123 (1.66) | 183 (13.97) |
| `pure` | 391 (2.19) | 301 (1.85) | 134 (4.96) | 3037 (11.88) | 196 (7.95) | 1337 (0.71) | 72 (5.50) |
| guard return `then return`/`do return` | 27 (0.15) | 147 (0.90) | 226 (8.37) | 4194 (16.41) | 107 (4.34) | 686 (0.36) | 34 (2.60) |
| `(← …)` nested action | 103 (0.58) | 268 (1.65) | 575 (21.30) | 13043 (51.03) | 227 (9.21) | 2255 (1.20) | 62 (4.73) |
| `←` total | 431 (2.41) | 975 (6.00) | 1859 (68.85) | 31338 (122.60) | 659 (26.75) | 18146 (9.64) | 200 (15.27) |
| `<-` ASCII | 0 (0.00) | 0 (0.00) | 0 (0.00) | 3 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `unless` | 1 (0.01) | 4 (0.02) | 109 (4.04) | 1703 (6.66) | 46 (1.87) | 324 (0.17) | 0 (0.00) |
| `if let` | 16 (0.09) | 82 (0.50) | 289 (10.70) | 2574 (10.07) | 74 (3.00) | 497 (0.26) | 6 (0.46) |
| `if h :` | 286 (1.60) | 212 (1.31) | 96 (3.56) | 532 (2.08) | 62 (2.52) | 608 (0.32) | 39 (2.98) |
| `match ← `/`match (← ` | 49 (0.27) | 47 (0.29) | 73 (2.70) | 633 (2.48) | 33 (1.34) | 216 (0.11) | 22 (1.68) |
| `let some x ← … |` (let-else) | 1 (0.01) | 3 (0.02) | 11 (0.41) | 943 (3.69) | 4 (0.16) | 199 (0.11) | 1 (0.08) |
| `let … := … |` (pure let-else) | 0 (0.00) | 10 (0.06) | 15 (0.56) | 811 (3.17) | 33 (1.34) | 252 (0.13) | 0 (0.00) |
| `try` | 15 (0.08) | 36 (0.22) | 47 (1.74) | 564 (2.21) | 10 (0.41) | 216 (0.11) | 6 (0.46) |
| `catch` | 1 (0.01) | 18 (0.11) | 44 (1.63) | 463 (1.81) | 10 (0.41) | 178 (0.09) | 6 (0.46) |
| `finally` | 21 (0.12) | 19 (0.12) | 4 (0.15) | 101 (0.40) | 0 (0.00) | 22 (0.01) | 0 (0.00) |

#### line-initial `return` followed by less-indented continuing code (≈ early return, approximate)
| col | count (per k) |
|---|---|
| Init | 10 (0.06) |
| Std | 76 (0.47) |
| Lake | 143 (5.30) |
| Lean | 2365 (9.25) |
| Batteries | 53 (2.15) |
| Mathlib | 637 (0.34) |
| Wild | 34 (2.60) |

- Lake and Lean are the imperative codebases: per kLOC, `return` 32/64, `(← …)` 21/51, `let mut` 4.3/8.2, `for … in` 4.2/8.1, `unless` 4.0/6.7, `if let` 10.7/10.1. Init/Std program code is mostly pure functional (`do` 1.5/k and 5.3/k).
- Early return in guard form (`if … then return …`) is 8.4/k in Lake, 16/k in Lean; `let some x ← e | alt` (let-else) is a Lean-elaborator idiom (943 of the ~1,160 occurrences across columns).
- `<-` (ASCII) is essentially absent (3 occurrences in Lean, 0 elsewhere in program code).
- Example of let-else: [Lean/Elab/BuiltinNotation.lean L379-L381](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Lean/Elab/BuiltinNotation.lean#L379-L381) (`let some stx ← liftMacroM <| expandCDotArg? stx | pure none`). `style.md` shows the same pattern and asks for early `return` "to reduce nesting depth".

Caveats: `for … in` also matches `for` inside docstring-free term syntax such as `deriving instance … for` (rare); the multi-line early-return heuristic is approximate (a `return` ending a `where` helper followed by another helper is miscounted).

## 6. Error handling

Script: `survey.py errors` (`s_errors`).

| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| `Except` (type/namespace) | 133 (0.74) | 114 (0.70) | 87 (3.22) | 345 (1.35) | 11 (0.45) | 35 (0.02) | 14 (1.07) |
| `ExceptT` | 72 (0.40) | 26 (0.16) | 6 (0.22) | 40 (0.16) | 2 (0.08) | 22 (0.01) | 1 (0.08) |
| `EIO` | 57 (0.32) | 27 (0.17) | 21 (0.78) | 47 (0.18) | 10 (0.41) | 2 (0.00) | 0 (0.00) |
| `IO` (type) | 98 (0.55) | 208 (1.28) | 113 (4.19) | 537 (2.10) | 16 (0.65) | 21 (0.01) | 20 (1.53) |
| `IO.Error` | 43 (0.24) | 50 (0.31) | 1 (0.04) | 23 (0.09) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `.userError` | 11 (0.06) | 37 (0.23) | 20 (0.74) | 124 (0.49) | 1 (0.04) | 3 (0.00) | 0 (0.00) |
| `throw` | 75 (0.42) | 84 (0.52) | 169 (6.26) | 520 (2.03) | 3 (0.12) | 60 (0.03) | 38 (2.90) |
| `throwError` | 3 (0.02) | 0 (0.00) | 14 (0.52) | 1642 (6.42) | 41 (1.66) | 725 (0.39) | 0 (0.00) |
| `MonadExcept` | 11 (0.06) | 3 (0.02) | 0 (0.00) | 31 (0.12) | 0 (0.00) | 2 (0.00) | 0 (0.00) |
| `Option` (type) | 635 (3.56) | 847 (5.21) | 389 (14.41) | 3617 (14.15) | 204 (8.28) | 1209 (0.64) | 146 (11.15) |
| `panic!` | 24 (0.13) | 45 (0.28) | 5 (0.19) | 224 (0.88) | 16 (0.65) | 66 (0.04) | 5 (0.38) |
| `unreachable!` | 1 (0.01) | 2 (0.01) | 4 (0.15) | 480 (1.88) | 6 (0.24) | 35 (0.02) | 2 (0.15) |
| `assert!` | 2 (0.01) | 2 (0.01) | 0 (0.00) | 275 (1.08) | 0 (0.00) | 3 (0.00) | 0 (0.00) |
| `dbg_trace`/`dbgTrace` | 4 (0.02) | 0 (0.00) | 0 (0.00) | 21 (0.08) | 0 (0.00) | 8 (0.00) | 2 (0.15) |
| `sorry` | 1 (0.01) | 0 (0.00) | 0 (0.00) | 16 (0.06) | 0 (0.00) | 4 (0.00) | 0 (0.00) |
| `.get!` | 34 (0.19) | 82 (0.50) | 17 (0.63) | 222 (0.87) | 17 (0.69) | 35 (0.02) | 23 (1.76) |
| `.getD` | 39 (0.22) | 120 (0.74) | 94 (3.48) | 462 (1.81) | 34 (1.38) | 149 (0.08) | 7 (0.53) |
| `.get?` | 11 (0.06) | 96 (0.59) | 53 (1.96) | 194 (0.76) | 2 (0.08) | 38 (0.02) | 1 (0.08) |
| `[i]!` | 5 (0.03) | 7 (0.04) | 47 (1.74) | 1521 (5.95) | 14 (0.57) | 280 (0.15) | 5 (0.38) |
| `[i]?` | 10 (0.06) | 19 (0.12) | 151 (5.59) | 1022 (4.00) | 44 (1.79) | 181 (0.10) | 18 (1.37) |
| `[i]'h` | 21 (0.12) | 51 (0.31) | 9 (0.33) | 10 (0.04) | 3 (0.12) | 3 (0.00) | 1 (0.08) |
| other `x!` calls | 127 (0.71) | 792 (4.88) | 78 (2.89) | 2581 (10.10) | 67 (2.72) | 4665 (2.48) | 89 (6.79) |
| `Inhabited` (derive/inst/binder) | 175 (0.98) | 420 (2.59) | 93 (3.44) | 862 (3.37) | 44 (1.79) | 1358 (0.72) | 46 (3.51) |

#### same accessors inside theorem/example declarations
| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| `Option` (type) | 1512 (8.47) | 3230 (19.88) | 0 (0.00) | 1 (0.00) | 99 (4.02) | 1237 (0.66) | 50 (3.82) |
| `.get!` | 21 (0.12) | 2159 (13.29) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `.getD` | 146 (0.82) | 1763 (10.85) | 0 (0.00) | 0 (0.00) | 13 (0.53) | 117 (0.06) | 1 (0.08) |
| `.get?` | 31 (0.17) | 3071 (18.90) | 0 (0.00) | 0 (0.00) | 2 (0.08) | 215 (0.11) | 0 (0.00) |
| `[i]!` | 142 (0.80) | 370 (2.28) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 2 (0.00) | 0 (0.00) |
| `[i]?` | 743 (4.16) | 926 (5.70) | 0 (0.00) | 2 (0.01) | 28 (1.14) | 104 (0.06) | 1 (0.08) |
| `[i]'h` | 353 (1.98) | 455 (2.80) | 0 (0.00) | 0 (0.00) | 17 (0.69) | 44 (0.02) | 24 (1.83) |
| other `x!` calls | 274 (1.53) | 6616 (40.73) | 0 (0.00) | 4 (0.02) | 24 (0.97) | 6085 (3.23) | 18 (1.37) |

- In program code, Lean leans on `throwError` (6.4/k), `unreachable!` (1.9/k), `assert!` (1.1/k), `panic!` (0.9/k) and `xs[i]!` (6.0/k). Lake uses `throw` (6.3/k), `Except` (3.2/k) and `xs[i]?` (5.6/k), with almost no `panic!` (5) or `unreachable!` (4). Init/Std program code uses few panicking forms; Std's `!` volume is in theorem statements (2,159 `.get!` and 6,616 other `x!` in theorems vs 82 and 792 in programs): the `!` variants exist so that lemmas about them can be stated.
- `[i]'h` (index with an explicit proof) is used in Init/Std programs (21/51) and almost never in Lake/Lean (9/10).
- `sorry` hits in library code are syntax/macro definitions of `sorry` itself (spot-checked in Init: `macro "sorry" : tactic …`), not unfinished proofs.
- Example: Std's `get!` documents its panic and points to notation ([Std/Data/HashMap/Basic.lean L161-L167](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/HashMap/Basic.lean#L161-L167)).

Caveats: `IO (type)` excludes `IO.` qualified names; "other `x!` calls" excludes `panic! unreachable! assert! s! m! f!` but still includes macros such as `dbg_trace!`-like names; `Option` counts every mention (types, `Option.map`, …).

## 7. Termination

Script: `survey.py termination` (`s_termination`). `partial`/`unsafe`/`nonrec` come from parsed modifiers; the denominator is defs+abbrevs+opaques+instances.

| col | defs+instances | `partial` | `termination_by` (per k) | … `structural` | `decreasing_by` (per k) | `partial_fixpoint` | `unsafe` decls | `implemented_by` | `nonrec` | `fuel` tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| Init | 7038 | 49 (0.7%) | 105 (0.59) | 6 | 50 (0.28) | 0 | 63 (0.9%) | 35 | 0 | 154 |
| Std | 5995 | 62 (1.0%) | 122 (0.75) | 0 | 5 (0.03) | 0 | 2 (0.0%) | 2 | 0 | 0 |
| Lake | 3045 | 51 (1.7%) | 5 (0.19) | 0 | 2 (0.07) | 0 | 7 (0.2%) | 5 | 21 | 0 |
| Lean | 19167 | 1484 (7.7%) | 37 (0.14) | 0 | 1 (0.00) | 0 | 205 (1.1%) | 127 | 4 | 23 |
| Batteries | 1288 | 61 (4.7%) | 45 (1.83) | 0 | 5 (0.20) | 0 | 12 (0.9%) | 7 | 4 | 0 |
| Mathlib | 65137 | 283 (0.4%) | 99 (0.05) | 5 | 37 (0.02) | 0 | 35 (0.1%) | 0 | 622 | 41 |
| Wild | 792 | 22 (2.8%) | 25 (1.91) | 0 | 1 (0.08) | 0 | 0 (0.0%) | 0 | 0 | 0 |

- `partial_fixpoint` occurs in no library file (only in 26 test files under `lean4/tests`).
- Std uses `termination_by` (122) with almost no `decreasing_by` (5); Init needs `decreasing_by` more often (50). Example: [Std/Data/DTreeMap/Internal/Operations.lean L225-L239](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DTreeMap/Internal/Operations.lean#L225-L239) (`termination_by sizeOf l + sizeOf r`, unindented as `style.md` asks).
- `partial` in Lake is used for genuinely non-terminating fetch loops, e.g. [lake/Lake/Build/Topological.lean L76-L78](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Build/Topological.lean#L76-L78) (`@[specialize] public partial def recFetch`), followed by a module doc explaining why.
- `unsafe` + `implemented_by` pairs: [Init/Dynamic.lean L97-L101](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Dynamic.lean#L97-L101) (`@[implemented_by Dynamic.get?Impl] opaque Dynamic.get? …`, `private unsafe def Dynamic.mkImpl`).
- Mathlib's 622 `nonrec` are `nonrec theorem` used to reuse a root name inside a namespace, not a termination device.

Caveat: "structural recursion" is not measured directly (it is the default when no annotation is present).

## 8. Data modelling

Script: `survey.py data` (`s_data`). "≈type" counts `abbrev`/`def` with an UpperCamel name.

| col | structure | inductive | class | class inductive | abbrev | abbrev UpperCamel (≈type) | def UpperCamel (≈type) | instances | named instances | named `inst…` | deriving clauses |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Init | 188 | 108 | 289 | 1 | 367 | 88 | 74 | 2577 | 411 (15.9%) | 302 | 128 |
| Std | 301 | 88 | 46 | 0 | 123 | 89 | 109 | 1411 | 114 (8.1%) | 103 | 173 |
| Lake | 128 | 42 | 45 | 0 | 305 | 146 | 9 | 516 | 5 (1.0%) | 1 | 93 |
| Lean | 1478 | 412 | 69 | 0 | 836 | 537 | 96 | 1225 | 9 (0.7%) | 4 | 998 |
| Batteries | 42 | 26 | 16 | 0 | 42 | 13 | 51 | 192 | 9 (4.7%) | 8 | 17 |
| Mathlib | 1712 | 344 | 1999 | 7 | 3684 | 920 | 2477 | 27793 | 12172 (43.8%) | 3452 | 352 |
| Wild | 32 | 30 | 13 | 0 | 21 | 16 | 36 | 98 | 2 (2.0%) | 0 | 33 |

#### derived classes (top 12)
- Init: Inhabited 46, SizeOf 37, BEq 29, DecidableEq 25, Repr 25, ReflBEq 9, LawfulBEq 9, Hashable 9, @[expose] 5, Nonempty 2, Ord 2
- Std: Repr 124, Inhabited 105, DecidableEq 70, BEq 31, LE 20, LT 20, Nonempty 12, Hashable 12, Add 9, Sub 9, Neg 9, ToString 9
- Lake: Inhabited 69, Repr 38, DecidableEq 21, Ord 6, Nonempty 4, TypeName 4, ToJson 4, FromJson 4, Hashable 3, BEq 3, Lean.ToJson 2, Lean.FromJson 1
- Lean: Inhabited 644, ToJson 232, FromJson 221, BEq 179, Repr 145, Hashable 78, TypeName 50, Nonempty 30, DecidableEq 28, Ord 19, RpcEncodable 13, EmptyCollection 7
- Batteries: Inhabited 10, Repr 6, DecidableEq 2, Nonempty 1
- Mathlib: Inhabited 153, DecidableEq 56, BEq 31, Category 15, Repr 15, CommRing 14, ToExpr 13, Module 12, AddCommMonoid 11, Algebra 11, AddCommGroup 10, TopologicalSpace 10
- Wild: Inhabited 27, Repr 24, DecidableEq 14, Lean.ToExpr 8, BEq 6, ToString 1

- Instances are mostly anonymous in core (named: Init 16%, Std 8%, Lake 1%, Lean 0.7%); Mathlib names 44%. Named core instances use the `inst…` scheme (e.g. [Init/Prelude.lean L1418](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Prelude.lean#L1418) `instance instOfNatNat (n : Nat) : OfNat Nat n where`).
- Lake defines types with `abbrev` more than any other column (146 UpperCamel abbrevs, e.g. [lake/Lake/Util/Binder.lean L15-L17](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Util/Binder.lean#L15-L17)).
- `deriving` clauses are unindented (as `style.md` asks), e.g. [lake/Lake/Config/Dependency.lean L44](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Config/Dependency.lean#L44) `deriving Inhabited, Repr`. Lean derives `ToJson`/`FromJson` heavily (LSP types).

Caveats: `Init`'s "`@[expose]` 5" in the derived-class list is a parsing artifact (`deriving @[expose] …`); "def UpperCamel" includes Prop-valued defs and type families.

## 9. Attributes

Script: `survey.py attrs` (`s_attrs`): every `@[…]` block and `attribute […]` command in code, split at top-level commas; `local`/`scoped` prefixes counted separately.

| attribute (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| `inline` | 1193 (6.68) | 2499 (15.38) | 828 (30.67) | 971 (3.80) | 318 (12.91) | 60 (0.03) | 136 (10.38) |
| `always_inline` | 333 (1.86) | 68 (0.42) | 35 (1.30) | 40 (0.16) | 1 (0.04) | 0 (0.00) | 1 (0.08) |
| `noinline` | 10 (0.06) | 0 (0.00) | 1 (0.04) | 15 (0.06) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `macro_inline` | 33 (0.18) | 0 (0.00) | 10 (0.37) | 3 (0.01) | 2 (0.08) | 229 (0.12) | 4 (0.31) |
| `specialize` | 157 (0.88) | 68 (0.42) | 20 (0.74) | 133 (0.52) | 84 (3.41) | 24 (0.01) | 7 (0.53) |
| `simp` | 9626 (53.90) | 4081 (25.12) | 11 (0.41) | 9 (0.04) | 703 (28.53) | 43631 (23.18) | 101 (7.71) |
| `grind` | 2624 (14.69) | 3164 (19.48) | 0 (0.00) | 0 (0.00) | 239 (9.70) | 812 (0.43) | 202 (15.42) |
| `extern` | 686 (3.84) | 101 (0.62) | 1 (0.04) | 243 (0.95) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `implemented_by` | 35 (0.20) | 2 (0.01) | 5 (0.19) | 124 (0.49) | 7 (0.28) | 0 (0.00) | 0 (0.00) |
| `csimp` | 66 (0.37) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 19 (0.77) | 9 (0.00) | 0 (0.00) |
| `reducible` | 40 (0.22) | 0 (0.00) | 9 (0.33) | 5 (0.02) | 6 (0.24) | 112 (0.06) | 7 (0.53) |
| `irreducible` | 9 (0.05) | 3 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 46 (0.02) | 0 (0.00) |
| `semireducible` | 19 (0.11) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 2 (0.00) | 0 (0.00) |
| `expose` | 810 (4.54) | 343 (2.11) | 33 (1.22) | 244 (0.95) | 277 (11.24) | 5243 (2.79) | 28 (2.14) |
| `inherit_doc` | 177 (0.99) | 963 (5.93) | 109 (4.04) | 90 (0.35) | 30 (1.22) | 823 (0.44) | 4 (0.31) |
| `export` | 65 (0.36) | 0 (0.00) | 0 (0.00) | 146 (0.57) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `instance` | 86 (0.48) | 38 (0.23) | 1 (0.04) | 0 (0.00) | 0 (0.00) | 1234 (0.66) | 0 (0.00) |
| `ext` | 30 (0.17) | 26 (0.16) | 0 (0.00) | 0 (0.00) | 12 (0.49) | 1278 (0.68) | 6 (0.46) |
| `deprecated` | 582 (3.26) | 142 (0.87) | 36 (1.33) | 21 (0.08) | 47 (1.91) | 3897 (2.07) | 2 (0.15) |
| `builtin_doc` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 178 (0.70) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `spec` | 1 (0.01) | 294 (1.81) | 0 (0.00) | 1 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `simps` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 4797 (2.55) | 0 (0.00) |
| `to_additive` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 16543 (8.79) | 0 (0.00) |
| `match_pattern` | 17 (0.10) | 2 (0.01) | 22 (0.81) | 32 (0.13) | 1 (0.04) | 82 (0.04) | 0 (0.00) |
| `never_extract` | 19 (0.11) | 4 (0.02) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `init` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `builtin_init` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 3 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `elab_as_elim` | 42 (0.24) | 29 (0.18) | 0 (0.00) | 0 (0.00) | 7 (0.28) | 450 (0.24) | 1 (0.08) |
| `induction_eliminator` | 3 (0.02) | 2 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 69 (0.04) | 0 (0.00) |
| `cases_eliminator` | 3 (0.02) | 2 (0.01) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 55 (0.03) | 1 (0.08) |
| `wf_preprocess` | 58 (0.32) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `congr` | 62 (0.35) | 7 (0.04) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 33 (0.02) | 0 (0.00) |
| `norm_cast` | 46 (0.26) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 1 (0.04) | 2216 (1.18) | 0 (0.00) |
| `aesop` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 338 (0.18) | 0 (0.00) |
| `nospecialize` | 3 (0.02) | 3 (0.02) | 5 (0.19) | 1 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `local` | 193 (1.08) | 10 (0.06) | 1 (0.04) | 4 (0.02) | 7 (0.28) | 1171 (0.62) | 0 (0.00) |
| `scoped` | 6 (0.03) | 2 (0.01) | 1 (0.04) | 0 (0.00) | 0 (0.00) | 107 (0.06) | 0 (0.00) |

#### grind variants (top 10)
- Init: `=` 2350, `_=_` 92, `hom` 57, `←` 50, `→` 29, `.` 13, `ext` 7, `hom_pred` 6, `<=` 4, `(plain)` 4
- Std: `=` 2960, `_=_` 108, `=_` 66, `norm` 10, `←` 9, `ext` 6, `→` 5
- Lake: 
- Lean: 
- Batteries: `=` 199, `.` 23, `=_` 7, `←` 6, `→` 2, `(plain)` 1, `=>` 1
- Mathlib: `=` 607, `.` 54, `←` 47, `→` 40, `_=_` 16, `(plain)` 12, `ext` 12, `inj` 8, `=>` 6, `<=` 4
- Wild: `=` 121, `=>` 31, `→` 26, `.` 14, `(plain)` 9, `_=_` 1

#### other modifiers (decl counts)
| col | `unsafe` decls | `noncomputable` decls | `noncomputable section` | `attribute [..]` cmds | `(priority := …)` |
|---|---|---|---|---|---|
| Init | 63 | 250 | 0 | 333 | 84 |
| Std | 2 | 46 | 0 | 187 | 7 |
| Lake | 7 | 1 | 0 | 7 | 28 |
| Lean | 205 | 0 | 0 | 16 | 29 |
| Batteries | 12 | 3 | 0 | 30 | 6 |
| Mathlib | 35 | 7640 | 1160 | 2883 | 1564 |
| Wild | 0 | 2 | 0 | 13 | 0 |

- `@[inline]` is the main performance attribute (Lake 31/k, Std 15/k, Batteries 13/k); `@[specialize]` is much rarer (0.4–0.9/k core, 3.4/k Batteries). `@[extern]` is concentrated in Init (686); `@[csimp]` only in Init (66) and Batteries (19).
- `@[grind]` is already as frequent as `@[simp]` in Std (3,164 vs 4,081) and dominated by the `grind =` variant (94% in Std); Lake and Lean use neither.
- `@[expose]` (module system: export the body) is used 810 times in Init and 277 in Batteries, besides file-level `@[expose] public section`.
- `@[spec]` appears 294 times in Std (its purpose was not checked).

Caveat: `simp ←`/`grind =` variants are taken from the first token after the attribute name only.

## 10. Visibility, scoping, file layout

Script: `survey.py visibility` (`s_visibility`).

| col | decls | `private` | `protected` | explicit `public` | effectively public (est.) | files with `public section` | files with `@[expose] public section` |
|---|---|---|---|---|---|---|---|
| Init | 32290 | 465 (1.4%) | 3088 (9.6%) | 1022 (3.2%) | 31445 (97.4%) | 525 | 60 |
| Std | 27368 | 574 (2.1%) | 74 (0.3%) | 533 (1.9%) | 26618 (97.3%) | 404 | 241 |
| Lake | 3292 | 3 (0.1%) | 209 (6.3%) | 2510 (76.2%) | 2513 (76.3%) | 2 | 0 |
| Lean | 21229 | 3192 (15.0%) | 175 (0.8%) | 991 (4.7%) | 15906 (74.9%) | 928 | 1 |
| Batteries | 3394 | 76 (2.2%) | 137 (4.0%) | 24 (0.7%) | 3241 (95.5%) | 149 | 0 |
| Mathlib | 260489 | 2399 (0.9%) | 8526 (3.3%) | 369 (0.1%) | 256884 (98.6%) | 8340 | 5014 |
| Wild | 1515 | 71 (4.7%) | 13 (0.9%) | 43 (2.8%) | 1120 (73.9%) | 62 | 0 |

| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| top-level `open X` (not `in`) | 313 (1.75) | 375 (2.31) | 146 (5.41) | 898 (3.51) | 80 (3.25) | 13219 (7.02) | 142 (10.84) |
| `open … in` (line ends `in` or `in decl`) | 82 (0.46) | 69 (0.42) | 11 (0.41) | 263 (1.03) | 10 (0.41) | 2528 (1.34) | 19 (1.45) |
| indented `open … in` (inside terms) | 49 (0.27) | 2 (0.01) | 0 (0.00) | 10 (0.04) | 0 (0.00) | 88 (0.05) | 15 (1.15) |
| `open scoped` | 20 (0.11) | 5 (0.03) | 0 (0.00) | 4 (0.02) | 0 (0.00) | 3648 (1.94) | 0 (0.00) |
| `namespace` | 904 (5.06) | 1356 (8.35) | 248 (9.18) | 1768 (6.92) | 212 (8.60) | 14705 (7.81) | 195 (14.89) |
| `section` | 737 (4.13) | 771 (4.75) | 6 (0.22) | 1022 (4.00) | 173 (7.02) | 26548 (14.10) | 85 (6.49) |
| `variable` | 321 (1.80) | 803 (4.94) | 11 (0.41) | 110 (0.43) | 27 (1.10) | 44711 (23.75) | 84 (6.41) |
| `universe` | 43 (0.24) | 117 (0.72) | 0 (0.00) | 12 (0.05) | 1 (0.04) | 2815 (1.50) | 0 (0.00) |
| `set_option … in` | 243 (1.36) | 42 (0.26) | 15 (0.56) | 299 (1.17) | 18 (0.73) | 11522 (6.12) | 3 (0.23) |
| top-level `set_option` | 320 (1.79) | 287 (1.77) | 9 (0.33) | 40 (0.16) | 4 (0.16) | 82 (0.04) | 1 (0.08) |
| `prelude` | 672 (3.76) | 499 (3.07) | 164 (6.07) | 1250 (4.89) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `public import` | 1777 (9.95) | 1359 (8.37) | 472 (17.48) | 3214 (12.57) | 206 (8.36) | 19923 (10.58) | 189 (14.43) |
| `public meta import` | 18 (0.10) | 6 (0.04) | 7 (0.26) | 39 (0.15) | 82 (3.33) | 550 (0.29) | 4 (0.31) |
| `meta import` | 7 (0.04) | 1 (0.01) | 33 (1.22) | 53 (0.21) | 2 (0.08) | 14 (0.01) | 4 (0.31) |
| plain `import` | 1699 (9.51) | 438 (2.70) | 292 (10.81) | 1859 (7.27) | 113 (4.59) | 3586 (1.90) | 152 (11.60) |
| `import all` | 225 (1.26) | 52 (0.32) | 5 (0.19) | 10 (0.04) | 32 (1.30) | 12 (0.01) | 83 (6.34) |

#### file size (nonblank lines per file)
| col | files | p50 | p90 | p99 | max | >1000 | >1500 |
|---|---|---|---|---|---|---|---|
| Init | 672 | 91 | 563 | 2545 | 6008 | 34 | 24 |
| Std | 499 | 102 | 540 | 4975 | 9051 | 28 | 21 |
| Lake | 164 | 82 | 373 | 1005 | 1616 | 3 | 1 |
| Lean | 1250 | 104 | 463 | 1619 | 2927 | 36 | 16 |
| Batteries | 194 | 59 | 321 | 979 | 1062 | 1 | 0 |
| Mathlib | 8642 | 144 | 511 | 1010 | 1265 | 90 | 0 |
| Wild | 132 | 60 | 227 | 486 | 1467 | 1 | 0 |

- Module system: every file has `module`; core files also have `prelude` (Init/Std/Lake/Lean 100%). Std/Init expose bodies file-wide with `@[expose] public section` (Std 241 files, Init 60; e.g. [Std/Data/HashMap/Basic.lean L12-L15](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/HashMap/Basic.lean#L12-L15), which also turns on `linter.missingDocs`). Lake marks declarations one by one ([lake/Lake/Config/Package.lean L28](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/Lake/Config/Package.lean#L28) `public structure Package where`).
- `protected` is an Init habit (9.6% of declarations) (why each name is protected was not checked).
- `open … in` is used 0.4–1.0/k in core, top-level `open` 1.8–5.4/k. `variable` is rare in Lake/Lean (0.4/k) and common in Std (4.9/k) and Mathlib (24/k).
- File size: median 59–144 nonblank lines; Std and Init have the biggest files (max 9,051 and 6,008; 21 and 24 files over 1,500 lines, mostly `Lemmas.lean`); Mathlib caps files at 1,500 by linter (max 1,265).

Caveat: "effectively public" depends on the scope tracker (namespace/section/mutual/end); files with unusual `end` usage could be misattributed.

## 11. Documentation

Script: `survey.py docs` (`s_docs`). A declaration is documented if a `/-- … -/` ends on the line before its first attribute line (or on the same line before the code). `@[inherit_doc]` is counted separately.

| col | public defs documented | public types documented | public theorems documented | public named instances documented | private defs documented | files with module doc | module docs per file | module docs starting with `#` |
|---|---|---|---|---|---|---|---|---|
| Init | 3154/4305 (73.3%) +74 inherit_doc | 490/578 (84.8%) +1 inherit_doc | 688/24043 (2.9%) +3 inherit_doc | 33/389 (8.5%) +0 inherit_doc | 14.1% | 278/672 (41.4%) | 1.77 | 85.4% |
| Std | 2898/4106 (70.6%) +923 inherit_doc | 320/404 (79.2%) +7 inherit_doc | 366/20700 (1.8%) +3 inherit_doc | 28/112 (25.0%) +0 inherit_doc | 36.4% | 321/499 (64.3%) | 1.23 | 71.4% |
| Lake | 1049/1886 (55.6%) +108 inherit_doc | 107/161 (66.5%) +0 inherit_doc | 3/19 (15.8%) +0 inherit_doc | 0/5 (0.0%) +0 inherit_doc | 22.7% | 75/164 (45.7%) | 1.25 | 96.1% |
| Lean | 5008/12909 (38.8%) +81 inherit_doc | 859/1734 (49.5%) +0 inherit_doc | 2/18 (11.1%) +0 inherit_doc | 0/9 (0.0%) +0 inherit_doc | 37.6% | 408/1250 (32.6%) | 0.43 | 45.1% |
| Batteries | 1002/1034 (96.9%) +25 inherit_doc | 77/77 (100.0%) +0 inherit_doc | 96/1939 (5.0%) +0 inherit_doc | 0/9 (0.0%) +0 inherit_doc | 46.8% | 86/194 (44.3%) | 1.02 | 95.4% |
| Mathlib | 35180/36276 (97.0%) +76 inherit_doc | 3964/4007 (98.9%) +4 inherit_doc | 28648/188413 (15.2%) +7 inherit_doc | 2291/12112 (18.9%) +2 inherit_doc | 72.6% | 8475/8642 (98.1%) | 1.51 | 95.4% |
| Wild | 336/547 (61.4%) +1 inherit_doc | 31/67 (46.3%) +0 inherit_doc | 5/412 (1.2%) +0 inherit_doc | 0/2 (0.0%) +0 inherit_doc | 6.8% | 6/132 (4.5%) | 0.14 | 94.4% |

#### def docstring form
| col | def docstrings | contain backticks | single-line | text starts on next line | end with period | start with code | top first words |
|---|---|---|---|---|---|---|---|
| Init | 3176 | 83.9% | 30.1% | 77.9% | 77.0% | 3.2% | Returns 340, Converts 282, The 201, Creates 116, Checks 109, A 99, Computes 93, Bitwise 71, Applies 59, Given 58 |
| Std | 3072 | 60.4% | 63.7% | 80.1% | 83.7% | 2.0% | Creates 247, Returns 225, Internal 199, Converts 157, Checks 116, The 104, Implementation 103, Parses 89, Tries 86, Adds 78 |
| Lake | 1195 | 57.2% | 72.8% | 26.9% | 97.1% | 1.1% | The 298, Returns 106, A 83, Whether 30, Build 28, Get 24, Run 21, Try 20, Fetch 20, Parse 17 |
| Lean | 6900 | 80.9% | 46.6% | 58.8% | 87.5% | 4.6% | Returns 662, Given 350, The 346, Return 332, A 184, If 158, Similar 122, Adds 102, Runs 101, Creates 99 |
| Batteries | 1031 | 79.7% | 59.1% | 36.7% | 84.2% | 28.1% | O 215, Returns 49, The 49, A 26, Get 18, Find 18, Fold 18, Convert 16, Encode 15, Decode 14 |
| Mathlib | 35955 | 75.9% | 53.4% | 4.5% | 91.4% | 8.8% | The 12584, A 3201, Given 2215, If 1995, An 836, Construct 451, Auxiliary 402, For 345, This 326, When 247 |
| Wild | 346 | 66.8% | 64.2% | 39.6% | 67.1% | 20.5% | parse 46, Finds 24, Checks 21, Parse 20, Converts 9, Creates 9, Renders 8, Prints 6, Parses 5, Inserts 5 |

- Docstring style: Init/Std def docs open with a third-person verb (top first words: "Returns", "Converts", "Creates", "Checks"), Lean mixes "Returns" and imperative "Return", Lake prefers "The …"/"Whether …" noun phrases, Mathlib "The …". Batteries opens 21% of def docs with a complexity tag (`` `O(n)`. Returns … ``, e.g. [Batteries/Lean/HashSet.lean L16-L17](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/Batteries/Lean/HashSet.lean#L16-L17)).
- Init/Std put the text on the line after `/--` (78–80%); Lake and Mathlib start on the `/--` line (Lake 27%, Mathlib 4.5% on the next line). Init docstrings carry `Examples:` bullets with backticked equations (84% contain backticks), e.g. [Init/Data/List/Basic.lean L361-L372](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Init/Data/List/Basic.lean#L361-L372).
- Module docs: 41% of Init files, 64% of Std, 46% of Lake, 33% of Lean, 98% of Mathlib have a `/-! -/`; most start with a `#` heading (Std 71%, Lake 96%). Example with heading and cross-references: [Std/Data/HashMap/Basic.lean L17-L31](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/HashMap/Basic.lean#L17-L31).

Caveats: coverage counts only declarations the parser sees; docstrings attached via `add_decl_doc` or generated declarations are missed; theorem docs are reported but not expected (the core `missingDocs` linter does not require them).

## 12. Tests

Script: `survey.py tests` (`s_tests`) for library code; test directories by shell:

```
for d in lean4/tests/elab lean4/tests/elab_fail lean4/tests/compile lean4/tests/pkg batteries/BatteriesTest mathlib4/MathlibTest; do
  fd -e lean . $d | wc -l; rg -l '^\s*#guard_msgs' $d -g '*.lean' | wc -l; …; done
```

| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| `#guard_msgs` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 27 (0.01) | 1 (0.08) |
| `#guard` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 1 (0.00) | 155 (11.83) |
| `#eval` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 11 (0.01) | 0 (0.00) |
| `#check` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 8 (0.00) | 0 (0.00) |
| `#print` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |
| `example` | 16 (0.09) | 0 (0.00) | 7 (0.26) | 63 (0.25) | 1 (0.04) | 528 (0.28) | 0 (0.00) |
| `#exit` | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |

| Test dir | `.lean` files | with `#guard_msgs` | with `#guard` | with `example` | with `#eval` | `.out.expected` files |
|---|---|---|---|---|---|---|
| `lean4/tests/elab` | 3,403 | 1,488 | 89 | 1,301 | 555 | 761 |
| `lean4/tests/elab_fail` | 316 | 4 | 0 | 76 | 38 | 316 |
| `lean4/tests/compile` | 105 | 1 | 0 | 0 | 1 | 94 |
| `lean4/tests/pkg` | 228 | 35 | 0 | 18 | 20 | 11 |
| `batteries/BatteriesTest` | 74 | 41 | 12 | 27 | 6 | 0 |
| `mathlib4/MathlibTest` | 421 | 247 | 14 | 290 | 33 | 0 |
| `lean4-parser/ParserTest` | 8 | 1 | 7 | 0 | 0 | 0 |
| `lean4-cli/CliTest` | 2 | 1 | 0 | 0 | 2 | 0 |

- Core library code contains no `#eval`/`#guard`/`#guard_msgs` at all; tests live in `lean4/tests`, whose README defines piles (`elab`, `elab_fail`, `compile`, `pkg`, `lake`, `server_interactive`, benches) and asks that each test be documented "via doc comment inside the test file" and its output recorded with `fix_expected.py` ([tests/README.md L123-L147](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/tests/README.md#L123-L147)). Std's data structures are tested with `/-- info: … -/ #guard_msgs in #eval …`, e.g. [tests/elab/hashmap.lean L15-L17](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/tests/elab/hashmap.lean#L15-L17).
- The wild libraries differ: lean-regex keeps `#guard` tests inside the library tree (`Regex/Data/Anchor/Test.lean`, `Regex/Syntax/Parser/Test.lean`; 155 `#guard` lines).

## 13. Proofs about programs

Script: `survey.py proofs` (`s_proofs`) plus a per-file listing:
`fd -e lean . lean4/src/Std/Data/HashMap | while read f; do echo "$f $(grep -cv '^\s*$' $f) thm:$(grep -cE '^\s*(@\[[^]]*\]\s*)?(private\s+|protected\s+|public\s+)*theorem\b' $f)"; done`.

| col | theorems | defs | thm/def | files: theorems only | files: defs only | files: mixed | `Lemmas.lean` or `Lemmas/` |
|---|---|---|---|---|---|---|---|
| Init | 24638 | 4461 | 5.52 | 145 | 167 | 248 | 108 |
| Std | 20937 | 4584 | 4.57 | 75 | 182 | 165 | 88 |
| Lake | 24 | 2529 | 0.01 | 0 | 136 | 10 | 0 |
| Lean | 31 | 17942 | 0.00 | 0 | 1139 | 13 | 1 |
| Batteries | 2021 | 1096 | 1.84 | 19 | 75 | 47 | 21 |
| Mathlib | 190733 | 37344 | 5.11 | 1567 | 850 | 5964 | 73 |
| Wild | 648 | 694 | 0.93 | 23 | 29 | 47 | 6 |

| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| subtype `{ x // p }` | 338 (1.89) | 109 (0.67) | 4 (0.15) | 9 (0.04) | 9 (0.37) | 2151 (1.14) | 0 (0.00) |
| `Subtype` | 206 (1.15) | 107 (0.66) | 0 (0.00) | 6 (0.02) | 5 (0.20) | 5790 (3.08) | 0 (0.00) |
| `WF` token | 7 (0.04) | 9151 (56.33) | 2 (0.07) | 42 (0.16) | 270 (10.96) | 0 (0.00) | 0 (0.00) |
| `Raw` token | 1371 (7.68) | 4568 (28.12) | 58 (2.15) | 370 (1.45) | 239 (9.70) | 62 (0.03) | 20 (1.53) |
| `Valid`/`Balanced`/`Ordered` tokens | 38 (0.21) | 555 (3.42) | 0 (0.00) | 3 (0.01) | 351 (14.25) | 455 (0.24) | 0 (0.00) |
| `structure … where` with `h…`/`…_lt`/`wf` proof field (≈) | 1387 (7.77) | 557 (3.43) | 43 (1.59) | 219 (0.86) | 146 (5.93) | 19148 (10.17) | 108 (8.25) |
| `:= by` occurrences (tactic bodies) | 18204 (101.92) | 9251 (56.95) | 62 (2.30) | 225 (0.88) | 1340 (54.39) | 139796 (74.26) | 711 (54.28) |

- Std's containers separate implementation and lemmas by file: `HashMap/Basic.lean` 266 nonblank lines / 1 theorem; `HashMap/Lemmas.lean` 2,845 / 679; `HashMap/RawLemmas.lean` 2,881 / 670; `DTreeMap/Internal/Lemmas.lean` 8,873 / 1,876. Each has a `Raw` variant (no invariant, "safe to use in nested inductive types") and a well-formedness predicate `Raw.WF`, bundled in the user-facing structure: [Std/Data/DHashMap/Basic.lean L69-L73](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/Basic.lean#L69-L73) (`structure DHashMap … where inner : DHashMap.Raw α β; wf : inner.WF`), [RawDef.lean L50-L54](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/RawDef.lean#L50-L54), [Raw.lean L686-L695](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DHashMap/Raw.lean#L686-L695) (`inductive WF … → Raw α β → Prop`, constructors named after the operations).
- Subtypes `{ x // p x }` are used 1.9/k in Init, 0.7/k in Std, almost never in Lake/Lean.
- Internal tree operations return proof-carrying results and write a `✓` term where side-condition proofs go (its definition was not checked) (e.g. [Operations.lean L225-L238](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/DTreeMap/Internal/Operations.lean#L225-L238)).

Caveats: the "proof field" row is a loose regex (any indented `h…`/`wf`/`…_lt` field with a relation) and overcounts; `:= by` counts tactic bodies of all declarations, not only lemmas.

## 14. Data structures and Unicode

Script: `survey.py unicode` (`s_unicode`). Type names counted in def/abbrev/opaque/instance headers only.

#### type names in def/abbrev/opaque/instance headers
| col | Array | List | Array share | ByteArray | Vector | HashMap | String | Subarray | Substring |
|---|---|---|---|---|---|---|---|---|---|
| Init | 462 | 675 | 40.6% | 109 | 234 | 0 | 818 | 87 | 127 |
| Std | 247 | 212 | 53.8% | 110 | 13 | 96 | 456 | 0 | 0 |
| Lake | 337 | 42 | 88.9% | 2 | 4 | 6 | 682 | 0 | 5 |
| Lean | 3104 | 997 | 75.7% | 2 | 1 | 102 | 1393 | 10 | 10 |
| Batteries | 162 | 329 | 33.0% | 10 | 36 | 45 | 77 | 8 | 21 |
| Mathlib | 519 | 1147 | 31.2% | 0 | 116 | 26 | 270 | 1 | 4 |
| Wild | 65 | 37 | 63.7% | 0 | 10 | 2 | 235 | 1 | 1 |

| pattern (count, per kLOC) | Init | Std | Lake | Lean | Batteries | Mathlib | Wild |
|---|---|---|---|---|---|---|---|
| `→` | 15046 (84.24) | 14175 (87.26) | 399 (14.78) | 4587 (17.94) | 2341 (95.01) | 110127 (58.50) | 540 (41.23) |
| `->` | 1 (0.01) | 0 (0.00) | 0 (0.00) | 7 (0.03) | 2 (0.08) | 6 (0.00) | 0 (0.00) |
| `←` | 5218 (29.22) | 2917 (17.96) | 1915 (70.92) | 32604 (127.55) | 1157 (46.96) | 78448 (41.67) | 312 (23.82) |
| `<-` | 3 (0.02) | 0 (0.00) | 0 (0.00) | 3 (0.01) | 0 (0.00) | 1 (0.00) | 0 (0.00) |
| `↦` | 73 (0.41) | 2 (0.01) | 0 (0.00) | 18 (0.07) | 0 (0.00) | 55823 (29.65) | 0 (0.00) |
| `=>` | 15344 (85.91) | 12881 (79.29) | 2184 (80.89) | 28687 (112.23) | 3108 (126.14) | 86887 (46.15) | 1676 (127.96) |
| `×` | 396 (2.22) | 4139 (25.48) | 89 (3.30) | 1844 (7.21) | 221 (8.97) | 11777 (6.26) | 147 (11.22) |
| `Prod ` (prefix) | 38 (0.21) | 17 (0.10) | 1 (0.04) | 26 (0.10) | 0 (0.00) | 528 (0.28) | 0 (0.00) |
| `∀` | 2955 (16.54) | 2137 (13.15) | 10 (0.37) | 33 (0.13) | 502 (20.37) | 51375 (27.29) | 120 (9.16) |
| `forall` | 10 (0.06) | 22 (0.14) | 0 (0.00) | 17 (0.07) | 0 (0.00) | 861 (0.46) | 0 (0.00) |
| `∃` | 1082 (6.06) | 462 (2.84) | 0 (0.00) | 8 (0.03) | 132 (5.36) | 15483 (8.22) | 140 (10.69) |
| `exists`/`Exists` | 147 (0.82) | 58 (0.36) | 0 (0.00) | 30 (0.12) | 7 (0.28) | 1231 (0.65) | 8 (0.61) |
| `≠` | 1776 (9.94) | 321 (1.98) | 11 (0.41) | 72 (0.28) | 102 (4.14) | 19659 (10.44) | 158 (12.06) |
| `!=` (Bool) | 101 (0.57) | 47 (0.29) | 29 (1.07) | 622 (2.43) | 13 (0.53) | 158 (0.08) | 1 (0.08) |
| `¬` | 1163 (6.51) | 1708 (10.51) | 11 (0.41) | 36 (0.14) | 62 (2.52) | 4550 (2.42) | 57 (4.35) |
| `Not ` | 47 (0.26) | 5 (0.03) | 0 (0.00) | 30 (0.12) | 1 (0.04) | 247 (0.13) | 0 (0.00) |
| `≤` | 5692 (31.87) | 965 (5.94) | 56 (2.07) | 220 (0.86) | 191 (7.75) | 43893 (23.32) | 207 (15.80) |
| `<=` | 12 (0.07) | 4 (0.02) | 0 (0.00) | 95 (0.37) | 3 (0.12) | 11 (0.01) | 9 (0.69) |
| `∘` | 246 (1.38) | 142 (0.87) | 1 (0.04) | 98 (0.38) | 33 (1.34) | 11166 (5.93) | 1 (0.08) |
| `⟨…⟩` | 8489 (47.53) | 6945 (42.75) | 521 (19.30) | 1748 (6.84) | 1519 (61.65) | 116032 (61.63) | 687 (52.45) |
| `.mk` | 483 (2.70) | 326 (2.01) | 127 (4.70) | 382 (1.49) | 67 (2.72) | 10793 (5.73) | 28 (2.14) |
| `<|` | 1214 (6.80) | 1418 (8.73) | 552 (20.44) | 5021 (19.64) | 415 (16.84) | 33793 (17.95) | 144 (10.99) |
| `$` | 543 (3.04) | 333 (2.05) | 470 (17.41) | 2205 (8.63) | 226 (9.17) | 3692 (1.96) | 53 (4.05) |
| `|>.` | 331 (1.85) | 2084 (12.83) | 420 (15.55) | 1646 (6.44) | 164 (6.66) | 3862 (2.05) | 121 (9.24) |
| `|>` | 167 (0.94) | 292 (1.80) | 83 (3.07) | 697 (2.73) | 44 (1.79) | 168 (0.09) | 84 (6.41) |
| `λ` | 3 (0.02) | 1 (0.01) | 0 (0.00) | 1 (0.00) | 3 (0.12) | 782 (0.42) | 0 (0.00) |
| `fun` | 5069 (28.38) | 7737 (47.63) | 632 (23.41) | 9113 (35.65) | 899 (36.49) | 114301 (60.72) | 206 (15.73) |

#### names bound with `: Type …`/`: Sort …` in binders
| col | n | Greek letter | single Latin letter | longer name |
|---|---|---|---|---|
| Init | 5215 | 78.0% | 21.6% | 0.4% |
| Std | 3500 | 76.3% | 15.4% | 8.3% |
| Lake | 141 | 77.3% | 22.7% | 0.0% |
| Lean | 638 | 80.4% | 18.3% | 1.3% |
| Batteries | 123 | 86.2% | 13.8% | 0.0% |
| Mathlib | 50507 | 31.2% | 64.9% | 3.9% |
| Wild | 24 | 95.8% | 4.2% | 0.0% |

- `Array` vs `List` in program signatures: Lake 89% `Array`, Lean 76%, Std 54%, Init 41% (Init defines the `List` API itself), Batteries 33%.
- Unicode notation is the norm and ASCII variants are nearly absent in code: `→` vs `->` 15,046:1 in Init; `←` vs `<-` 5,218:3; `≤` vs `<=` 5,692:12. `!=` is the Bool operator and not an ASCII spelling of `≠`.
- Type variables bound with `: Type`/`: Sort` are Greek in 76–86% of core binders and single Latin letters in Mathlib (65%).

Caveat: `$` count includes `$` in syntax quotations (`$x` antiquotations are excluded by the lookahead only when followed by an identifier character).

## 15. Tooling (linters and formatters)

Commands: `rg -n -A3 'register_builtin_option\s+linter\.' lean4/src` (defaults read from `defValue`); `rg -o --no-filename '^set_option (linter\.[\w.]+) (\w+)' <subtree> | sort | uniq -c`; Mathlib `lakefile.lean` and `Mathlib/Init.lean`; Batteries `lakefile.toml`, `Batteries/Tactic/Lint/`.

Core builtin linter options (39 registrations; default in parentheses): on by default: `unusedVariables` (+`.funArgs`, `.patternVars`), `unusedSectionVars`, `unusedSimpArgs`, `unnecessarySimpa`, `unnecessaryRwa`, `deprecated` (+`.module`, `.options`, `.syntax`, `.arg`, `.deprecatedTarget`), `ambiguousOpen`, `deprecatedCoercions`, `defProp`, `suspiciousUnexpanderPatterns`, `tactic.docsOnAlt`, `tactic.unusedName`, `checkUnivs`, `constructorNameAsVariable`, `doc.deferred`. Off by default: `missingDocs`, `redundantVisibility`, `indexVariables`, `listVariables`, `omit`, `tacticCheckInstances`, `loopingSimpArgs`, `extra.*` (`unusedDecidableInType`, `unreachableTactic`, `unnecessarySeqFocus`, `dupNamespace`), `coreInternal.*`, `all`. Source files: `lean4/src/Lean/Linter/` (e.g. [List.lean L24-L42](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Lean/Linter/List.lean#L24-L42): `indexVariables` allows only `i`, `j`, `k` as indices and `n`, `m` as widths).

How the stdlib turns them on:
- Build-wide for core: `leanOptions.linter.coreInternal = true`, `leanOptions.linter.redundantVisibility = true` ([src/lakefile.toml.in L48-L50](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lakefile.toml.in#L48-L50)).
- Per file: Std has `set_option linter.missingDocs true` in 102 files and `linter.all true` in 88; Init has `linter.listVariables true` in 95 files, `linter.indexVariables true` in 94 and `linter.missingDocs true` in 61; Lake sets almost none (it disables `deprecated` in 6 files).
- New in core: an environment-linter framework ported from Batteries/Mathlib (`@[builtin_env_linter]`, `src/Lean/Linter/EnvLinter/`) with no builtin linters registered yet, and a code-quality metrics module (`src/Lean/Linter/CodeQuality/`).

Mathlib: `linter.mathlibStandardSet` ([Mathlib/Init.lean L88-L116](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/Mathlib/Init.lean#L88-L116)) enables `style.{cases,induction,refine,cdot,docString,dollarSyntax,emptyLine,header,lambdaSyntax,longLine,longFile,multiGoal,native,openClassical,maxHeartbeats,missingEnd,setOption,show,whitespace}`, `auxLemma`, `flexible`, `hashCommand`, `oldObtain`, `privateModule`, `unusedDecidableInType`, `unusedFintypeInType`; the lakefile turns the set on for Mathlib builds with `linter.style.longFile` at 1500 and sets `pp.unicode.fun` ([lakefile.lean L28-L48](https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/lakefile.lean#L28-L48)), uses `lintDriver := "batteries/runLinter"` and `builtinLint := true`. A text-based linter (`Mathlib/Tactic/Linter/TextBased.lean`) checks adaptation notes, Windows line endings, semicolons, unwanted Unicode and Unicode variant selectors; `scripts/fix_long_lines.py` exists.

Batteries: `[leanOptions] linter.missingDocs = true` for the library ([lakefile.toml](https://github.com/leanprover-community/batteries/blob/4453b52d2468f4c346a8711d728c0742e7483c9b/lakefile.toml)), `lintDriver = "runLinter"`, environment linters `unusedArguments`, `docBlame`, `checkType`, `synTaut`, `unusedHavesSuffices`, `simpNF`, `simpComm`, `impossibleInstance`, `nonClassInstance` (disabled: `docBlameThm`, `explicitVarsOfIff`), and `scripts/lintWhitespace.sh` (trailing whitespace, final newline).

Formatters: none of the repos ships or runs a source formatter. Core has the pretty-printer (`Lean.PrettyPrinter.ppCommand`/`ppModule`) and a 2021 experiment, [script/reformat.lean](https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/script/reformat.lean) (Gabriel Ebner), that re-prints parsed commands with `ppCommand`. Mathlib uses the pretty-printer only inside linters: `linter.ppRoundtrip` (off by default, "warning when the syntax of a command differs substantially from the pretty-printed version") and `linter.style.whitespace` (compares a declaration's hypotheses segment with its pretty-printed form; in the standard set). The awesome list names three third-party formatters (leanfmt, lean-fmt, leaner); **unverified**, not cloned.

## Not measured

- Structure-instance layout (`{` placement, `with`), `if`/`then`/`else` splitting, operator-at-end-of-line splitting, orphaned parentheses (style.md rules).
- Theorem naming against `naming.md`'s algorithm; variable-name conventions beyond `Type` binders.
- Structural recursion counts; `fuel` patterns beyond a token count.
- Docstring first-sentence grammar beyond first-word frequency; `add_decl_doc`.
- Test content of `lean4/tests/lake` and `server_interactive`; the third-party formatters; any column beyond the three wild libraries.
- Per-topic handoff summary (`summary-survey.md`) was skipped at the lead's request.

## Addendum: conversion names (2026-10-20)

Definitions whose last name component starts with `of`, `from` or `to` followed by an uppercase letter, at lean4 `3a685e6`.

| col | `ofX` | `fromX` | `toX` |
|---|---|---|---|
| Init | 191 | 6 | 375 |
| Std | 271 | 24 | 248 |
| Lean | 122 | 41 | 363 |
| Lake | 64 | 15 | 87 |

Command, run from `vendor/repos/lean4/src` for each directory `$d` and prefix `$p` (`of`, `from`, `to`):

```sh
grep -rhoE '^\s*(@\[[^]]*\]\s*)?((private|protected|public|partial|noncomputable|unsafe)\s+)*(def|abbrev) ([A-Za-z0-9_.]+\.)?'"$p"'[A-Z][A-Za-z0-9]*' $d --include='*.lean' | wc -l
```

The regex counts `def` and `abbrev` only, not instances or theorems.
