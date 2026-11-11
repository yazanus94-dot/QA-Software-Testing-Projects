# Test Plan — SauceDemo Web Shop

## Objective
Provide fast, reliable regression coverage of the customer purchase journey on every pull request.

## Scope
**In:** authentication, product listing & sorting, cart, checkout, basic accessibility, visual stability of the login page.
**Out:** payment integrations, back-office, load and security testing.

## Strategy
* Risk-based: login and checkout are tagged `@smoke` and run on every PR.
* Full regression (all browsers + mobile viewport) nightly.
* Page Object Model + fixtures keep tests short and maintainable.
* Independent tests, no shared state, parallel execution.

## Test data
Public demo users (`standard_user`, `locked_out_user`, ...). Data is centralised in `test-data/`.

## Environments & browsers
Chromium, Firefox, WebKit (desktop), Pixel 7 emulation. Base URL configurable via `BASE_URL`.

## Entry / exit criteria
Entry: environment reachable. Exit: all `@smoke` pass, regression ≥ 98%, flaky tests quarantined with a ticket.

## Reporting
Playwright HTML report, JUnit XML, traces/videos on failure, artifacts stored 14 days in CI.

## Risks
Third-party demo site may change or be slow → retries in CI (2), traces to diagnose.
