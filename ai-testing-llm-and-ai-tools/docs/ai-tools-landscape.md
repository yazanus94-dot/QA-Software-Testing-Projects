# AI in Testing — Tool Landscape (what I used and why)

| Need | Tool used here | Alternatives | Notes |
|---|---|---|---|
| Declarative LLM evals & red-teaming | **Promptfoo** | Garak, PyRIT | YAML-driven, great for CI |
| LLM-as-judge metrics for RAG | **DeepEval** | Ragas, TruLens | pytest-native |
| Visual regression with AI | **Applitools Eyes** | Percy, Chromatic | ignores rendering noise, flags meaningful changes |
| Self-healing locators | own implementation + **Healenium** | Testim, mabl, Katalon, Functionize | commercial tools add ML-based element fingerprints |
| AI-assisted authoring | LLM assistants for test ideas/data | Copilot, Claude | always review generated tests |

## Guidelines I follow
1. Deterministic checks first; use LLM judges only for what rules cannot express.
2. Every healed locator or auto-approved visual diff is **reviewed by a human**.
3. Version prompts, datasets and thresholds like code.
4. Track pass rate **per risk category**, not only an overall percentage.
