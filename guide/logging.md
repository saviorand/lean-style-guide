# Logging

Part of [A Lean Style Guide for Software](../README.md), a community draft. Every example compiles with Lean 4.35.0.

<a name="logging-decisions"></a>
## Decisions

Log where the code makes a decision that its result can't express. An empty list or a bare 403 doesn't say which of several causes produced it, so whoever investigates later depends on the log to find out.

*Source: [Paul Butcher, issue #1][issue-1].*

<a name="logging-values"></a>
## The deciding value

Record the value that decided the branch, not just the outcome: "refused, scopes held: []" rather than "refused". The examples write to standard error with `IO.eprintln`; use whatever logger your application has.

```lean
-- bad
def authorize (scopes : List String) : IO Bool := do
  if scopes.contains "admin" then return true
  IO.eprintln "refused"
  return false
```

```lean
-- good
def authorize (scopes : List String) : IO Bool := do
  if scopes.contains "admin" then return true
  IO.eprintln s!"refused, scopes held: {scopes}"
  return false
```

*Source: [Paul Butcher, issue #1][issue-1].*

<a name="logging-requests"></a>
## What was asked for

Log what was asked for. A tracing span records the route that handled a request, such as `/search`, but not the query or the parameters that decided the result.

*Source: [Paul Butcher, issue #1][issue-1].*

<a name="logging-success"></a>
## Ordinary success

Don't log ordinary success when a span already records the request. The entry repeats the span and buries the entries that explain decisions.

*Source: [Paul Butcher, issue #1][issue-1].*

---

Previous: [Error handling](errors.md) · [Contents](../README.md#rules) · Next: [API design and visibility](api.md)

[issue-1]: https://github.com/saviorand/lean-style-guide/issues/1
