# agda-stdlib style guide (doc/style-guide.md)

| Field | Value |
|---|---|
| URL | https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md |
| Author / org | Agda standard library maintainers |
| Date / version | repo HEAD `2ffa8b7d4e8e818717ad643d184f055a4d1b0447` (2026-09-12); file last changed in `810f87395c45a5dc06dc2815f69a1fbc8260e961` (2026-08-30) |
| License | MIT (text in `LICENCE`, "Copyright (c) 2007-2026 Nils Anders Danielsson, Ulf Norell, ..."; `vendor/pages/proof-assistants/agda-LICENCE`); GitHub API reports NOASSERTION because of the filename |
| Scope & audience | agda-stdlib contributors |
| Kind | normative |
| Lean version | n/a (Agda) |
| Raw copy | `vendor/pages/proof-assistants/agda-stdlib-style.md` |

## Summary
A mostly layout-and-naming guide (indentation, imports, record layout, symbols for operators). The parts relevant to a general Lean guide are the naming rules for proofs (preconditions in names, `f⁺`/`f⁻` introduction/elimination lemmas, `-local` suffix), the policy on which `variable`s a file may declare, the implicit-argument rule, and short "idiomatic pattern" notes (restrict `pattern` synonyms to Base/Core modules; avoid unnecessary `with`). The guide says nothing about when to prove, bundling, or termination. The Base/Properties module split is visible in the guide only indirectly.

## Rules
Implicit arguments:
> Function arguments should be implicit if they can "almost always" be inferred. If there are common cases where they cannot be inferred then they should be left explicit.
([Types](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L449-L452))

Variables:
> A file may only declare variables of other types if those types are used in the definition of the main type that the file concerns itself with. At the moment the policy is *not* to generalise over any other types to minimise the amount of information that users have to keep in their head concurrently.
([Variables](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L458-L477))

Descriptive names:
> Names should be descriptive - i.e. given the name of a proof and the module it lives in, then users should be able to make a reasonable guess at its meaning.
([Naming](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L479-L482))

Preconditions and postconditions in names:
> Preconditions should only be included in names of results if "important" (mostly a judgment call). / Preconditions of results should be prepended to a description of the result by using the symbol `⇒` in names (e.g. `asym⇒antisym`)
([Preconditions and postconditions](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L521-L536))

Introduction/elimination lemmas:
> `f⁺` is a lemma of the form `Precondition -> P(f)` / `f⁻` is a lemma of the form `P(f) -> Postcondition` [...] `⁺` makes f appear in the conclusion while `⁻` makes it disappear from the hypothesis.
([Functions and relations over specific datatypes](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L661-L687))

Local versions:
> The naming convention is to add a `-local` suffix on to the name of the latter variety. e.g. `map-id : map id xs ≡ xs`, `map-id-local : All (λ x → f x ≡ x) xs → map f xs ≡ xs`
([same section](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L661-L687))

Modules (paraphrase): one named module per file; named internal modules are opened publicly or split out; no single-letter named modules exported publicly ([Modules](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L84-L96)).

Pattern synonyms:
> their use should be restricted to `Base` or `Core` modules, and not pollute the namespaces of `Properties` or other modules.
([Use of pattern synonyms](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L705-L711))

`with`: "Thinking on this has changed since the early days of the library, with a desire to avoid 'unnecessary' uses of `with`" (issues #1937, #2123 linked) ([L713-L718](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L713-L718)).

Decidability: points to issue #803 for "a programming pattern for writing proofs of decidability" (not read) ([L720-L727](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L720-L727)).

## Reasons given
- Variables policy: "to minimise the amount of information that users have to keep in their head concurrently".
- `contradiction` over `⊥-elim`: "clearer documentation for readers of the code" ([L729-L736](https://github.com/agda/agda-stdlib/blob/2ffa8b7d4e8e818717ad643d184f055a4d1b0447/doc/style-guide.md#L729-L736)).
- Pattern synonyms: namespace pollution.
- Most other rules give no reason.

## What transfers to general-purpose Lean
- Naming of lemmas: "name states the result, with an important precondition marked" and the introduction/elimination (`⁺`/`⁻`) idea is the same as Lean's `_of_`/`_iff` suffixes, but Lean core has its own naming doc (`doc/std/naming.md`), which should win.
- The "restrict what a file may generalise over" policy is a transferable idea for Lean `variable` declarations.
- The Base/Properties split (definitions in one module, lemmas in another) is the Agda-side counterpart of the Lean stdlib's `Basic`/`Lemmas` split. The guide does not state it as a rule: **unverified** whether it is documented elsewhere in the repo (`doc/README` and `HACKING.md` were grepped; nothing found).
- Unicode operator conventions, layout and `Level` rules do not transfer.

## Caveats and unverified items
- Agda has no termination-checker-vs-proof guidance here.
- Several sections are stubs (e.g. "Proving instances of Decidable" only links issues).
