# Projects and tooling

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="project-layout"></a>
## Package layout

Start from the layout that `lake new` creates. The library lives in `MyApp/`, with a root module `MyApp.lean` that imports its parts. `Main.lean` stays a small wrapper that parses the command line and calls the library. A library whose tests need extra dependencies keeps them in a `test/` subproject instead (see [A test library](testing.md#tests-library)).

```text
myapp/
├── lakefile.toml
├── lake-manifest.json
├── lean-toolchain
├── Main.lean
├── MyApp.lean
├── MyApp/
│   ├── Basic.lean
│   └── Http/
│       └── Router.lean
├── MyAppTest.lean
└── MyAppTest/
    └── Router.lean
```

*Source: [FPIL][fpil-main].*

<a name="project-dependencies"></a>
## Toolchain and dependencies

Commit `lean-toolchain`, which pins the Lean version, and `lake-manifest.json`, which records the exact commit of every dependency. Require each dependency at a release tag when it has one, rather than at a branch. Upgrade Lean in a change of its own.

```toml
[[require]]
name = "routing"
git = "https://github.com/paulbutcher/lean-routing"
rev = "v0.8.0"
```

*Source: [Lake README][lake-manifest].*

<a name="project-options"></a>
## Lean options

Set project-wide options in the Lake configuration, so they apply to every file. Turn off automatic implicit arguments everywhere.

```toml
[leanOptions]
autoImplicit = false
```

*Source: [Mathlib configuration][ml-autoimplicit].*

<a name="project-warnings"></a>
## Warnings

Keep the build free of warnings, and check it in CI with `lake build --wfail`. Don't set `warningAsError` in a library's own configuration. Lake builds each dependency with its own options, so a warning added in a new Lean release would then break every project that uses your library.

*Sources: [Google Haskell guide][google-warnings], [RealWorld app][realworld], [checked with Lean 4.35][checked].*

<a name="project-linters"></a>
## Linters

Keep Lean's built-in linters, such as the unused-variables linter, turned on.

*Source: [linter defaults][survey-linters].*

<a name="project-formatting"></a>
## Formatting changes

Don't reformat code you aren't otherwise changing, because it buries real changes in the diff. When an official formatter is released, run it over the whole project in one commit that does nothing else.

*Source: [Lean contributing guide][lean-contributing].*

---

Previous: [Performance and low-level code](performance.md) · [Contents](../README.md#rules) · Next: [Source code layout](layout.md)

[checked]: ../research/decisions.md#facts-checked-while-drafting
[fpil-main]: https://github.com/leanprover/fp-lean/blob/0abeea545d560a324e2561f7210fbd6ed154fa02/book/FPLean/HelloWorld/StartingAProject.lean#L40
[google-warnings]: https://google.github.io/styleguide/haskellguide.html#warnings
[lake-manifest]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/src/lake/README.md?plain=1#L441
[lean-contributing]: https://github.com/leanprover/lean4/blob/3a685e6c855f0eb4ccabe92e21120f1b1ef81d24/CONTRIBUTING.md?plain=1#L35
[ml-autoimplicit]: https://github.com/leanprover-community/mathlib4/blob/7bb03b4c5313d552989ba5b1c6d3f0f436f65d73/lakefile.lean#L44
[realworld]: https://github.com/saviorand/lean-realworld-example-app/blob/a25664892b8bdf84722bcc24d31286560f975186/lakefile.toml#L13
[survey-linters]: ../research/stdlib-survey.md#15-tooling-linters-and-formatters
