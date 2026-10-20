# The Clojure Style Guide (bbatsov) - format model

| Field | Value |
|---|---|
| URL | https://guide.clojure.style/ (rendered); source https://github.com/bbatsov/clojure-style-guide |
| Author / org | Bozhidar Batsov (primary editor) with an editor team: Alex Miller, Daniel Compton, Sean Corfield ([Editor Team](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L3689)) |
| Date / version | `2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a`, 2026-09-17 (single-commit shallow clone; history not inspected). Started 2013 ([History](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L3660)). |
| License | **CC BY 3.0 Unported** ([License section](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L3738)). Attribution; adaptation allowed. |
| Scope & audience | Clojure programmers; "real-world Clojure programmers can write code that can be maintained by other real-world Clojure programmers" |
| Kind | community advice |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/bbatsov-clojure.adoc` |

## Summary
The model for the Lean guide's format. Single AsciiDoc file (~3,750 lines, 162 rule-level headings), converted from Markdown in 2019. Opens with a principle (code is read more than written), a consistency note borrowed from PEP 8, and an explicit statement that where the community has no consensus, "all popular styles are acknowledged and it's up to you to pick one". Rules are short, anchored and illustrated with `;; good` / `;; bad` code. Ends with an "Existential" section of three one-line meta-rules.

## Structure (top-level table of contents)
Introduction (Guiding Principles, A Note About Consistency, Translations); Source Code Layout & Organization; Namespace Declaration; Naming; Functions; Idioms; Data Structures; Types & Records; Mutation; Math; Strings; Exceptions; Macros; Common Metadata; Comments; Documentation; Testing; Library Organization; Existential; Tools; History; Sources of Inspiration; Editor Team; Contributing; Colophon; License; Spread the Word. (`grep '^== '` of the source; Layout begins at [L146](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L146).)

## How a rule is written
- Heading = short title; anchor in double brackets `[[kebab-id]]` (e.g. `=== Predicate Methods [[naming-predicates]]`), giving a stable URL fragment. Some headings lack an explicit anchor (auto-generated).
- Body = one or two imperative sentences, then optionally a rationale sentence, then a `[source,clojure]` block with `;; good` / `;; bad` (sometimes `;; not so good`, `;; okish`) comment labels.
- Admonition blocks: `NOTE:`, `TIP:`; discussion sidebars in `****` blocks (e.g. ".Why Bother with 80 characters in a World of Modern Widescreen Displays?" under [Maximum Line Length](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L156-L188)).
- Rules are plain imperatives with no severity labels; strength is carried by wording: "Avoid", "Prefer", "Use", "Consider".
Sample ([Predicate Methods](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L977-L991)):
> The names of predicate methods (methods that return a boolean value) should end in a question mark (e.g., `even?`).
Sample with a threshold ([Function Length](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L1263-L1267)):
> Avoid functions longer than 10 LOC (lines of code). Ideally, most functions will be shorter than 5 LOC. Short functions are easier to understand, test, and compose.

## Intro, principles and disagreement
Intro ([L12-L40](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L12-L40)):
> A style guide that reflects real-world usage gets used, and a style guide that holds to an ideal that has been rejected by the people it is supposed to help risks not getting used at all -- no matter how good it is.
> We've tried to add the rationale behind the rules (if it's omitted, we've assumed that it's pretty obvious).
> Nothing written here is set in stone. This style guide evolves over time as additional conventions are identified and past conventions are rendered obsolete by changes in Clojure itself.
Guiding principles ([L75-L103](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L75-L103)):
> Programs must be written for people to read, and only incidentally for machines to execute. (quote from SICP)
> When we had to choose between a very established practice and a subjectively better alternative we've opted to recommend the established practice.
> There are some areas in which there is no clear consensus in the Clojure community regarding a particular style (like semantic indentation vs fixed indentation, semantic comments vs uniform comments, etc). In such scenarios all popular styles are acknowledged and it's up to you to pick one and apply it consistently.
Consistency ([L104-L127](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L104-L127)):
> Consistency with this style guide is important. Consistency within a project is more important. Consistency within one class or method is the most important.
> In particular: do not break backwards compatibility just to comply with this guide!
plus four listed good reasons to ignore a guideline (readability for people used to the style, consistency with surrounding code, predates the guideline, compatibility with older versions).
Handling disagreement inside rules: fixed-vs-semantic indentation is presented as the recommended style, then "Some people in the Clojure community have argued that's not worth it ... Here are a few examples" with alternatives shown ([L310-L322](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L310-L322)); the Ruby guide does the same.
Existential ([L3609-L3620](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L3609-L3620)): "Be Functional", "Be Consistent", "Use common sense."

## Contribution and license setup
- Contributing ([L3700-L3730](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L3700-L3730)): "Nothing written in this guide is set in stone"; fork, feature branch, PR; "some guidelines are lacking examples"; sponsorship links; separate `CONTRIBUTING.md` ([file](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/CONTRIBUTING.md)) covers issue reporting and PR hygiene (descriptive title, one subject per PR).
- Governance: editor team named in the guide; sources of inspiration listed (Elements of Style, PEP 8, Ruby guide, Google Common Lisp guide, books).
- License: CC BY 3.0 at the bottom; no CLA.
- Tooling and translations: README says a nicer rendered version exists with better navigation; translation list present.
- Colophon states AsciiDoc and AsciiDoctor, hosted on GitHub Pages ([L3731](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L3731)).

## Rules that transfer to Lean (selected, verbatim)
- Naming, predicates: "should end in a question mark" (Lean: `is` prefix / `Bool`-valued vs `Prop`; compare Ruby which forbids `is_`).
- [Unsafe Functions](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L993-L1009): "The names of functions/macros that are not safe in STM transactions should end with an exclamation mark (e.g. `reset!`)." (side-effect marker; compare Lean `!` = panics).
- [Conversion Functions](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L1011-L1022): "Use `->` instead of `to` in the names of conversion functions." (`f->c`).
- [Idiomatic Names](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L1098-L1125): table of conventional local names (`f g h`, `n`, `xs`, `m`, `k`, `coll`, `pred`...). A model for Lean's `a b c : α`, `xs`, `h` for hypotheses.
- [Function positional parameters limit](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L1269-L1284): "Avoid parameter lists with more than three or four positional parameters... Prefer a map of options instead." (Lean: structure of options).
- [Pre and Post Conditions](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L1286-L1302): prefer `:pre`/`:post` to body checks (Lean analogue: hypotheses/subtypes).
- Exceptions: [Reuse Existing Exception Types](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L2431-L2455), [Prefer with-open over finally](https://github.com/bbatsov/clojure-style-guide/blob/2bc3d2c5d940ab87326860fe68e9fcd849cbeb0a/README.adoc#L2452-L2470).
- Sections on Documentation, Testing, Library Organization (coordinates) exist and are a ready topic list for a general-purpose Lean guide.

## Reasons given
Mostly one-liners ("Short functions are easier to understand, test, and compose"); long rationales only for contested rules (line length). The introduction promises rationale except where "obvious", which in practice means many rules have none.

## What transfers to general-purpose Lean
- Everything under "How a rule is written", "Intro", "Consistency" and "Contribution/license setup" is the format template (the lead has already chosen this guide as the model).
- Anchors with stable ids: rules can be cited in reviews and linters.
- Unusual among style guides: dated-by-version statements ("changes in Clojure itself") and a clause about not breaking backward compatibility just to comply.

## Caveats and unverified items
- Several rules (e.g. Function Length "10 LOC") are stated without sources; not all rules are consensus; this repo checkout is shallow so edit history/dates per rule are **unverified**.
- Line ranges are from the checked-out file at the SHA above.
