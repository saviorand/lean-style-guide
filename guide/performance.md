# Performance and low-level code

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="perf-measure"></a>
## Measure first

Don't add `@[inline]` or `@[specialize]` without a measurement that shows they help.

*Sources: [Google Haskell guide][google-pragmas], [FRO practice][fro-d].*

<a name="perf-implemented-by"></a>
## `implemented_by` and `csimp`

`@[implemented_by fast] def slow` makes the compiler run `fast` wherever the code calls `slow`. Lean doesn't check that the two agree. If you can, prove that they agree and use `@[csimp]` instead, which requires the proof.

```lean
-- good
def double (n : Nat) : Nat := n + n

def doubleFast (n : Nat) : Nat := 2 * n

@[csimp] theorem double_eq_doubleFast : @double = @doubleFast := by
  funext n
  simp only [double, doubleFast]
  omega
```

*Source: [Lean Reference][ref-implby].*

<a name="perf-unsafe"></a>
## `unsafe`

Keep `unsafe` code in small functions with a safe interface, and say in a comment why it's needed. Lean can't reason about `unsafe` code.

*Source: [Lean Reference][ref-partial].*

<a name="perf-ffi"></a>
## Foreign functions

Declare C functions with `@[extern]` in a small module of their own, and wrap them in functions with Lean types that are hard to misuse. Lean's FFI is unstable, and keeping it in one place limits what you have to fix when it changes.

*Source: [Lean Reference][ref-ffi].*

---

Previous: [Macros and notation](macros.md) · [Contents](../README.md#rules) · Next: [Projects and tooling](projects.md)

[fro-d]: ../research/author-survey.md#author-dependent-no-fro-convention
[google-pragmas]: https://google.github.io/styleguide/haskellguide.html#pragmas
[ref-ffi]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Runtime.lean#L340
[ref-implby]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs.lean#L298-L303
[ref-partial]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/RecursiveDefs.lean#L195-L211
