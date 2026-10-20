# Proposed table of contents

Modelled on bbatsov's Clojure guide ([bbatsov-clojure](notes/bbatsov-clojure.md)): an intro with guiding principles and a consistency note, then topic chapters whose rules each have an anchor, a short imperative and a good/bad pair, then the closing sections. Lean-specific chapters (termination, proofs about programs, invariants) sit where Clojure has Macros and Metadata. The bracketed `Q#` references point to [open-questions.md](open-questions.md); chapters that depend on an unresolved decision say so.

1. **Introduction**
   - Scope: programs, libraries and tools, not Mathlib-style mathematics. Relation to `doc/std` and Mathlib's guides. [Q0]
   - Guiding principles: code is read more than written; guessable names (from core-naming); prefer established stdlib practice to subjective alternatives.
   - A note about consistency (in the PEP 8/bbatsov style). Version policy: the Lean version the guide targets, and how rules change between releases.
   - How to read a rule: anchors and strength words (Prefer, Avoid, Use, Consider).
2. **Source code layout and organization** [Q4, Q5, Q6]
   - Whitespace; indentation; line length; splitting terms and signatures; `match` layout.
   - `where`, `termination_by` and `deriving` placement.
   - Structure instances; `do` blocks.
   - File header, imports, module docs; `namespace`/`section`; file and module layout. [Q23]
3. **Naming** [Q1, Q2, Q3]
   - Casing by kind; namespaces and dot notation; acronyms; no primes.
   - Predicates; failure variants (`?`, `!`, `D`, proof-taking).
   - Conversions (`ofX`/`toX`); instances; helpers; local variable names (idiomatic-names table).
4. **Functions**
   - Lambdas (`fun`/`·`) [Q4]; explicit signatures on public definitions; implicit vs explicit arguments.
   - Local helpers (`where`/`let rec`) [Q7]; pipelines and point-free style [Q8].
   - Parameter count and options structures.
5. **`do` notation and effects**
   - Early `return`; `let some … | …`; `let mut` and `for`; nested `(← …)`.
   - `Id.run do`; monad stacks; resources and `try … finally` [Q14].
6. **Data modelling** [Q9, Q10, Q11]
   - `structure` vs `inductive` vs `class`; custom inductives over `Sum`/`Bool`.
   - Making illegal states unrepresentable; named wrapper types; `abbrev` vs `def`.
   - `deriving`; constructor naming; hiding representations.
7. **Type classes and instances**
   - When to define a class; `-Of` variants and outParams; `where` instances.
   - Instance naming; no `Monad List`-style traps.
8. **Collections and data structures**
   - `Array` vs `List`; `HashMap`/`TreeMap`; Unicode in identifiers and notation; custom notation restraint.
9. **Error handling** [Q12, Q13]
   - `Option`, `Except` and `IO` errors; `panic!`/`unreachable!`; `get!` vs `getD`; error types; never catch everything; documenting failure modes.
10. **Termination and recursion** [Q15]
    - Structural, `termination_by`/`decreasing_by`, fuel, `partial_fixpoint` and `partial`; tail recursion and accumulators.
11. **Invariants and proofs about programs** [Q9, Q16, Q17, Q18, Q0b]
    - Bundled vs separate lemmas; subtypes; where proofs live; when not to prove; proof robustness (squeezing, `grind`/`omega`).
12. **Performance and low-level** [Q24]
    - `@[inline]`, `@[specialize]`; `@[extern]`, `implemented_by`, `unsafe`; `@[csimp]`.
13. **API design and visibility** [Q22, Q23]
    - Minimal surface; `private`/`protected`/`Internal`; the module system (`public`, `@[expose]`).
    - `open` hygiene; `scoped` syntax; deprecation (`@[deprecated … (since := …)]`).
14. **Comments** — what to comment; invariants not enforced by types; `TODO` format.
15. **Documentation** [Q19, Q20]
    - Docstrings: summary first, sections, examples; module docs (`/-! -/`); doc-gen4 and Verso.
16. **Testing** [Q21]
    - `#guard_msgs` and `#guard`; `lake test`; test layout; property tests.
17. **Library organization** — Lake package layout; naming packages and libraries; toolchain pinning; Reservoir.
18. **Tooling** [Q25] — linters to enable; warning-free builds; formatter status.
19. **Existential** — be total where cheap, be consistent, use common sense (after Clojure's three one-liners).
20. **Appendices and closing sections**
    - Sources of inspiration and evidence (link to this research).
    - Changelog by Lean version; contributing; licence [Q26].
