# Testing

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="tests-coverage"></a>
## Test coverage

Don't test what the types already guarantee. Test what types and proofs don't cover, such as input parsing, output formats and code that talks to files or the network. Also test performance, such as whether a hot loop updates its arrays in place.

*Sources: FPIL on [types][fpil-types-tests] and [copying][fpil-copy].*


<a name="tests-literals"></a>
## Tests that restate the source

Don't write a test that compares a value with a literal copied from the source, with no computation in between. It can fail only if someone retypes the literal wrong, and it has to change every time the value does.

```lean
def defaultPort : Nat := 8080

-- bad
#guard defaultPort == 8080
```

```lean
def defaultPort : Nat := 8080

def serverUrl (host : String) (port : Nat := defaultPort) : String := s!"http://{host}:{port}"

-- good
#guard serverUrl "localhost" == "http://localhost:8080"
```

*Source: [Paul Butcher, issue #1][issue-1].*
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

For a library whose tests need packages its users don't, such as Plausible, put the tests in a `test/` subproject instead. Lake has no test-only dependencies, so every `require` in your package's configuration also reaches every package that depends on yours. The subproject requires your package by path and has its own test driver. The root configuration runs it from a test driver script:

<!-- nocheck -->
```lean
-- lakefile.lean
import Lake
open Lake DSL

package mylib

lean_lib MyLib

@[test_driver]
script tests do
  let child ← IO.Process.spawn { cmd := "lake", args := #["test"], cwd := __dir__ / "test" }
  child.wait
```

<!-- nocheck -->
```lean
-- test/lakefile.lean
import Lake
open Lake DSL

package mylibTest

require mylib from ".."

@[test_driver]
lean_lib MyLibTest
```

`lake test` in the root then runs the tests and fails if they fail, while the root's `lake-manifest.json` lists none of the test dependencies.

*Sources: [Lake README][lake-test], [Lean Reference][ref-guardmsgs], [testing practice][testing], [Paul Butcher, issue #1][issue-1], [checked with Lean 4.35][checked].*

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


<a name="tests-golden"></a>
## Golden files

Compare output with a saved copy only where its exact form is what you promise, such as a file format, a protocol message or an error message that people read. `#guard_msgs` does this for short output. For longer output, keep the expected output in a file next to the test, as Lean's own test suite does. When the output changes on purpose, regenerate the file with a script and review the diff, rather than copying the new output over it. Where only the meaning matters, as with generated HTML, check the meaning instead, for example by parsing the output and checking the parts you care about, so that a harmless change to the markup doesn't break the test.

*Sources: [Lean's test suite][lean-tests-expected], [Paul Butcher, issue #1][issue-1].*
<a name="tests-runtime"></a>
## Run-time tests

Some tests have to run `IO`, for example to read files, start a server or talk to a database. For those, make the test driver an executable. `lake test` builds it and runs it, and a non-zero exit code means the tests failed.

```lean
/-- Writes `lines` to `path`, each followed by a newline. -/
def writeLines (path : System.FilePath) (lines : List String) : IO Unit :=
  IO.FS.writeFile path (String.join (lines.map (· ++ "\n")))

-- good
def main : IO UInt32 := do
  let path : System.FilePath := "write-lines-test.txt"
  writeLines path ["a", "b"]
  let written ← IO.FS.readFile path
  IO.FS.removeFile path
  if written == "a\nb\n" then return 0
  IO.eprintln s!"FAIL writeLines: {written.quote}"
  return 1
```

*Sources: [Lake README][lake-test], [testing practice][testing].*

<a name="tests-property"></a>
## Property tests

When a property of your own code can't be proved yet (see [Proofs first](proofs.md#proofs-first)), test it on random inputs with [Plausible](https://github.com/leanprover-community/plausible). Write the property out with `Plausible.Testable.check`, which fails the build when it finds a counterexample. Don't use the `plausible` tactic in tests. When it finds no counterexample, it closes the goal with `sorry`, so the build warns and `lake build --wfail` fails.

<!-- nocheck -->
```lean
import Plausible

/-- Puts a backslash before every comma and backslash in `s`. -/
def escape (s : String) : String :=
  s.foldl (fun acc c => if c == ',' || c == '\\' then (acc.push '\\').push c else acc.push c) ""

/-- Removes the backslashes that `escape` adds. -/
def unescape (s : String) : String := Id.run do
  let mut out := ""
  let mut escaped := false
  for c in s.toList do
    if escaped then
      out := out.push c
      escaped := false
    else if c == '\\' then
      escaped := true
    else
      out := out.push c
  return out

-- good
-- Not proved yet: the loop in `unescape` needs an invariant that relates `escaped` to the input.
#eval Plausible.Testable.check (∀ s : String, unescape (escape s) = s)
```

*Sources: [testing practice][testing], [Google Haskell guide][google-quickcheck], [Paul Butcher, issue #1][issue-1], [checked with Lean 4.35][checked].*
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

[checked]: ../research/decisions.md#facts-checked-while-drafting
[fpil-copy]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/ProgramsProofs/InsertionSort.lean#L512-L513
[fpil-types-tests]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/GettingToKnow/Summary.lean#L57
[google-quickcheck]: https://google.github.io/styleguide/haskellguide.html#quickcheck
[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
[lake-test]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md#test--lint
[lean-tests-expected]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/tests/README.md?plain=1#L192-L199
[ref-guardmsgs]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L547-L553
[ref-meta-eval]: https://github.com/leanprover/reference-manual/blob/400f1682df64bc00e485215bfa4398d24c0f220c/Manual/Interaction.lean#L95-L96
[testing]: ../research/notes/testing-practice.md
