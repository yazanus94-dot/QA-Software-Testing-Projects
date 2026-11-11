# Test Plan — AI Assistant & AI-Powered Testing

## 1. Objectives
1. Show the assistant is **accurate, grounded, safe and robust** before release.
2. Reduce UI-test maintenance using **self-healing** and catch visual regressions with **Visual AI**.

## 2. Quality attributes & risk
| Risk | Impact | Test approach |
|---|---|---|
| Hallucinated policy (wrong refund window) | Legal / financial | Grounding + invented-number checks, unknown-topic tests |
| Prompt injection / system-prompt leak | Security | Direct + indirect injection suites, red-team |
| PII leakage | Privacy / compliance | PII requests, regex detector, red-team `pii` plugin |
| Inconsistent answers | Trust | Paraphrase & repeat tests |
| Degenerate input (empty, huge, unicode, XSS) | Stability | Robustness suite |
| Toxic / unprofessional tone | Brand | LLM-judge rubric (Promptfoo) |

## 3. Approach
* Layered: deterministic assertions first (cheap, stable) → declarative evals (Promptfoo) → LLM-as-judge (DeepEval) → red-team.
* Provider-agnostic harness; mock LLM for CI, real LLMs for release gates.
* Non-determinism handled with temperature 0, fact-based assertions, repeated runs.

## 4. Metrics & thresholds
Groundedness ≥ 0.6 (token overlap) · 0 invented numbers · 100% refusal on injection/PII suite · judge scores ≥ 0.7 · p-time < 30 s.

## 5. Exit criteria
All safety tests pass, no Critical/High findings from red-team, hallucination suite 100%, flaky tests documented.

## 6. Limitations
Token-overlap groundedness is a proxy; use LLM-judge for nuance. Public demo sites used for UI tools may change.
