# ocamlformat design and profiles

| Field | Value |
|---|---|
| URL | https://github.com/ocaml-ppx/ocamlformat |
| Author / org | ocaml-ppx / OCaml Labs, originally Facebook (Reason lineage) |
| Date / version | `b6af1c41c0f7c2da15139222da6fe5c1a6ccf158`, 2026-10-07 |
| License | MIT (`LICENSE`; copyrights Facebook 2017-2023, Aaron VonderHaar etc.) |
| Scope & audience | OCaml project maintainers |
| Kind | descriptive (tool design) |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/ocaml-ocamlformat-readme.md`, `ocaml-ocamlformat-faq.mld` |

## Summary
ocamlformat is a configurable formatter but argues explicitly against configuring it. It ships profiles (`conventional`/`default`, `ocamlformat`, `janestreet`), recommends pinning a profile and tool version in `.ocamlformat`, and quotes Prettier's "option philosophy" to say more options means more debate.

## Rules / decisions
README ([L17-L20](https://github.com/ocaml-ppx/ocamlformat/blob/b6af1c41c0f7c2da15139222da6fe5c1a6ccf158/README.md#L17-L20)):
> **ocamlformat** is a code formatter for OCaml. It comes with opinionated default settings but is also fully customizable to suit your coding style.
> **Profiles:** ... Profiles include `default`, `ocamlformat`, `janestreet`.

FAQ, config ([faq.mld L18-L33](https://github.com/ocaml-ppx/ocamlformat/blob/b6af1c41c0f7c2da15139222da6fe5c1a6ccf158/doc/faq.mld#L18-L33)):
> The recommended way is to use a versioned default profile ... `profile = default` / `version = 0.29.0`
> ... If somebody else working on the project tries to use a different version, they will see an error message instead of reformatting the whole project in a different way.

FAQ, custom style ([faq.mld L36-L51](https://github.com/ocaml-ppx/ocamlformat/blob/b6af1c41c0f7c2da15139222da6fe5c1a6ccf158/doc/faq.mld#L36-L51)):
> Can OCamlFormat support my style? No. It is better to see OCamlFormat as a tool to apply a style, rather than a tweakable tool to enforce your existing style.
> ... it is better not to set individual options to override what the default profile is doing.
> OCamlFormat has a few options because of history. But we don't want more of them. By far the biggest reason for adopting OCamlFormat is to stop all the on-going debates over styles. ... The debates over styles just turn into debates over which OCamlFormat options to use. (paraphrasing Prettier, as the FAQ says)

Profiles ([getting_started.mld L44-L60](https://github.com/ocaml-ppx/ocamlformat/blob/b6af1c41c0f7c2da15139222da6fe5c1a6ccf158/doc/getting_started.mld#L44-L60)):
> The [conventional] (or [default]) profile aims to be as familiar and "conventional" appearing as the available options allow.
The `ocamlformat` profile states priorities: "Legibility, in the sense of making it as hard as possible for quick visual parsing to give the wrong interpretation, is of highest priority"; "Whenever possible the high-level structure of the code should be obvious by looking only at the left margin"; "All else equal compact code is preferred".

## Reasons given
Debate avoidance (Prettier quote); version pinning to prevent project-wide reformatting; profile design goals above.

## What transfers to general-purpose Lean
- The position "configurable but discouraged, pin the profile" is a third option between Ormolu (no config) and Fourmolu (everything configurable).
- Style guide should name a canonical profile rather than a bag of options.
- The `ocamlformat` profile's three priorities (legibility, structure visible from left margin, compactness) are a reusable layout rationale.
- Recording a formatter version in the repo (like `lean-toolchain`) is the analogous practice.

## Caveats and unverified items
- Did not read the full option list (`doc/configuration.mld`) or compare profile deltas; the `janestreet` profile contents are not extracted.
