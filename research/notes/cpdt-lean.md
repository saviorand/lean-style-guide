# cpdt-lean: a Lean 4 port of Chlipala's CPDT (plus CPDT's position on proof engineering)

| Field | Value |
|---|---|
| URL | https://github.com/hargoniX/cpdt-lean ; original book http://adam.chlipala.net/cpdt/ |
| Author / org | Henrik Böving (hargoniX), single commit; original book by Adam Chlipala |
| Date / version | `65896137166a8ef74e816efc187346bc8f8bbd22`, 2022-06-05; `lean-toolchain` = `leanprover/lean4:nightly-2022-06-05` (very early Lean 4 syntax); 1 commit; 1010 lines of Lean over 14 files |
| License | Port: Apache-2.0 (`LICENSE`; file headers "Released under Apache 2.0 license"; GitHub API: Apache License 2.0). Book: copyrighted, free online version allowed by MIT Press ("who have graciously agreed to allow distribution of free versions online indefinitely"); only the supporting library modules are "released under an open-source license, while the book generally isn't" ([site](http://adam.chlipala.net/cpdt/)). |
| Scope & audience | Lean learners following CPDT; not a style guide |
| Kind | descriptive |
| Lean version | Lean 4, nightly-2022-06-05 (pre-Std, pre-`omega`/`grind`; uses `termination_by f x => ...` old syntax) |
| Raw copy | clone `vendor/repos/cpdt-lean`; book pages `vendor/pages/proof-assistants/cpdt-intro.md`, `cpdt-subset.md`, `cpdt-predicates.md`, `cpdt-datastruct.md` |

## Summary
The port has no design commentary beyond a one-line README ("Lean implementations of things found in Certified Programming with Dependent Types") and a few code comments. As code it shows how the book's idioms look in Lean 4: indexed families for intrinsically typed ASTs, a hand-rolled `Maybe p` type that returns a proof with the answer, `{ys // ys.length = n}` subtypes for the inverse of an indexed vector, a separate `theorem` for a well-foundedness fact used inside a `have` for `termination_by`, and `simp`/`simp_all` as the automation. The chapters 2, 3, 4, 5, 7, 8 are covered; the domain-theory file is unfinished (`sorry`). The original book's introduction states the philosophy that the port inherits.

## What the code shows (descriptive; no rules)
- **Intrinsic typing in data.** `inductive Exp : Ty → Type` with constructors indexed by result type (`and : Exp .bool → Exp .bool → Exp .bool`) and `Ty.denote` marked `@[reducible]` so the index computes ([Chapter8/Tagless.lean L9-L30](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter8/Tagless.lean#L9-L30)). Stack machine with `TInstr : TStack → TStack → Type` ([Chapter2/Typed.lean L60-L66](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter2/Typed.lean#L60-L66)).
- **Extrinsic typing with a proof-carrying result.** An untyped `Exp`, a `HasType` relation in `Prop`, and `Exp.typecheck : (e : Exp) → {{ t | HasType e t }}` where `Maybe p` is `found (a) (p a) | unknown`; correctness is proved afterwards as separate theorems (`typecheck_correct`, `typecheck_complete`) ([Chapter5/Typechecker.lean L12-L90](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter5/Typechecker.lean#L12-L90)).
- **Subtype as return type.** `unject : (xs : IList α n) → {ys : List α // ys.length = n}` builds the proof with the data, discharged by `by simp [prop]`; a separate theorem `inject_unject_inv` states the round trip ([Chapter8/LengthIndexed.lean L9-L35](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter8/LengthIndexed.lean#L9-L35)).
- **Indexed type vs partial function.** `head : IList α (Nat.succ n) → α` is total by indexing, no proof argument (same file).
- **Where proofs live.** Theorems follow the definitions in the same file; operational lemmas are `@[simp] theorem denote_nConst : ... := by rfl` ([Typed.lean L52-L54](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter2/Typed.lean#L52-L54)); main correctness theorem last (`compile_correct`).
- **Termination.** `mergeSort` is defined by structural patterns, builds `have h1 : (split ls).fst.length < ...` from a separate lemma `split_wf_match`, then `termination_by mergeSort ls => ls.length` ([Chapter7/Wellfounded.lean L27-L54](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter7/Wellfounded.lean#L27-L54)). This is pre-`decreasing_by` syntax and obsolete.
- **Automation.** Mostly `induction e with simp[denote, cfold]` then `split <;> simp_all[...]` ([Tagless.lean L86-L102](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter8/Tagless.lean#L86-L102)); `rfl` for computation lemmas; no custom tactics (CPDT's own `crush` has no counterpart).
- **Comments admit limits.** "Sadly writing the definition like in the book doesnt work yet :(" ([Chapter3/Nested.lean L42](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter3/Nested.lean#L42)); the domain-theory/general-recursion monad ends with `sorry`s and "this approach will not work out. Hence I stopped work on it" ([Chapter7/DomainTheory.lean L157-L159](https://github.com/hargoniX/cpdt-lean/blob/65896137166a8ef74e816efc187346bc8f8bbd22/Cpdt/Chapter7/DomainTheory.lean#L157-L159)).

## CPDT's own position (book)
Cost of verification:
> today most people who write software, practitioners and academics alike, assume that the costs of formal program verification outweigh the benefits. The purpose of this book is to convince you that the technology of program verification is mature enough today that it makes sense to use it in a support role in many kinds of research projects in computer science.
([Intro](http://adam.chlipala.net/cpdt/html/Intro.html))

Dependent types fold specification into code:
> we start investigating uses of *dependent types* to integrate programming, specification, and proving into a single phase. The techniques we will learn make it possible to reduce the cost of program verification dramatically.
([Subset](http://adam.chlipala.net/cpdt/html/Subset.html))

Automation over hand-written proofs:
> A commitment to a kernel proof language opens up wide possibilities for user extension of proof automation systems, without allowing user mistakes to trick the overall system into accepting invalid proofs.
([Intro, "Convenient Programmable Proof Automation"](http://adam.chlipala.net/cpdt/html/Intro.html))

Proof readability:
> It is very easy to write proof scripts that manipulate proof goals imperatively, with no structure to aid readers. Such developments are nightmares to maintain, and they certainly do not manage to convey "why the theorem is true" to anyone but the original author.
([Intro, "Engineering with a Proof Assistant"](http://adam.chlipala.net/cpdt/html/Intro.html))

Pragmatics are unsettled:
> I believe that the best ways to manage significant Coq developments are far from settled. In this book, I mean to propose my own techniques
([Intro, "Reading This Book"](http://adam.chlipala.net/cpdt/html/Intro.html))

The QED-at-large survey summarises the book's stance as "advocates for the heavy use of program-specific automation, noting that this makes proofs more robust", localising "the burden of change to the automation itself" (see `proof-engineering.md`, secondary source).

## What transfers to general-purpose Lean
- Both styles co-exist: intrinsic (indexed families; no proof obligations at call sites, but proof burden inside definitions) and extrinsic (plain data plus `Prop` relation plus separate theorems). The port shows no rule for choosing; the book's Subset chapter argues for dependent types to lower cost.
- A function that returns "the answer with a proof" (`Maybe p`, subtype) versus a function plus a separate correctness theorem is the central bundled-vs-separate choice for programs.
- Termination via a lemma proved separately and brought in with `have` is superseded in current Lean by `decreasing_by`/`grind`; so port code cannot be used for termination style.
- Custom, program-specific automation (`crush`) is a Coq idiom; in Lean the closest are `simp` sets and macros (not shown in the port).

## Caveats and unverified items
- Port dates from 2022; the syntax and Lean automation have changed a lot. Do not treat its idioms as current Lean style.
- Only the Intro and Subset chapters of the book were skimmed (via defuddle); the book's chapters on reflection/automation (chap. 14+) were not read. The "pragmatics unsettled" quote's source paragraph is in the Intro (line 70 of the saved copy).
- The port has 14 files; I did not read `DomainTheory.lean` beyond its end and `Mutual`/`Nested`/`Reflexive` beyond headers.
