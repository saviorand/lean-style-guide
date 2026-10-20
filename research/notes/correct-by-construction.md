# Correct by construction: "make illegal states unrepresentable", "parse, don't validate", "ghosts of departed proofs", Wlaschin

Combined note, four primary sources. All are about ML/Haskell/F#, not Lean; they are the usual citations for the design ideas a Lean guide would restate.

| Field | Value |
|---|---|
| URL | (1) https://blog.janestreet.com/effective-ml-revisited/ (2) https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ (3) https://kataskeue.com/gdp.pdf (4) https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/ |
| Author / org | (1) Yaron Minsky, Jane Street (2) Alexis King (3) Matt Noonan, Kataskeue LLC / Input Output HK, Haskell Symposium '18 (4) Scott Wlaschin |
| Date / version | (1) 2011-03-09 (date from the page; "Effective ML Revisited") (2) 2019-11-05 (3) 2018-09 (ACM Haskell '18; "Functional Pearl") (4) 2013-01-14 |
| License | (1) none stated; footer "Copyright 2015-2026 Jane Street Group, LLC. All rights reserved." (2) none stated; footer "© 2025, Alexis King" (3) ACM copyright notice on the paper; author-hosted PDF; no open licence found (4) none found on the page (site-wide terms not checked) |
| Scope & audience | Practitioners in typed functional languages |
| Kind | community advice (all four) |
| Lean version | n/a (OCaml, Haskell, Haskell, F#) |
| Raw copy | `vendor/pages/proof-assistants/minsky-effective-ml-revisited.md`, `king-parse-dont-validate.md`, `noonan-gdp.pdf` / `noonan-gdp.txt`, `wlaschin-illegal-states.md` |

## Summary
All four say: put the invariant into the types so callers cannot construct or pass bad data, and establish the invariant once, at the boundary. They differ in mechanism. Minsky: split a record of optionals into a sum type with per-state records. King: change the argument type (`NonEmpty a`) rather than weaken the result (`Maybe a`), parse once at the boundary, and use an abstract newtype with a smart constructor when full indexing is impractical. Noonan: a library author attaches "ghost" proofs to phantom type parameters of a newtype, so callers can prove preconditions in their own way, with no runtime cost. Wlaschin: derive the sum type from the business rule.

## Rules / claims
**Minsky** gives the slogan as a heading and a before/after example only; the post has no prose argument.
> ### Make illegal states unrepresentable
Before: one record with `state : connection_state` plus several `option` fields (`last_ping_time`, `session_id`, ...). After: `Connecting of connecting | Connected of connected | Disconnected of disconnected`, each with exactly the fields valid in that state. ([Minsky](https://blog.janestreet.com/effective-ml-revisited/)) Wlaschin credits the phrase to this post: "a phrase borrowed from Yaron Minsky" ([Wlaschin](https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/)); this is a secondary attribution.

**King** ([post](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)), section "Parsing, not validating, in practice":
> **Use a data structure that makes illegal states unrepresentable.** Model your data using the most precise data structure you reasonably can. If ruling out a particular possibility is too hard using the encoding you are currently using, consider alternate encodings that can express the property you care about more easily. Don't be afraid to refactor.

> **Push the burden of proof upward as far as possible, but no further.** Get your data into the most precise representation you need as quickly as you can. Ideally, this should happen at the boundary of your system, before *any* of the data is acted upon.

> **Let your datatypes inform your code, don't let your code control your datatypes.** Avoid the temptation to just stick a `Bool` in a record somewhere because it's needed by the function you're currently writing.

> **Avoid denormalized representations of data, *especially* if it's mutable.** [...] Strive for a single source of truth. / **Keep denormalized representations of data behind abstraction boundaries.**

> **Use abstract datatypes to make validators "look like" parsers.** Sometimes, making an illegal state truly unrepresentable is just plain impractical given the tools Haskell provides, such as ensuring an integer is in a particular range. In that case, use an abstract `newtype` with a smart constructor to "fake" a parser from a validator.

> **Treat functions that return `m ()` with deep suspicion.**

On when not to: 
> As always, use your best judgement. It probably isn't worth breaking out singletons and refactoring your entire application just to get rid of a single `error "impossible"` call somewhere—just make sure to treat those situations like the radioactive substance they are, and handle them with the appropriate care. If all else fails, at least leave a comment to document the invariant for whoever needs to modify the code next.

Strengthen-the-argument vs weaken-the-result: section "Turning partial functions total" ("Managing expectations" weakens the result to `Maybe`; "Paying it forward" strengthens the argument; "By strengthening the type of the argument to `head` instead of weakening the type of its result, we've completely eliminated all the problems from the previous section"). The term "shotgun parsing" is quoted from Sassaman et al. (LangSec) in section "The danger of validation".

**Noonan** ([paper](https://kataskeue.com/gdp.pdf), abstract):
> Library authors often are faced with a design choice: should a function with preconditions be implemented as a partial function, or by returning a failure condition on incorrect use? Neither option is ideal. Partial functions lead to frustrating run-time errors. Failure conditions must be checked at the use-site, placing an unfair tax on the users who have ensured that the function's preconditions were correctly met.

> sophisticated preconditions can be encoded in Haskell's type system with no run-time overhead, by using proofs that inhabit phantom type parameters attached to newtype wrappers. [...] Critically, this technique allows the library user to decide when and how to validate that the API's preconditions are met.

The mechanism (paraphrase of §1-§3 as skimmed): the library hides the constructor of a `Named`-style newtype and exports "proof combinators"; the encapsulation relies on hiding the constructor ("By hiding the constructor of Named, this module ensures..."). The paper frames this as API design for safe, ergonomic use ("Safe" = no run-time error; "Ergonomic" = correct use puts no undue burden on the user).

**Wlaschin** ([post](https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/)): works from the business rule "A contact must have an email or a postal address" to a three-case union (`EmailOnly | PostOnly | EmailAndPost`) and observes "Once it is put like this, the solution becomes obvious – use a union type with a case for each possibility."

## Reasons given
- King: validators discard what they learned, so every later function must re-check or trust; parsers return the stronger type. Shotgun parsing mixes checking with processing and deprives "the program of the ability to reject invalid input instead of processing it" (quoting Sassaman et al.).
- Noonan: avoids both run-time failure and use-site checks; zero run-time overhead.
- Minsky/Wlaschin: the type system rejects invalid combinations, and the compiler flags every place to update when states change (Wlaschin; the Minsky post gives no prose).

## What transfers to general-purpose Lean
- Direct fit: sum types per state, `Option` fields replaced by variant-specific structures, `Subtype`/`NonEmpty`-style arguments (`{xs : List α // xs ≠ []}`, `Vector α n`, `Fin n`), parsing at the boundary into a refined type.
- Lean can do what King calls "impractical in Haskell" (ranges, lengths) with subtypes or indexed families; the question for a guide is when that is worth the proof obligations at call sites. King's "use best judgement" bullet and "single `error "impossible"` is not worth it" is the closest explicit guidance found.
- Noonan's technique (proofs in phantom types) is largely unnecessary in Lean, where proofs are first-class and erased; the API-design insight that matters is "let the caller choose how to discharge the precondition" (a hypothesis argument `(h : xs ≠ [])` vs an `Option` return vs a `!` panic variant). Lean core's `naming.md` already prescribes `?`/`!` variants for the last two.
- Strengthen-the-argument vs weaken-the-result is a direct framing for the Lean `getElem` family (`xs[i]` with proof, `xs[i]?`, `xs[i]!`); not discussed in these sources.

## Caveats and unverified items
- Minsky's slogan page is a 2011 follow-up to a talk; the talk (video) and the original "Effective ML" (2010) were not read.
- Noonan's PDF was read through the abstract and a few sections (text extract), not in full.
- Wlaschin's post is about F# records and unions; no formal-methods content.
- Other well-cited candidates not fetched (**unverified leads**): Wlaschin, *Domain Modeling Made Functional* (book); Harper, "Boolean blindness"; Hoare, "null references".
