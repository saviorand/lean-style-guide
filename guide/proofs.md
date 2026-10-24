# Proofs about programs

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="proofs-first"></a>
## Proofs first

Give each claim about your code the strongest form it admits. Put it in a type if that's cheap. Otherwise prove it as a theorem, and fall back to a property test, then to an example with an expected result, only when the stronger form doesn't work out. FPIL warns that proofs can be expensive, but with AI assistance many now cost little more than the tests they replace, so make them the default.

A theorem is required when the claim is about a pure, total function and either:

- its cases are finite, as with encodings and mappings between representations, or
- a counterexample would corrupt output rather than merely look wrong, as with an invariant that a file format depends on.

*Sources: [Paul Butcher, issue #1][issue-1], [FPIL][fpil-proofs].*
<a name="proofs-spec"></a>
## Executable specifications

When you write a fast version of a function, keep the simple version as its specification, and prove that the two agree.

```lean
def sumTo (n : Nat) : Nat := (List.range (n + 1)).foldl (· + ·) 0

def sumToFast (n : Nat) : Nat := n * (n + 1) / 2

-- bad
#guard (List.range 50).all fun n => sumTo n == sumToFast n
```

```lean
def sumTo (n : Nat) : Nat := (List.range (n + 1)).foldl (· + ·) 0

def sumToFast (n : Nat) : Nat := n * (n + 1) / 2

-- good
theorem sumToFast_eq_sumTo (n : Nat) : sumToFast n = sumTo n := by
  induction n with
  | zero => rfl
  | succ k ih => simp only [sumTo, sumToFast, List.range_succ, List.foldl_append] at *; grind
```

*Sources: [FPIL][fpil-proofs], [Paul Butcher, issue #1][issue-1].*

<a name="proofs-timebox"></a>
## When a proof doesn't work out

Give a proof a fixed amount of time. If it doesn't work out, write a property test instead, and say in a comment what blocked the proof, so the next person knows where to start.

*Source: [Paul Butcher, issue #1][issue-1].*

<a name="proofs-recheck"></a>
## Revisiting property tests

When a module that has property tests changes, check whether each property can now be proved. A change to a definition or a new lemma in a dependency can make a proof that failed before go through.

*Source: [Paul Butcher, issue #1][issue-1].*
<a name="proofs-location"></a>
## Location of proofs

Keep a few short lemmas next to the definitions they're about. When the proofs grow, move them to a module of their own, such as a `Lemmas.lean` next to `Basic.lean`. Code that imports only the definitions then doesn't have to build the proofs.

*Source: [standard library][survey-proofs].*

<a name="proofs-automation"></a>
## Automation

Prefer strong automation such as `grind`, `omega` and `simp` to long step-by-step proofs. Tactic proofs are what most often breaks when you upgrade Lean, and short automated proofs break less. When `simp` isn't the last step of a proof, list its lemmas with `simp only [...]` (`simp?` prints them), so new simp lemmas can't change what it does.

```lean
def rev {α : Type} : List α → List α
  | [] => []
  | x :: xs => rev xs ++ [x]

-- bad
theorem rev_length {α : Type} (xs : List α) : (rev xs).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp [rev]
    rw [ih]
```

```lean
def rev {α : Type} : List α → List α
  | [] => []
  | x :: xs => rev xs ++ [x]

-- good
theorem rev_length {α : Type} (xs : List α) : (rev xs).length = xs.length := by
  fun_induction rev <;> grind
```

*Sources: [Lean core style][cs-tactics], [FPIL][fpil-proof-style].*

<a name="proofs-names"></a>
## Theorem names

Name a theorem after what it states, in `snake_case`, starting from the conclusion. `rev_length` is about the length of `rev`. `List.length_append` is about the length of an append. Lean's [naming conventions](https://github.com/leanprover/lean4/blob/master/doc/std/naming.md) describe the full scheme.

*Source: [Lean naming conventions][cn-thm].*

<a name="proofs-sorry"></a>
## `sorry`

Don't commit `sorry`. Lean accepts it as a proof of any statement, true or false. A false proof that an index is in bounds, for example, lets an out-of-bounds access through at run time. Lean warns about every `sorry`, so `lake build --wfail` catches them.

*Source: [FPIL][fpil-sorry].*

---

Previous: [Recursion and termination](recursion.md) · [Contents](../README.md#rules) · Next: [Testing](testing.md)


[cn-thm]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#naming-algorithm-for-theorems-and-some-definitions
[cs-tactics]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#tactic-proofs
[fpil-proof-style]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Inequalities.lean#L459-L462
[fpil-proofs]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs.lean#L37-L41
[fpil-sorry]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L99
[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
[survey-proofs]: ../research/stdlib-survey.md#13-proofs-about-programs
