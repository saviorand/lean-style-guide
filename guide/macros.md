# Macros and notation

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="macros-symbols"></a>
## Custom operators

Avoid new symbolic operators in program APIs. A named function is easier to search for and to read aloud. Use the standard operators through their classes instead.

*Sources: [Lean core style][cs-notation], [measured in Lake][checked].*

<a name="macros-classes"></a>
## Standard notation through classes

Before you add notation, check whether a standard class already provides it. Implement `Add` to get `+`, `GetElem` to get `xs[i]`, `ToString` to use a value in `s!"…"`, and `Append` to get `++`.

```lean
structure Vec2 where
  x : Int
  y : Int

-- bad
def Vec2.add (a b : Vec2) : Vec2 := ⟨a.x + b.x, a.y + b.y⟩

infixl:65 " +ᵥ " => Vec2.add
```

```lean
structure Vec2 where
  x : Int
  y : Int

-- good
instance : Add Vec2 where
  add a b := ⟨a.x + b.x, a.y + b.y⟩
```

*Source: [Lean core style][cs-notation].*

<a name="macros-macro-or-elab"></a>
## Macros or elaborators

Use `macro` and `notation` for syntax sugar, where one piece of syntax becomes another. If the translation needs to look at types or make decisions, write an elaborator instead.

*Source: [Metaprogramming in Lean 4][mp-macro].*

<a name="macros-scoped"></a>
## Scoped notation

Declare notation `scoped` inside your namespace, unless it's meant for everyone who imports your library. Users then turn it on with `open`. A `scoped` declaration has to be inside a `namespace`.

```lean
structure Vec2 where
  x : Int
  y : Int

-- good
namespace Vec2

def dot (a b : Vec2) : Int := a.x * b.x + a.y * b.y

scoped infixl:70 " ⬝ " => Vec2.dot

end Vec2

open Vec2 in
def normSquared (v : Vec2) : Int := v ⬝ v
```

*Source: [Lean core style][cs-file].*

<a name="macros-overlap"></a>
## Extending existing syntax

Don't add `macro_rules` that cover only some uses of existing syntax. Which rule applies then depends on details the reader can't see.

*Source: [Metaprogramming in Lean 4][mp-overlap].*

<a name="macros-output"></a>
## Notation in output

Make your notation appear in Lean's output the way users write it. `notation`, `infixl` and the other simple commands do this for you. If you write a `macro`, also write an unexpander.

*Source: [Lean Reference][ref-delab].*

---

Previous: [Comments](comments.md) · [Contents](../README.md#rules) · Next: [Performance and low-level code](performance.md)


[checked]: ../research/decisions.md#facts-checked-while-drafting
[cs-file]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#basic-file-structure
[cs-notation]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/style.md#notation-and-unicode
[mp-macro]: https://github.com/leanprover-community/lean4-metaprogramming-book/blob/9bb0918b272015ad6e39e6db6220fec378a35d8a/lean/main/02_overview.lean#L153-L155
[mp-overlap]: https://github.com/leanprover-community/lean4-metaprogramming-book/blob/9bb0918b272015ad6e39e6db6220fec378a35d8a/lean/main/06_macros.lean#L57-L78
[ref-delab]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/NotationsMacros/Delab.lean#L33
