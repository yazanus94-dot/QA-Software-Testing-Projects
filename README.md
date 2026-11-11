# QA Software Testing Projects Portfolio

[![QA Tests](https://github.com/yazanus94-dot/QA-Software-Testing-Projects/actions/workflows/qa.yml/badge.svg)](https://github.com/yazanus94-dot/QA-Software-Testing-Projects/actions/workflows/qa.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue) ![Node 20](https://img.shields.io/badge/node-20-brightgreen) ![License](https://img.shields.io/badge/license-MIT-green)

Hands-on QA engineering across **five disciplines**, each an independent project
with its own framework, docs (test plan / test cases / bug report) and CI:
web E2E, API, mobile, performance, and AI/LLM quality & safety.

| # | Project | Stack | What it proves |
|---|---------|-------|----------------|
| 1 | [playwright-automation](playwright-automation/) | **Playwright + TypeScript** | Page Object Model + custom fixtures, data-driven logins, network interception (`page.route`), axe-core a11y audit, visual regression, trace/video-on-failure; matrix over Chromium/Firefox/WebKit + mobile viewports |
| 2 | [api-testing-postman](api-testing-postman/) | **Postman/Newman + pytest + SQLite** | Four testing layers: functional collections (chained requests, JSON schema, auth negatives), CSV data-driven runs, API→DB integrity checks, and an API→UI hybrid test |
| 3 | [mobile-testing-appium](mobile-testing-appium/) | **Appium 2 + UiAutomator2 (Android)** | POM with explicit waits (no sleeps), data-driven + negative login, mobile gestures/orientation/lifecycle tests, auto failure screenshots, runs on an Android emulator in CI |
| 4 | [performance-testing-pytest-k6](performance-testing-pytest-k6/) | **k6 + pytest** | Explicit SLO budgets: smoke/load/stress/spike k6 profiles + pytest latency budget gates (p95/p99, error rate) asserting real-world targets |
| 5 | [ai-testing-llm-and-ai-tools](ai-testing-llm-and-ai-tools/) | **pytest + Promptfoo + DeepEval** | Tests an LLM app for correctness, hallucination/grounding, prompt injection, PII leakage, robustness (46 offline tests on a deterministic mock LLM) + Promptfoo evals & red-team configs, and AI-powered tooling (self-healing locators, Visual AI) |

## How the suite runs in CI

Eight jobs on every push (`.github/workflows/qa.yml`):

| Job | Target | Notes |
|-----|--------|-------|
| Playwright E2E | live [SauceDemo](https://www.saucedemo.com) | Chromium (full 3-browser + visual matrix is available per-project via config) |
| Newman functional + data-driven | live [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) | chained requests, CSV-driven, htmlextra reports as artifacts |
| API→DB integrity | Restful-Booker + SQLite | `pytest -m db` — API responses must match persisted data |
| Appium suite validation | local | imports + collection of all 13 mobile tests (emulator smoke runs on manual dispatch) |
| pytest performance budgets | live [k6 demo API](https://test-api.k6.io) | latency SLOs asserted in the normal test run |
| k6 smoke gate | k6 demo API | smoke profile as a merge gate |
| AI/LLM offline suite | built-in mock LLM | 46 tests: hallucination, injection, PII, robustness, consistency |
| Promptfoo eval + red-team | mock provider | LLM-judge configs run headlessly, results as artifacts |

The AI project also has a **manual `live-llm` mode**: same tests, `LLM_PROVIDER=openai`
with a repository secret — showing the suite doesn't change when the model does.

## Quick start

```bash
# 1. Web E2E (TypeScript)
cd playwright-automation && npm install && npx playwright install chromium && npm test

# 2. API testing
cd api-testing-postman && npm install && npm run test:api   # Newman collections
python -m pytest -m db                                      # API->DB integrity

# 3. Mobile (needs an Android emulator + Appium)
cd mobile-testing-appium && pip install -r requirements.txt && python -m pytest -m smoke

# 4. Performance
cd performance-testing-pytest-k6 && pip install -r requirements.txt && python -m pytest
k6 run k6/smoke.js                                          # (with the k6 CLI installed)

# 5. AI/LLM testing (offline, no API keys needed)
cd ai-testing-llm-and-ai-tools && pip install -r requirements.txt && python -m pytest
```

## Project demonstration

Watch the video demonstration to see the testing projects, implementation, and execution results.

**Video:** https://github.com/user-attachments/assets/d3561295-e508-4403-9d84-ab3464b93379

## References & learning resources

Official documentation and industry resources used as technical references.

| Tool / Standard | Official Reference |
|---|---|
| Playwright | https://playwright.dev/docs/intro |
| Postman | https://learning.postman.com/docs/ |
| Appium | https://appium.io/docs/en/latest/ |
| Python pytest | https://docs.pytest.org/en/stable/ |
| Grafana k6 | https://grafana.com/docs/k6/latest/ |
| OWASP GenAI / LLM Security | https://genai.owasp.org/llm-top-10/ |
| NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework |

## Scope

Portfolio projects by Yazan Aljabari. Live third-party demo sites are used as test
targets per their terms; no vendor or client data.

## License

MIT, see [LICENSE](LICENSE).
