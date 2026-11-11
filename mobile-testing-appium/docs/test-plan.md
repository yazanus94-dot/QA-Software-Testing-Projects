# Test Plan — Sauce Labs My Demo App (Android)

## 1. Objective
Verify that the core shopper journeys (authentication, browsing, cart) work correctly on Android and behave well under mobile-specific conditions.

## 2. Scope
**In scope:** login/logout, product catalog, product details, cart, orientation change, backgrounding, scrolling.
**Out of scope:** payment gateway, push notifications, iOS, performance/security testing (separate repositories).

## 3. Test approach
| Level | Technique | Automation |
|---|---|---|
| Smoke | Critical path after each build | Yes (`-m smoke`) |
| Regression | Functional + negative + boundary | Yes (`-m regression`) |
| Mobile-specific | Gestures, rotation, interruptions | Yes (`-m gestures`) |
| Exploratory | Usability, accessibility, edge devices | Manual, charter-based |

## 4. Environments
Android 14 (API 34) emulator in CI · one real mid-range device locally · Appium 2 / UiAutomator2.

## 5. Entry / exit criteria
* Entry: build installs, app launches, Appium session opens.
* Exit: 100% smoke pass, ≥95% regression pass, no open Critical/High defects.

## 6. Risks & mitigation
| Risk | Mitigation |
|---|---|
| Flaky element timing | Explicit waits, 1 automatic rerun in CI |
| Emulator slowness | KVM acceleration, smoke-only on PRs |
| APK version drift | Locators centralised in page objects |

## 7. Deliverables
Automated suite, HTML report, screenshots on failure, bug reports, this plan.
