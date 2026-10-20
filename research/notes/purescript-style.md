# PureScript library guidelines

| Field | Value |
|---|---|
| URL | https://github.com/purescript/documentation/blob/master/guides/Style-Guide.md |
| Author / org | PureScript core team (documentation repo) |
| Date / version | file last commit `8abc7163980f54e2350b7934ffeb85a7a4cab062` (2020-03-01) |
| License | **CC BY-NC-SA 3.0 Unported** (`LICENSE` in purescript/documentation begins "Attribution-NonCommercial-ShareAlike 3.0 Unported"). Non-commercial and share-alike: **do not copy text into a guide with a more permissive licence**. |
| Scope & audience | Authors of PureScript libraries; "if you would like to contribute to the core libraries" |
| Kind | community advice (official docs repo) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/purescript-style.md` (defuddle of the GitHub page) |

## Summary
Not a code-formatting guide: it is a library-packaging checklist (build tool, docs, tests, examples, CI, publishing, types, modules, FFI, runtime requirements, keeping up to date). No widely-used PureScript formatting style guide was found beyond the `purs-tidy` formatter (not investigated). Closest to Lean's concerns: library hygiene for a young ecosystem.

## Rules
> Try to document every exported type and function.
> Even if a function seems "self-explanatory", it is still better to include a small comment or example to help beginners.
> Include type signatures for top-level declarations. Use type wildcards to infer the type if necessary.
> Use `newtype` to convey additional information about primitive types where applicable (for example, consider using `newtype EmailAddress` instead of just `String`).
> Do not misuse the type system when providing bindings via the FFI. ... PureScript has a rich set of types such as `Foreign` and `FnX` for safe interop with JavaScript
> PureScript follows Haskell conventions for module namespacing.
> Include a module export list in your modules. / Strive to keep module exports minimal.
> consider splitting it into two libraries, a barebones set of FFI bindings, and your extra functionality.
> Write at least one example, which might be a part of your test suite, to document how your library might be used to solve some simple complete use-case.
> Include tests with your project, so that contributors can easily verify their changes.
> Set up continuous integration for your project to verify that your library compiles correctly.
> Note any assumptions about the execution environment (Node-only, browser-only, etc.) in your `README` file.
Section anchors: [Documentation](https://github.com/purescript/documentation/blob/master/guides/Style-Guide.md#documentation), [Types](...#types), [Modules](...#modules), [Foreign Function Interface](...#foreign-function-interface).

## Reasons given
Almost none; bullets are terse. Stale tooling (Bower, Travis, VersionEye) shows the page has not been maintained.

## What transfers to general-purpose Lean
- Library-hygiene sections for the guide: README states assumptions, example in tests, CI, minimal exports, separate FFI binding library from the nice layer.
- "Document every exported item, even self-explanatory ones" vs Mathlib-style docstring requirements.
- `newtype` over primitive for meaning.

## Caveats and unverified items
- Published 2016-2020 tooling; outdated. NC licence blocks reuse of text. Looked for another widely-used PureScript style guide (e.g. purs-tidy docs, Thomas Honeyman's guides); not fetched, **unverified leads**.
