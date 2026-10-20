# Lean 4 (Meta)programming Cookbook (recipes)

| Field | Value |
|---|---|
| URL | https://leanprover-cookbook.github.io/lean-metaprogramming-recipes/ (source: https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/tree/18c12de7a681c856a96e4a594fec6d39d952f7f3) |
| Author / org | leanprover-cookbook. Top contributors by commits: AnirudhG07 40, Siddhartha Gadgil 23, ajay-k-nair 13, David Thrane Christiansen 2 (GitHub, 2026-10-20) |
| Date / version | `18c12de` (2026-04-22); repo created 2026-03-02; 19★ |
| License | MIT (`LICENSE`, "Copyright (c) 2026 leanprover-cookbook") |
| Scope & audience | Lean users looking for task-oriented recipes in programming and metaprogramming |
| Kind | community advice (young, low authority) |
| Lean version | Lean 4 |
| Raw copy | source clone `vendor/repos/mprecipes` |

## Summary
A Verso-built cookbook. Despite the name, about half of it is ordinary programming: IO, CLI arguments, tasks, the file system, JSON, state. It has almost nothing on macro style; it says only that `syntax` and `macro_rules` can be split "if you prefer". Its value to this project is that it touches application topics no other Lean source covers. It is young, had its last commit in April 2026 and is mostly the work of two people, so treat each claim as a pointer to check against the Reference or the Std source.

## Rules
Base: `https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/`.

- CLI: taking `main (args : List String)` and pattern matching on the list is "the most common and idiomatic way" to read arguments for simple tools ([IO/CliArgs.lean L29, L42](https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/IO/CliArgs.lean#L29)).
- Exit codes: `IO.Process.exit`, with 0 for success "by convention" ([IO/Miscellaneous.lean L48](https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/IO/Miscellaneous.lean#L48)).
- Tasks:
  - use `IO.asTask` for tasks with side effects ([IO/SpawningTasks.lean L53](https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/IO/SpawningTasks.lean#L53));
  - "Deadlocking the Task System" explains how spawning many tasks that block on each other can exhaust the worker threads ([IO/Miscellaneous.lean L132ff](https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/IO/Miscellaneous.lean#L132)).
- Timing: use the monotonic clock for benchmarks ([IO/TimePerformanceMeasure.lean L31](https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/IO/TimePerformanceMeasure.lean#L31)).
- JSON: "The most idiomatic way to handle JSON in Lean is by defining a structure and deriving a `Lean.ToJson` instance" ([DataStructures/JSON/JsonObject.lean L56](https://github.com/leanprover-cookbook/lean-metaprogramming-recipes/blob/18c12de7a681c856a96e4a594fec6d39d952f7f3/Cookbook/DataStructures/JSON/JsonObject.lean#L56)).

## Reasons given
Mostly none beyond "idiomatic" or "by convention". The deadlock section explains the mechanism with an analogy of chefs in a kitchen.

## What transfers to general-purpose Lean
- Topics for the application chapters (CLI, tasks, timing, JSON, exit codes), each to be checked against the Reference's IO and Async chapters before it becomes a rule ([lean-reference](lean-reference.md#concurrency-read-2026-10-20)).
- The JSON claim agrees with the author survey: `ToJson`/`FromJson` are among the most derived classes in FRO code that talks to the outside world ([author-survey](../author-survey.md)).
- Nothing for the macros chapter.

## Caveats and unverified items
- Only the advice-word lines were read, and no recipe was run.
- Recipe quality varies, and the site's own guidelines say recipes are not meant to replace TPIL, MIL or FPIL.
