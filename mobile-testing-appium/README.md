# 📱 Mobile Testing — Appium + Python + Pytest (Android)

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Appium](https://img.shields.io/badge/Appium-2.x-purple) ![Pytest](https://img.shields.io/badge/Pytest-8-green) ![Platform](https://img.shields.io/badge/Android-UiAutomator2-brightgreen)

Automated mobile test suite for the open-source **Sauce Labs My Demo App (Android)**, built with the
**Page Object Model**, explicit waits, parametrised data-driven tests, mobile gestures, automatic
failure screenshots, an HTML report and a CI pipeline on an Android emulator.

> Author: **Yazan Aljabari** | QA / Software Test Engineer

## What this project demonstrates
| Skill | Where |
|---|---|
| Page Object Model, no sleeps (explicit waits only) | `pages/` |
| Data-driven + negative testing | `tests/test_login.py` |
| Mobile gestures, orientation, app lifecycle | `tests/test_gestures_and_device.py` |
| Test strategy, test cases, bug reporting | `docs/` |
| CI on an Android emulator + report artifacts | `.github/workflows/android-ci.yml` |
| Failure screenshots + self-contained HTML report | `tests/conftest.py`, `pytest.ini` |

## Project structure
```
config/      settings (env-var driven)
pages/       BasePage + Login / Catalog / Cart page objects
tests/       smoke, regression and gesture suites + fixtures
docs/        test plan, test cases, sample bug report
apps/        put the APK here (git-ignored)
```

## How to run
1. Install: Node 20+, Python 3.10+, JDK 17, Android SDK (an emulator or a real device with USB debugging).
2. `npm i -g appium && appium driver install uiautomator2`
3. `pip install -r requirements.txt`
4. Download the APK into `apps/mda-app.apk` (see `apps/README.md`).
5. Start an emulator, then in one terminal: `appium`
6. In another terminal:
```bash
pytest -m smoke          # critical path only
pytest                   # everything
pytest -m gestures       # mobile-specific checks
```
Report: `reports/report.html` · Failure screenshots: `screenshots/`

Configuration via env vars: `APPIUM_URL`, `APP_PATH`, `DEVICE_NAME`, `PLATFORM_VERSION`, `EXPLICIT_WAIT`.

## Notes
* Locators live in the page classes (single place to update). If you use a different APK version,
  confirm them with **Appium Inspector**.
* iOS is a natural extension: add an `XCUITest` options fixture and reuse the same page objects through accessibility ids.
