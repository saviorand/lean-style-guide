# Type classes and instances

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="classes-when"></a>
## When to define a class

Define a type class when several types will have instances and code will be generic over them. For a single type, write ordinary functions. If callers need to pick an implementation at run time, pass a structure of functions instead.

*Source: [FPIL][fpil-classes].*

<a name="classes-weakest"></a>
## The weakest class that works

Ask for the weakest class a function needs, so it works for more types. Give your own types the strongest instances they support.

```lean
-- bad
def labelAll {m : Type → Type} [Monad m] (xs : m Nat) : m String := (toString ·) <$> xs
```

```lean
-- good
def labelAll {m : Type → Type} [Functor m] (xs : m Nat) : m String := (toString ·) <$> xs
```

*Source: [FPIL][fpil-weak].*

<a name="classes-consistent"></a>
## Consistent instances

Make a type's instances agree with each other. Values that are equal under `BEq` must have equal hashes, and `Ord`, `LT` and `LE` must give the same order. Lean can't check this, and a hash map with disagreeing instances silently loses entries.

```lean
-- bad: two tags that are equal under `==` can have different hashes
structure Tag where
  name : String
deriving Hashable

instance : BEq Tag where
  beq a b := a.name.toLower == b.name.toLower
```

```lean
-- good
structure Tag where
  name : String

instance : BEq Tag where
  beq a b := a.name.toLower == b.name.toLower

instance : Hashable Tag where
  hash t := hash t.name.toLower
```

*Sources: [Lean Reference][ref-beq], [FPIL][fpil-lawful].*

<a name="classes-coercions"></a>
## Coercions

Add a coercion only when every value of the source type has an obvious counterpart in the target type, as with `Nat` to `Int`. Don't add a coercion that undoes a wrapper type.

*Source: [FPIL][fpil-coe].*

<a name="classes-recursive"></a>
## Instances for recursive types

For a recursive type, write the recursive function in the type's namespace and have the instance call it. You can then also call the function directly.

```lean
-- good
inductive Tree where
  | leaf
  | node (left : Tree) (value : Nat) (right : Tree)

def Tree.toString : Tree → String
  | .leaf => "."
  | .node l v r => s!"({l.toString} {v} {r.toString})"

instance : ToString Tree where
  toString := Tree.toString
```

*Source: [Lean Reference][ref-recinst].*

<a name="classes-where"></a>
## Instance syntax

Write instances with `where`, one method per line.

```lean
structure Money where
  cents : Int

-- bad
instance : Add Money := ⟨fun a b => ⟨a.cents + b.cents⟩⟩
```

```lean
structure Money where
  cents : Int

-- good
instance : Add Money where
  add a b := ⟨a.cents + b.cents⟩
```

*Source: [FPIL][fpil-instwhere].*

---

Previous: [Functions](functions.md) · [Contents](../README.md#rules) · Next: [Collections](collections.md)


[fpil-classes]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L328
[fpil-coe]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Coercions.lean#L217-L218
[fpil-instwhere]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/Conveniences.lean#L70
[fpil-lawful]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L284
[fpil-weak]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Summary.lean#L58-L59
[ref-beq]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Classes/BasicClasses.lean#L30
[ref-recinst]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Classes/InstanceDecls.lean#L119-L123
