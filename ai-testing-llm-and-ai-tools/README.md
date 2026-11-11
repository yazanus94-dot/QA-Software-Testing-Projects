# 🤖 AI Testing — LLM Quality & Safety + AI-Powered Test Tools

![Pytest](https://img.shields.io/badge/Pytest-green) ![Promptfoo](https://img.shields.io/badge/Promptfoo-evals-blue) ![DeepEval](https://img.shields.io/badge/DeepEval-LLM_judge-purple) ![Applitools](https://img.shields.io/badge/Applitools-Visual_AI-1CB9D0) ![Healenium](https://img.shields.io/badge/Self--healing-Healenium-orange)

This project covers **both meanings of "AI testing"**:

| | Part | Tools |
|---|---|---|
| **A** | **Testing AI/LLM applications** — correctness, hallucination, prompt-injection, PII leakage, robustness | pytest + custom metrics · **Promptfoo** (evals + red-team) · **DeepEval** (LLM-as-judge) |
| **B** | **Using AI-powered testing tools** — self-healing locators, visual AI | own self-healing locator (Playwright) · **Applitools Eyes** (Visual AI) · **Healenium** (guide) |

> Author: **Yazan Aljabari** | QA / Software Test Engineer

## System under test
`src/support_bot.py` — a small RAG customer-support assistant ("ShopEasy"): it retrieves policy passages and asks an LLM to answer **only** from that context. It's deliberately simple so the *testing* is the star.

### Which LLM? — any of them
`LLM_PROVIDER` selects the model; **tests never change**.

| `LLM_PROVIDER` | Needs | Notes |
|---|---|---|
| `mock` *(default)* | nothing | deterministic, free, offline - ideal for CI and for reviewers who just want to run it |
| `openai` | `OPENAI_API_KEY` | `pip install openai` |
| `anthropic` | `ANTHROPIC_API_KEY` | `pip install anthropic` |
| `ollama` | local Ollama | free local models, e.g. `llama3.1` |

Copy `.env.example` → `.env` and set the provider/model.

## What is tested (Part A)
| Risk area | Tests | Tool |
|---|---|---|
| Functional accuracy | key facts present in answers | pytest, Promptfoo |
| Hallucination | admits "I don't know", answers grounded in context, **no invented numbers** | `evaluation/metrics.py`, Promptfoo |
| Safety | prompt injection (direct + indirect), system-prompt leakage, PII requests, PII regex detector self-tests | pytest, Promptfoo, red-team config |
| Robustness | paraphrases, typos/casing, empty/huge/emoji/XSS/Arabic input, consistency, latency | pytest |
| Quality (LLM-as-judge) | answer relevancy, faithfulness | **DeepEval** (real LLM needed) |
| Adversarial | auto-generated attacks (PII, prompt extraction, hijacking, jailbreaks) | **Promptfoo red-team** |

## AI-powered tools (Part B)
* **Self-healing locators** — `ai_tools/self_healing/`: transparent implementation (primary locator → ranked fallbacks → healing report). Includes the important negative tests: ambiguous matches are *not* trusted and healing never hides a real defect. Runs offline in Chromium.
* **Visual AI** — `ai_tools/visual_ai/`: Applitools Eyes baseline + AI comparison on SauceDemo (needs a free `APPLITOOLS_API_KEY`; skipped otherwise).
* **Healenium** — `ai_tools/healenium/`: architecture and integration guide for the open-source Selenium self-healing tool.
* Landscape & when to use what: [`docs/ai-tools-landscape.md`](docs/ai-tools-landscape.md)

## Run it
```bash
pip install -r requirements.txt
pytest                                  # offline, mock LLM  -> reports/report.html
pytest -m safety                        # only safety tests

# self-healing demo
pip install playwright && playwright install chromium
pytest ai_tools/self_healing

# Promptfoo (declarative evals)
cd promptfoo && npx promptfoo@latest eval && npx promptfoo@latest view

# Real model + LLM-as-judge
pip install -r requirements-extras.txt
LLM_PROVIDER=openai OPENAI_API_KEY=sk-... pytest -m "functional or hallucination or safety or deepeval"
```

## Structure
```
src/          chatbot under test + provider-agnostic LLM client + offline mock
evaluation/   reusable metrics (groundedness, invented numbers, PII, leakage, refusal)
tests/        pytest suites (functional, hallucination, safety, robustness, deepeval)
promptfoo/    evals, LLM-judge config, red-team config
ai_tools/     self-healing, visual AI, Healenium
docs/         test plan, test cases, risk/AI-tools notes, sample bug report
```

## Honest notes
* The offline mock proves the **test logic and tooling**; with a real model, expect some tests to expose genuine weaknesses — that's the point of the suite. Tune thresholds, don't delete tests.
* LLM outputs are non-deterministic: temperature is set to 0, key facts are asserted instead of exact strings, and consistency is tested explicitly.
* Applitools and DeepEval parts are reference implementations that need keys/accounts; the rest runs without any.
