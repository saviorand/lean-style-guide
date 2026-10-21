# Testing

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="tests-coverage"></a>
## Test coverage

Don't test what the types already guarantee. Test what types and proofs don't cover, such as input parsing, output formats and code that talks to files or the network. Also test performance, such as whether a hot loop updates its arrays in place.

*Sources: FPIL on [types][fpil-types-tests] and [copying][fpil-copy].*

<a name="tests-library"></a>
## A test library

Put tests in a separate library named after your package with `Test` added, such as `MyAppTest`, and make it the package's `testDriver`. `lake test` then builds that library. Each test is a check that runs while the file compiles, so a successful build means the tests passed. Keep tests out of your library's own modules.

```toml
name = "myapp"
testDriver = "MyAppTest"

[[lean_lib]]
name = "MyApp"

[[lean_lib]]
name = "MyAppTest"
```

*Sources: [Lake README][lake-test], [Lean Reference][ref-guardmsgs], [testing practice][testing].*

<a name="tests-guard-msgs"></a>
## Expected output

Check results with `#guard_msgs`. It compares the messages that a command produces, such as the output of `#eval`, with the docstring above it, and the build fails if they differ. Use `#guard` for a check that returns a `Bool`.

```lean
def slug (title : String) : String :=
  "-".intercalate ((title.toLower.splitOn " ").filter (· != ""))

-- good
/-- info: "hello-world" -/
#guard_msgs in
#eval slug "Hello  World"

#guard slug "" == ""
```

*Source: [Lean Reference][ref-guardmsgs].*

<a name="tests-runtime"></a>
## Run-time tests

Some tests have to run `IO`, for example to read files, start a server or talk to a database. For those, make the test driver an executable. `lake test` builds it and runs it, and a non-zero exit code means the tests failed.

```lean
def checks : List (String × Bool) :=
  [("empty", "".isEmpty), ("upper", "abc".toUpper == "ABC")]

-- good
def main : IO UInt32 := do
  let failed := checks.filter fun (_, ok) => !ok
  for (name, _) in failed do
    IO.eprintln s!"FAIL {name}"
  return if failed.isEmpty then 0 else 1
```

*Sources: [Lake README][lake-test], [testing practice][testing].*

<a name="tests-property"></a>
## Property tests

When a function has a clear property, such as "decoding an encoded value gives back the original", test it on random inputs with [Plausible](https://github.com/leanprover-community/plausible).

<!-- nocheck -->
```lean
import Plausible

#eval Plausible.Testable.check <| ∀ (xs : List Nat), xs.reverse.reverse = xs
```

*Sources: [testing practice][testing], [Google Haskell guide][google-quickcheck].*

<a name="tests-meta-import"></a>
## Tests and the module system

If your test files are modules, import the code they `#eval` with `meta import`. Your editor makes every import available to `#eval`, but `lake build` doesn't. Without `meta import`, a test can pass in the editor and fail in the build.

<!-- nocheck -->
```lean
module

meta import MyApp.Slug

/-- info: "hello-world" -/
#guard_msgs in
#eval slug "Hello  World"
```

*Source: [Lean Reference][ref-meta-eval].*

---

Previous: [Proofs about programs](proofs.md) · [Contents](../README.md#rules) · Next: [Documentation](documentation.md)

[fpil-copy]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L512-L513
[fpil-types-tests]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Summary.lean#L57
[google-quickcheck]: https://google.github.io/styleguide/haskellguide.html#quickcheck
[lake-test]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md#test--lint
[ref-guardmsgs]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L547-L553
[ref-meta-eval]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L95-L96
[testing]: ../research/notes/testing-practice.md
