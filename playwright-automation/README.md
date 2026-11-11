# 🎭 Playwright Automation — TypeScript, Page Object Model, CI

![Playwright](https://img.shields.io/badge/Playwright-1.48-2EAD33) ![TypeScript](https://img.shields.io/badge/TypeScript-5-blue) ![CI](https://img.shields.io/badge/GitHub_Actions-ready-black)

End-to-end UI automation framework for the public **[SauceDemo](https://www.saucedemo.com)** shop.
Cross-browser (Chromium, Firefox, WebKit + mobile viewport), parallel, with traces, video, screenshots,
accessibility scanning and visual regression.

> Author: **Yazan Aljabari** | QA / Software Test Engineer

## Highlights
* **Page Object Model** + custom **fixtures** (`loggedIn` gives a ready authenticated session)
* **Data-driven** negative login tests, sorting verification, full purchase E2E flow
* **Network control** with `page.route`, console-error guard
* **Accessibility** audit with axe-core, **visual regression** with `toHaveScreenshot`
* Stable locators (`getByTestId`, `getByRole`) — no XPath, no hard waits
* Trace-on-retry, video-on-failure, HTML + JUnit reports
* GitHub Actions matrix (3 browsers) with nightly schedule and report artifacts

## Structure
```
pages/        page objects (Login, Inventory, Cart, Checkout)
fixtures/     custom Playwright fixtures
test-data/    users & checkout data
tests/        specs (login, inventory, cart-checkout, network, a11y/visual)
docs/         test plan, test cases, sample bug report
```

## How to run
```bash
npm install
npx playwright install --with-deps
npm test                    # all browsers, headless
npm run test:smoke          # only @smoke
npx playwright test --project=chromium --headed
npm run test:visual:update  # create visual baselines first time (@visual)
npm run report              # open the HTML report
```
Override the target with `BASE_URL=https://staging... npm test`.

## Test coverage
See [`docs/test-cases.md`](docs/test-cases.md) for the traceability table and [`docs/test-plan.md`](docs/test-plan.md) for the strategy.
