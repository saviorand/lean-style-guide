# Jane Street OCaml conventions (what is publicly available)

| Field | Value |
|---|---|
| URL | Former style page `https://opensource.janestreet.com/standards/` now **301-redirects to https://github.com/janestreet** (checked 2026-10-17). Used instead: https://github.com/janestreet/ppx_js_style (README), https://github.com/janestreet/base (README.org), ocamlformat `janestreet` profile |
| Author / org | Jane Street Group |
| Date / version | ppx_js_style HEAD `d847928a067accd99edd6c327a836bfb059249d4` (2026-05-15); base `28d466710aa1858a70fd3c1fcbeae07a07ac8106` (2026-07-10) |
| License | base: MIT (`LICENSE.md`, "Copyright (c) 2016--2026 Jane Street Group, LLC"). ppx_js_style: `gh` lists janestreet repos as MIT; README itself not separately licensed (**unverified** for that repo; LICENSE not read). |
| Scope & audience | Jane Street's own code (Base, Core, Async); externally usable lint |
| Kind | normative for Jane Street; descriptive for outsiders |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/ocaml-janestreet-ppx_js_style.md`, `js-base-readme.md`, `ocaml-janestreet-org-page-redirect.md` (the redirect target, not useful) |

## Summary
The prose "Jane Street OCaml Style" page could **not** be retrieved: the old URL redirects to the GitHub org page and the Wayback Machine is blocked in this environment. What is public and primary is a lint ppx that enforces a handful of rules mechanically, the Base README's "coding rules", and a formatter profile. A web search snippet (secondary, not verified here) described the lost page as saying: underscores not CamelCase, short names for short scopes, predicate names like `is_valid`, ocp-indent, ocamlformat `janestreet` profile with 90 columns. Treat that as an **unverified lead**.

## Rules (primary, from the repos)
ppx_js_style README ([permalink](https://github.com/janestreet/ppx_js_style/blob/d847928a067accd99edd6c327a836bfb059249d4/README.md)): "`ppx_js_style` is an identity ppx rewriter that enforces Jane Street coding styles." Enforced rules:
> `[@@deprecated]` attributes must contain the date of deprecation, using the format `"[since MM-YYYY] ..."`
> Ignored expressions must come with a type annotation, such as: `ignore (expr : typ)` / `let (_ : type) = expr`
> Comments in mli must either be documentation comments or explicitly "ignored": `(** documentation comment *)` `(*_ ignored comment *)`. Normal `(* comment *)` comments are disallowed.
> Check for misleading usage of underscores in number literals ... in positions that are multiple of 3 for numbers in decimal notation.
> [binding operators] ... we have made the choice to keep using `ppx_let` internally and to forbid the use of binding operators, to keep a consistent style across our codebase. (rejected at Jane Street, allowed externally)
> `-forbid-inline-never` ... "they would be better off using `[@cold]`"

Base README "Base coding rules" ([README.org L130-L158](https://github.com/janestreet/base/blob/28d466710aa1858a70fd3c1fcbeae07a07ac8106/README.org#L130-L158)):
> Opening the =Stdlib= module is not allowed. ... We forbid opening =Stdlib= so that we know exactly where things come from.
> Indentation is exactly the one of =ocp-indent=.
Rules are "enforced by lint tools".

Partial/total pairs in Base (primary code evidence): `Option.value_exn` raises with optional `?here ?error ?message` arguments ([option.mli L84](https://github.com/janestreet/base/blob/28d466710aa1858a70fd3c1fcbeae07a07ac8106/src/option.mli#L84)); naming scheme `_exn` (raises) vs plain option/`_opt`/`_or_error` returns is visible in the library but **no written rule was found** (unverified lead: `Hashtbl.of_alist_exn` in doc example at option.mli L9).

OCamlFormat `janestreet` profile exists ([getting_started.mld L44-L48](https://github.com/ocaml-ppx/ocamlformat/blob/b6af1c41c0f7c2da15139222da6fe5c1a6ccf158/doc/getting_started.mld#L44-L48)).

## Reasons given
Only for a few lint rules: dated deprecations (traceability, implied), unannotated ignores (type safety), binding operators (consistency with `ppx_let`), explicit `Stdlib` (know where names come from).

## What transfers to general-purpose Lean
- Style enforced by a linter plug-in with opt-in/out flags; "enabled at Jane Street, off externally" shows an internal-vs-public split.
- Dated deprecations (`[since MM-YYYY]`): Lean's `@[deprecated (since := "...")]` has the same idea.
- `_exn` suffix convention for raising variants: Lean's `!` suffix (`get!`) and `?` suffix (`get?`) are the counterparts; worth comparing in the naming topic.
- Doc comments vs ordinary comments distinction in interface files (Lean `/-- -/` vs `--`).

## Caveats and unverified items
- The actual standards page is unobtainable (see Summary). Snippet claims: **unverified**. Suggest the lead try another route (Real World OCaml, or Jane Street blog) if the full text matters.
