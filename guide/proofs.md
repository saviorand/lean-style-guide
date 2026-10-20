# Proofs about programs

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="proofs-cost"></a>
## The cost of proofs

Proofs make many tests unnecessary, but they take time to write and maintain. Put cheap guarantees in types, test the rest, and prove the properties that matter most and change least. Test a function before you prove anything about it, so you don't spend a proof on a bug.

*Sources: FPIL on [cost][fpil-proofs] and [testing first][fpil-testfirst].*

<a name="proofs-spec"></a>
## Executable specifications

When you write a fast version of a function, keep the simple version as its specification. Test that the two agree, and prove it if it matters.

```lean
-- good
def sumTo (n : Nat) : Nat := (List.range (n + 1)).foldl (· + ·) 0

def sumToFast (n : Nat) : Nat := n * (n + 1) / 2

#guard (List.range 50).all fun n => sumTo n == sumToFast n
```

*Source: [FPIL][fpil-proofs].*

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

Previous: [Recursion and termination](recursion.md) · [Contents](../README.md#rules) · Next: [Performance and low-level code](performance.md)


[cn-thm]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#naming-algorithm-for-theorems-and-some-definitions
[cs-tactics]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#tactic-proofs
[fpil-proof-style]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Inequalities.lean#L459-L462
[fpil-proofs]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs.lean#L37-L41
[fpil-sorry]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/Summary.lean#L99
[fpil-testfirst]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/TailRecursionProofs.lean#L20
[survey-proofs]: ../research/stdlib-survey.md#13-proofs-about-programs
