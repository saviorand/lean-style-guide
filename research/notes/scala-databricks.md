# Databricks Scala Guide

| Field | Value |
|---|---|
| URL | https://github.com/databricks/scala-style-guide |
| Author / org | Databricks (individual authors not named in the README) |
| Date / version | `7cc731d0df944ce2de1b67acd0faf9c7b6bc4166`, last commit 2022-08-05; document history from 2015-03-16 |
| License | **CC BY-NC-SA 4.0** (README header). Non-commercial and share-alike: do not copy text into a permissively licensed guide; paraphrase only. |
| Scope & audience | Databricks engineers, Apache Spark/Delta contributors |
| Kind | normative (company standard), community-influential |
| Lean version | n/a |
| Raw copy | `vendor/pages/other-langs/scala-databricks.md` |

## Summary
A rule list with a strong preference for simple code: "Code is written once by its author, but read and modified multiple times by lots of other engineers." Sections: syntactic style, language features (what to avoid), exception handling, concurrency, performance, Java interop, testing, misc. It is blunt: it bans `Try` in APIs, symbolic method names, `return` in closures, and discourages monadic chains. It also has a changelog in which it **downgraded the severity of some rules from "do NOT" to "avoid"** (2015-08-23).

## Rules
Intro ([README](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L1-L8)):
> we need to optimize our codebase for long-term, global readability and maintainability. The best way to achieve this is to write simple code.

Selected rules (section links are anchors in the README):
- [Rule of 30](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L166-L174): "A method should contain less than 30 lines of code. A class should contain less than 30 methods."
- [Line length](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L160-L164): "Limit lines to 100 characters."
- [Symbolic methods](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L633-L645): "__Do NOT use symbolic method names__, unless you are defining them for natural arithmetic operations (e.g. `+`, `-`, `*`, `/`)." Example: `channel ! msg` vs `channel.send(msg)`.
- [Type inference](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L647-L654): "__Public methods should be explicitly typed__ ... A good litmus test is that explicit types should be used if a code reviewer cannot determine the type in 3 seconds."
- [Exception handling](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L755-L795): "Do NOT use `Try` in APIs, that is, do NOT return Try in any methods. Instead, prefer explicitly throwing exceptions for abnormal execution and Java style try/catch for exception handling." Background: "the use of it often leads to more levels of nesting that are harder to read. In addition, it is often unclear what the semantics are for expected errors vs exceptional cases." Its example prefers `def get(userId: Int): Option[User]` documented with `@throws` for connection errors, and says "The 2nd one makes it very obvious error cases the caller needs to handle."
- [Options](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L796-L810): "Use `Option` when the value can be empty." "Do not use None to represent exceptions. Instead, throw exceptions explicitly." "Do not call `get` directly on an `Option`, unless you know absolutely for sure the `Option` has some value."
- [Monadic chaining](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L811-L867): "Avoid chaining (and/or nesting) more than 3 operations." "If it takes more than 5 seconds to figure out what the logic is, try hard to think about how you can express the same functionality without using monadic chaining."
- [Case classes](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L520-L542): "Constructor parameters should NOT be mutable for case classes. Instead, use copy constructor."
- [Prefer well-tested methods](https://github.com/databricks/scala-style-guide/blob/7cc731d0df944ce2de1b67acd0faf9c7b6bc4166/README.md#L1226-L1240): reimplementing library methods "may introduce bugs and requires spending time testing it".
- Also: variable naming, ordering within a class, imports, pattern matching, implicits, recursion/tail recursion, `override` modifier, Java interop, testing exceptions.

## Reasons given
Frequent short rationales, often with a concrete failure mode (mutable case class in a hash map, `return` compiled to a thrown exception). The document history documents softening of rule strength: counterexample to "rules never change".

## What transfers to general-purpose Lean
- Numeric thresholds as heuristics (30 lines per method, 3-4 chain depth, 3-second type test) are a model of testable "smell" rules; also Clojure's "10 LOC" function length.
- "No symbolic operators except natural arithmetic": direct parallel to restraint in Lean `notation`/`infix`.
- Error handling split: exceptions for abnormal, `Option` for expected absence, documented with `@throws`; strongly contradicts the Effective Scala / Rust stance on typed errors. Good for the "Result vs exceptions" open question.
- Explicit types on public definitions.
- Rule strength levels with a changelog.

## Caveats and unverified items
- Last substantive update 2022; Scala 2 specifics (implicits, `Symbol` literals). NC licence limits reuse.
