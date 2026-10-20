# When (not) to prove: proof-engineering literature and practitioner cost/benefit

Combined note: Ringer et al., *QED at Large* (survey), Newcombe et al. (AWS, 2014), plus what the other notes in this track say about restraint.

| Field | Value |
|---|---|
| URL | (1) https://arxiv.org/abs/2003.06458 (DOI 10.1561/2500000045) (2) https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf |
| Author / org | (1) Talia Ringer, Karl Palmskog, Ilya Sergey, Milos Gligoric, Zachary Tatlock (2) Chris Newcombe, Tim Rath, Fan Zhang, Bogdan Munteanu, Marc Brooker, Michael Deardeuff (Amazon) |
| Date / version | (1) arXiv v1, 2020-03-13; version of record in Foundations and Trends in Programming Languages (2) 2014-09-29 |
| License | (1) arXiv non-exclusive distribution licence (https://arxiv.org/licenses/nonexclusive-distrib/1.0/, linked from the abstract page) (2) none stated on the PDF (Amazon-authored, hosted on Lamport's site) |
| Scope & audience | (1) proof-engineering researchers and practitioners (2) industry engineers |
| Kind | descriptive (both) |
| Lean version | n/a (surveys Coq, Isabelle, Lean 3 era systems; the survey predates Lean 4) |
| Raw copy | `vendor/pages/proof-assistants/qed-at-large.pdf` / `.txt`, `aws-fm.pdf` / `.txt` |

## Summary
No source found gives a rule for "when not to prove". The survey is about how to make proofs maintainable and what is known about cost; it reports brittleness, scale and cost estimation results and says design principles from software engineering carry over. The AWS paper argues from experience that formal specification and model checking (not proof) paid off on large real systems, and rejects the view that cost limits formal methods to safety-critical software. Both are descriptive and neither is Lean-specific. What follows is limited to quotable statements.

## Claims
**Brittleness** (QED at Large, section 6.2, "Design Principles for Robustness"):
> A major source of inefficiency in verification is proof brittleness: Even a minor change to a single theorem or definition can break many dependent proofs. This makes proofs difficult to maintain [...] Design principles help make proofs robust in the face of changes.
([arXiv PDF](https://arxiv.org/pdf/2003.06458), text extract L2940-L2950)

**Automation and robustness** (same section):
> CPDT [...] advocates for the heavy use of program-specific automation, noting that this makes proofs more robust [...] This style of development localizes the burden of change to the automation itself as opposed to the many proofs that use the automation.
> While automation can make proofs more robust, it can also be brittle in itself. For example, some Coq tactics automatically generate hypothesis names; small changes in specifications can cause proofs that rely on those names to break.
([text L2960-L2975](https://arxiv.org/pdf/2003.06458))

**Cost estimation** (section 7.3, secondary reporting of seL4 studies):
> Staples et al. (2014) study the proof productivity problem in the context of seL4; they find that effort is correlated linearly with proof size. Matichuk et al. (2015a) [...] find a quadratic relationship between the size of a formal property and the proof script required to prove it.
> Bourke et al. (2012) [...] highlight three lessons: (1) proof automation is crucial, (2) using introspective tools for quickly finding facts in large databases gain importance for productivity, and (3) tools that shorten the edit-check cycle increase productivity, even when sacrificing soundness.
([text L4532-L4556](https://arxiv.org/pdf/2003.06458))

Also: Andronick et al. (2012) "conclude that formal verification, and re-verification, for systems requiring in the order of 10,000 LOC is feasible using a proof assistant" (same section).

**Industry view of cost** (AWS):
> In industry, formal methods have a reputation of requiring a huge amount of training and effort to verify a tiny piece of relatively straightforward code, so the return on investment is only justified in safety-critical domains such as medical systems and avionics. Our experience with TLA+ has shown that perception to be quite wrong. [...] In every case TLA+ has added significant value, either finding subtle bugs that we are sure we would not have found by other means, or giving us enough understanding and confidence to make aggressive performance optimizations without sacrificing correctness.
([PDF, "The Value of Formal Methods for 'Real-world Systems'"](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf))

The paper's own caution: engineers "initially avoid the words 'formal', 'verification', and 'proof'" because of the widespread view of low return (PDF text L325); and that "conventional informal proofs can miss very subtle" bugs (L289-L290). Scope: specifications of distributed designs checked exhaustively with TLC, not code-level proofs.

**Related, from other notes in this track** (see each for links):
- Brady: types "rarely eliminate" the need for tests (`tdd-idris-brady.md`).
- King: "It probably isn't worth breaking out singletons and refactoring your entire application just to get rid of a single `error "impossible"` call"; document the invariant in a comment (`correct-by-construction.md`).
- Idris 2 docs: `partial` "is not advisable [...] only [...] during the initial development of a function, or during debugging" (`idris2-docs.md`).
- Lean core: "Prefer highly automated tactics (like `grind` and `omega`) over low-level proofs" and "Do not over-golf proofs" (`vendor/repos/lean4/doc/std/style.md` L449-L465; read for context, not a note of this track).

## Reasons given
- Robustness: dependency of proofs on definitions and on generated names; automation localises change.
- Cost: effort tracks proof size, proof size tracks property size (in seL4 data), so statement choice drives cost.
- Value: model checking found bugs "we are sure we would not have found by other means".

## What transfers to general-purpose Lean
- Treat statements as the cost driver: a guide could ask for small, local invariants rather than whole-program specs, citing the seL4 size/effort findings (they are about Isabelle, Staples/Matichuk are secondary here).
- Brittleness advice (avoid dependence on auto-generated names, prefer automation that localises change) is in Lean core `style.md` already; the survey is the external justification.
- No source here supports a firm "do not prove X" rule; candidate framing is "prove what is cheap to state and stable, test the rest".

## Caveats and unverified items
- The survey is large (about 380 KB of text); only sections 6.2 and 7.3 and keyword hits were read. Chapter 3-4 material on specifications ("trusting the spec") was not read.
- Line references (L...) are to my text extract, which is not versioned; use section names to find them.
- Unverified leads: Staples et al. 2015 ICSE "Empirical study towards a leading indicator for cost of formal software verification"; Klein et al. seL4 reports; Hillel Wayne's essays on formal methods adoption; Lean-community discussions of verification cost.
