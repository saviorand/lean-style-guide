# Naming

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="naming-case"></a>
## Case by kind

Name types, structures, classes, inductive types, namespaces and `Prop`-valued predicates in `UpperCamelCase`. Name functions, values, structure fields and constructors in `lowerCamelCase`. Name theorems in `snake_case`.

```lean
-- bad
structure http_request where
  Method : String
  request_path : String

def Is_Get (r : http_request) : Bool := r.Method == "GET"
```

```lean
-- good
structure HttpRequest where
  method : String
  path : String

inductive Status where
  | ok
  | notFound

def HttpRequest.isGet (r : HttpRequest) : Bool := r.method == "GET"

def double (n : Nat) : Nat := 2 * n

theorem double_add (a b : Nat) : double (a + b) = double a + double b := by
  unfold double
  omega
```

*Source: [Lean naming conventions][cn-prelude].*

<a name="naming-acronyms"></a>
## Acronyms

Write acronyms of four or more letters as words: `Json`, `Http`, `parseJson`, `HttpServer`. Keep acronyms of up to three letters in one case: `IO`, `URL`, `toURL`, `urlPath`. Keep established mixed-case spellings such as `IPv4Addr`.

*Source: [Lean naming conventions][cn-acronyms].*

<a name="naming-namespaces"></a>
## Namespaces and dot notation

Put the functions about a type in the namespace named after the type. Callers can then use dot notation, where `r.isGet` means `Request.isGet r`.

```lean
structure Request where
  method : String

-- bad
def requestIsGet (r : Request) : Bool := r.method == "GET"

def handle (r : Request) : String :=
  if requestIsGet r then "read" else "write"
```

```lean
structure Request where
  method : String

-- good
def Request.isGet (r : Request) : Bool := r.method == "GET"

def handle (r : Request) : String :=
  if r.isGet then "read" else "write"
```

*Source: [Lean naming conventions][cn-ns].*

<a name="naming-predicates"></a>
## Predicates

Start the name of a `Bool`-valued function with a word that makes it a question, such as `isEmpty`, `hasKey` or `canRetry`. Name a `Prop`-valued predicate in `UpperCamelCase` with the prefix `Is`, unless that would be ungrammatical. In program code, prefer `Bool` functions, and write a `Prop` only when you plan to prove things about it.

```lean
structure Order where
  total : Nat
  paid : Nat

-- good
def Order.isPaid (o : Order) : Bool := o.paid ≥ o.total

def IsAscending (xs : List Nat) : Prop := xs.Pairwise (· ≤ ·)
```

*Sources: [Lean naming conventions][cn-types], [FPIL][fpil-bool].*

<a name="naming-failure"></a>
## Functions that can fail

If a function can fail, say how in its name:

- `price?` returns an `Option`.
- `price!` panics on failure. Call it only where failure would be a bug.
- `priceD` takes a default value and returns it on failure.
- `price`, with no suffix, can't fail, or takes a proof that it won't.

```lean
-- good
structure PriceList where
  prices : List (String × Nat)

namespace PriceList

def price? (p : PriceList) (item : String) : Option Nat :=
  p.prices.lookup item

def priceD (p : PriceList) (item : String) (default : Nat) : Nat :=
  (p.price? item).getD default

def price! (p : PriceList) (item : String) : Nat :=
  (p.price? item).get!

end PriceList
```

If you provide a `!` variant, provide a `?` variant too, so callers who can't rule out failure have a safe choice.

*Sources: [Lean naming conventions][cn-data], [FPIL][fpil-failure], [Ruby guide][ruby-bang], [standard library][survey-names].*

<a name="naming-conversions"></a>
## Conversions

Name a conversion `toX` in the source type's namespace and `ofX` in the target type's namespace. Don't use `fromX`.

```lean
structure Celsius where
  degrees : Float

structure Fahrenheit where
  degrees : Float

-- bad
def Celsius.fromFahrenheit (f : Fahrenheit) : Celsius := ⟨(f.degrees - 32) * 5 / 9⟩
```

```lean
structure Celsius where
  degrees : Float

structure Fahrenheit where
  degrees : Float

-- good
def Celsius.ofFahrenheit (f : Fahrenheit) : Celsius := ⟨(f.degrees - 32) * 5 / 9⟩

def Celsius.toFahrenheit (c : Celsius) : Fahrenheit := ⟨c.degrees * 9 / 5 + 32⟩
```

*Source: [standard library][survey-conv].*

<a name="naming-monadic"></a>
## Monadic variants

Add `M` to the name of a variant that runs in a monad, as in `mapM` and `forM`. A pure `validate` and a `validateM` that runs in `IO` can then live side by side.

*Source: [Lean Reference][ref-monadapi].*

<a name="naming-primes"></a>
## Primes

Don't name a variant of a public function by adding `'`. Pick a name that says what is different. Primes are fine for short-lived locals such as `acc'`.

```lean
-- bad
def splitWords (s : String) : List String := s.splitOn " "

def splitWords' (s : String) : List String := (s.splitOn " ").filter (· != "")
```

```lean
-- good
def splitWords (s : String) : List String := s.splitOn " "

def splitNonemptyWords (s : String) : List String := (s.splitOn " ").filter (· != "")
```

*Source: [Lean naming conventions][cn-primes].*

<a name="naming-locals"></a>
## Local names

Short names are fine for locals with a small scope, if they follow these conventions:

| Name | Used for |
|---|---|
| `α`, `β`, `γ` | type parameters with no more specific meaning |
| `xs`, `ys` | arrays |
| `l`, `as`, `bs` | lists |
| `acc` | an accumulator |
| `i`, `j`, `k` | indices |
| `n`, `m` | sizes and other natural numbers |
| `f`, `g` | functions |
| `h`, `h₁`, `h₂` | proofs of hypotheses |
| `m` | a monad, in type signatures |
| `ε` | an error type |

Give everything that lives longer than a few lines a descriptive name, including structure fields and public function arguments.

*Sources: [Lean naming conventions][cn-vars], FPIL on [type variables][fpil-names] and [field names][fpil-fields].*

<a name="naming-instances"></a>
## Instances

Leave instances anonymous. Name one only if you need to refer to it.

```lean
inductive Color where
  | red
  | green

-- bad
instance instToStringColor : ToString Color where
  toString
    | .red => "red"
    | .green => "green"
```

```lean
inductive Color where
  | red
  | green

-- good
instance : ToString Color where
  toString
    | .red => "red"
    | .green => "green"
```

*Source: [FRO practice][fro-c].*

<a name="naming-files"></a>
## Packages, modules and files

Name packages and executables in lowercase. Name modules in `UpperCamelCase`. The module `MyApp.Http.Router` lives in `MyApp/Http/Router.lean`.

*Source: [FPIL][fpil-packages].*

---

Previous: [Source code layout](layout.md) · [Contents](../README.md#rules) · Next: [Functions](functions.md)


[cn-acronyms]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#acronyms
[cn-data]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#naming-convention-for-data
[cn-ns]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#namespaces-and-generalized-projection-notation
[cn-prelude]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#prelude
[cn-primes]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#primed-names
[cn-types]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#naming-convention-for-types
[cn-vars]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/doc/std/naming.md#variable-names
[fpil-bool]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/TypeClasses/StandardClasses.lean#L150
[fpil-failure]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L419-L420
[fpil-fields]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/DatatypesPatterns.lean#L86
[fpil-names]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Polymorphism.lean#L45
[fpil-packages]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StartingAProject.lean#L104
[fro-c]: ../research/author-survey.md#consistent-across-authors
[ref-monadapi]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Monads/API.lean#L25
[ruby-bang]: https://github.com/rubocop/ruby-style-guide/blob/357eb786d6b7c2dbaaf57820bc997c03adb75c19/README.adoc?plain=1#L1112-L1138
[survey-conv]: ../research/stdlib-survey.md#addendum-conversion-names-2026-10-20
[survey-names]: ../research/stdlib-survey.md#1-naming
