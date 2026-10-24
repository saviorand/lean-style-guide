# Comments

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="comments-why"></a>
## Explaining why

Comment on why the code does something. Don't restate what the code does or repeat its type signature.

```lean
-- bad
def backoffMs (attempt : Nat) : Nat :=
  -- multiply 100 by 2 to the power of attempt, at most 30000
  min 30000 (100 * 2 ^ attempt)
```

```lean
-- good
def backoffMs (attempt : Nat) : Nat :=
  -- Cap the delay so that a long outage doesn't stall a client for minutes.
  min 30000 (100 * 2 ^ attempt)
```

*Sources: [lean4 `AGENTS.md`][agents-comments], [Google Haskell guide][google-comments].*

<a name="comments-invariants"></a>
## Invariants

Write down every invariant that your types don't enforce, next to the code that relies on it. If you can move an invariant into a type cheaply, do that instead (see [Checking at the boundary](data.md#data-boundary)).

```lean
-- good
structure Buffer where
  data : ByteArray
  -- Invariant: `start ≤ data.size`. `Buffer.remaining` relies on it.
  start : Nat

def Buffer.remaining (b : Buffer) : Nat := b.data.size - b.start
```

*Source: [lean4 `AGENTS.md`][agents-comments].*

<a name="comments-history"></a>
## History and dead code

Don't keep the history of a change or old versions of code in comments. Version control keeps both. When a comment goes stale, rewrite it rather than adding a new one beside it. Track unfinished work in the issue tracker rather than in `-- TODO:` comments. A TODO describes a plan, so it stops being true when the plan changes or is carried out.

*Sources: [lean4 `AGENTS.md`][agents-comments], [Paul Butcher, issue #1][issue-1].*

---

Previous: [Documentation](documentation.md) · [Contents](../README.md#rules) · Next: [Macros and notation](macros.md)

[agents-comments]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/AGENTS.md?plain=1#L75-L83
[google-comments]: https://google.github.io/styleguide/haskellguide.html#comments
[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
