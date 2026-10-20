# API design and visibility

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="api-modules"></a>
## Modules

Use the module system in libraries. Start each file with `module`, import what your public API needs with `public import`, and put the code in a `public section`. Use `@[expose] public section` only in files whose definitions other code needs to unfold in proofs. Each `public` and `@[expose]` you remove saves rebuilds. `lake new` doesn't add `module`, so add it yourself.

```lean
module

public import Std.Data.HashMap

public section

/-- Returns how often each word occurs in `words`, ignoring case. -/
def histogram (words : List String) : Std.HashMap String Nat :=
  words.foldl (fun counts w => counts.insert (normalize w) (counts.getD (normalize w) 0 + 1)) {}
where
  normalize (w : String) : String := w.toLower

end
```

*Sources: [Lean Reference][ref-modules], [checked with Lean 4.35][checked].*

<a name="api-private"></a>
## Private and internal declarations

Mark helpers that aren't part of your API `private`. If a declaration has to stay public for technical reasons, for example because another module of the same library uses it, put it in a namespace called `Internal`.

```lean
-- good
namespace Csv

private def splitLine (line : String) : List String := line.splitOn ","

namespace Internal

def parseRows (text : String) : List (List String) := (text.splitOn "\n").map splitLine

end Internal

def parse (text : String) : List (List String) := Internal.parseRows text

end Csv
```

*Source: [Lean naming conventions][cn-std].*

<a name="api-protected"></a>
## Protected names

Mark a declaration `protected` when its short name would clash with a common name after someone opens its namespace. Here, `open Vec2` doesn't hide the global `toString`.

```lean
structure Vec2 where
  x : Int
  y : Int

-- good
namespace Vec2

protected def toString (v : Vec2) : String := s!"({v.x}, {v.y})"

end Vec2

open Vec2 in
def describe (v : Vec2) (count : Nat) : String := s!"{v.toString} × {toString count}"
```

*Source: [FPIL][fpil-protected].*

<a name="api-open"></a>
## `open`

Open a namespace for a whole file only if the file uses it throughout. For a single declaration, write `open Foo in` in front of it.

```lean
import Std.Data.HashMap

-- good
open Std in
def emptyCounts : HashMap String Nat := {}
```

*Source: [F# component design][fs-component].*

<a name="api-variable"></a>
## `variable`

Avoid `variable` in program code. Write each declaration's parameters in its own signature, so readers see them without scrolling up.

```lean
-- bad
section
variable {α : Type} [ToString α] (sep : String)

def joinAll (xs : List α) : String := sep.intercalate (xs.map toString)

end
```

```lean
-- good
def joinAll {α : Type} [ToString α] (sep : String) (xs : List α) : String :=
  sep.intercalate (xs.map toString)
```

*Sources: [agda-stdlib style guide][agda-variable], [FRO practice][fro-all].*

<a name="api-deprecation"></a>
## Deprecation

Before you rename or remove a public declaration, mark it `@[deprecated newName (since := "YYYY-MM-DD")]` and keep it for a while. Lean then warns everyone who still uses the old name and tells them the new one.

```lean
-- good
def fetchUrl (url : String) : String := url

@[deprecated fetchUrl (since := "2026-10-20")]
def getUrl (url : String) : String := fetchUrl url
```

*Source: [Mathlib style][ml-deprecation].*

<a name="api-surface"></a>
## Small public surface

Make public only what callers need. You have to keep every public declaration working or deprecate it.

*Source: [Rust API guidelines][rust-private].*

---

Previous: [Performance and low-level code](performance.md) · [Contents](../README.md#rules) · Next: [Macros and notation](macros.md)


[agda-variable]: https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md
[checked]: ../research/decisions.md#facts-checked-while-drafting
[cn-std]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#the-std-namespace
[fpil-protected]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/Monads/IO.lean#L153
[fro-all]: ../research/author-survey.md
[fs-component]: https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/component-design-guidelines
[ml-deprecation]: https://leanprover-community.github.io/contribute/style.html#deprecation
[ref-modules]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/SourceFiles.lean#L843-L848
[rust-private]: https://rust-lang.github.io/api-guidelines/future-proofing.html#c-struct-private
