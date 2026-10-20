# Data modelling

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="data-structure-inductive"></a>
## Structures and inductive types

Use a `structure` for a value made of several parts that are all present at once. Use an `inductive` type for a value that is one of several alternatives.

*Source: [FPIL][fpil-product].*

<a name="data-illegal-states"></a>
## Impossible states

Model state so that impossible combinations can't be written down. A structure with flags and optional fields can describe a connection that is both connected and failed. An inductive type with one constructor per state can't.

```lean
-- bad
structure Connection where
  connected : Bool
  sessionId : Option String
  lastError : Option String
```

```lean
-- good
inductive Connection where
  | disconnected
  | connecting (attempt : Nat)
  | connected (sessionId : String)
  | failed (error : String)
```

*Source: [Yaron Minsky][minsky].*

<a name="data-own-types"></a>
## Your own types over tuples

Define a structure with named fields instead of passing pairs and nested tuples around. Field names make the code easier to read and the values harder to mix up.

```lean
-- bad
def distance (a b : Float × Float) : Float :=
  let dx := a.1 - b.1
  let dy := a.2 - b.2
  Float.sqrt (dx * dx + dy * dy)
```

```lean
-- good
structure Point where
  x : Float
  y : Float

def Point.distance (a b : Point) : Float :=
  let dx := a.x - b.x
  let dy := a.y - b.y
  Float.sqrt (dx * dx + dy * dy)
```

*Source: [FPIL][fpil-own].*

<a name="data-wrappers"></a>
## Wrapper types for domain values

Wrap a primitive in a single-field structure when values with the same representation must not be mixed, such as user IDs and article IDs. The wrapper costs nothing at run time. An `abbrev` doesn't help, because Lean treats it as the type it abbreviates. In the bad example, the call with swapped arguments compiles. In the good example, it would be a type error.

```lean
-- bad
abbrev UserId := Nat
abbrev ArticleId := Nat

def deleteArticle (user : UserId) (article : ArticleId) : String :=
  s!"user {user} deletes article {article}"

def mistake (u : UserId) (a : ArticleId) : String := deleteArticle a u
```

```lean
-- good
structure UserId where
  val : Nat
deriving BEq, Hashable, Repr

structure ArticleId where
  val : Nat
deriving BEq, Hashable, Repr

def deleteArticle (user : UserId) (article : ArticleId) : String :=
  s!"user {user.val} deletes article {article.val}"
```

*Sources: FPIL on [separate structures][fpil-separate] and [run-time cost][fpil-wrapper], [Haskell (Kowainik)][kowainik-data], [Rust API guidelines][rust-newtype].*

<a name="data-abbrev"></a>
## `abbrev`, `def` and `structure` for types

Use `abbrev` for a name that should behave exactly like the type it stands for, such as an application's monad. Use a `structure` for a new domain type. Avoid `def` for type synonyms. Lean doesn't look through a `def` when it searches for instances, so even `def p : Port := 8080` fails to compile.

```lean
-- bad
def Port := Nat

def defaultPort : Port := (8080 : Nat)
```

```lean
-- good
abbrev AppM := ReaderT String IO

structure Port where
  val : Nat

def defaultPort : Port := ⟨8080⟩
```

*Sources: FPIL on [`abbrev`][fpil-abbrev] and [monad stacks][fpil-abbrev-stack], [Haskell (Kowainik)][kowainik-data], [checked with Lean 4.35][checked].*

<a name="data-update"></a>
## Updating structures

Use `{ s with field := value }` to change some fields of a structure. If you copy fields by hand, it's easy to swap two fields of the same type without Lean noticing.

```lean
structure Settings where
  width : Nat
  height : Nat
  title : String

-- bad: width and height are swapped by mistake, and it compiles
def rename (s : Settings) (title : String) : Settings :=
  { width := s.height, height := s.width, title := title }
```

```lean
structure Settings where
  width : Nat
  height : Nat
  title : String

-- good
def rename (s : Settings) (title : String) : Settings := { s with title }
```

*Source: [FPIL][fpil-update].*

<a name="data-constructors"></a>
## Building structures

Build structures with named fields, as in `{ name := "Ada", age := 36 }`. Use `⟨…⟩` or `Point.mk` only for small structures where the order of the fields is obvious.

```lean
structure User where
  name : String
  email : String
  age : Nat

-- bad: name and email are swapped, and it compiles
def ada : User := ⟨"ada@example.com", "Ada", 36⟩
```

```lean
structure User where
  name : String
  email : String
  age : Nat

-- good
def ada : User := { name := "Ada", email := "ada@example.com", age := 36 }
```

*Source: [FPIL][fpil-mk].*

<a name="data-deriving"></a>
## Deriving instances

Derive instances instead of writing them by hand, so they stay correct when the type changes. Derive `Repr` for every data type, so you can inspect its values with `#eval`. Derive `Hashable` together with `BEq` for types used as hash map keys. Write an instance by hand only when the derived one does the wrong thing.

```lean
-- bad
structure Version where
  major : Nat
  minor : Nat

instance : BEq Version where
  beq a b := a.major == b.major && a.minor == b.minor
```

```lean
-- good
structure Version where
  major : Nat
  minor : Nat
deriving Repr, BEq, Hashable, Ord
```

*Source: [FPIL][fpil-deriving].*

<a name="data-boundary"></a>
## Checking at the boundary

Check a value once, where it enters your program, and from then on pass a type that records the check. Keep subtypes and proof fields behind an API that maintains them, so callers never write proofs.

```lean
-- bad: every caller has to prove the bound
def listen (port : Nat) (h : port < 65536) : String := s!"listening on {port}"

def start := listen 8080 (by decide)
```

```lean
-- good: `Port.ofNat?` checks once, and the result carries the proof
structure Port where
  val : Nat
  valid : val < 65536

def Port.ofNat? (n : Nat) : Option Port :=
  if h : n < 65536 then some ⟨n, h⟩ else none

def listen (port : Port) : String := s!"listening on {port.val}"
```

*Sources: [Alexis King][king], [FPIL][fpil-subtype], [Std's `HashMap`][std-hashmap].*

<a name="data-indexed-families"></a>
## Indexed families

Avoid indexed families in APIs, such as a vector type indexed by its length. They expose the implementation in the interface, slow down type checking and produce hard-to-read errors. Use them only for code that resembles a typed language, such as an interpreter or a typed syntax tree.

*Source: [FPIL][fpil-indexed].*

<a name="data-extends"></a>
## Inheritance

Use `extends` only when one structure clearly "is a" kind of another.

*Source: [FPIL][fpil-extends].*

---

Previous: [`do` notation and effects](effects.md) · [Contents](../README.md#rules) · Next: [Type classes and instances](classes.md)

[checked]: ../research/decisions.md#facts-checked-while-drafting
[fpil-abbrev]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/FunctionsDefinitions.lean#L224
[fpil-abbrev-stack]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/MonadTransformers/ReaderIO.lean#L337
[fpil-deriving]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L348-L378
[fpil-extends]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Inheritance.lean#L238-L242
[fpil-indexed]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/DependentTypes/Pitfalls.lean#L500-L515
[fpil-mk]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L325
[fpil-own]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L497-L560
[fpil-product]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Summary.lean#L87
[fpil-separate]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L28
[fpil-subtype]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/FunctorApplicativeMonad/Applicative.lean#L225-L227
[fpil-update]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Structures.lean#L243-L246
[fpil-wrapper]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/SpecialTypes.lean#L52
[king]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[kowainik-data]: https://kowainik.github.io/posts/2019-02-06-style-guide#data-types
[minsky]: https://blog.janestreet.com/effective-ml-revisited/
[rust-newtype]: https://rust-lang.github.io/api-guidelines/type-safety.html#c-newtype
[std-hashmap]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/Std/Data/HashMap/Basic.lean#L56-L59
