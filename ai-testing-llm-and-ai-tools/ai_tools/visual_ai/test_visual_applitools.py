"""Visual AI testing with Applitools Eyes (https://applitools.com).

Applitools compares screenshots with a trained Visual-AI model, ignoring noise (anti-aliasing, tiny shifts)
and highlighting meaningful differences. Needs a free account/API key:  export APPLITOOLS_API_KEY=...
Skipped automatically when the key or SDK is missing.

NOTE: reference implementation - SDK method names can differ slightly between major versions; check the
eyes-playwright docs for the version you install.
"""
import os

import pytest

pytestmark = pytest.mark.ai_tools

if not os.getenv("APPLITOOLS_API_KEY"):
    pytest.skip("Set APPLITOOLS_API_KEY to run Visual AI tests", allow_module_level=True)

pytest.importorskip("applitools.playwright", reason="pip install eyes-playwright")
from applitools.playwright import BatchInfo, ClassicRunner, Eyes, Target  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402


@pytest.fixture(scope="module")
def runner():
    r = ClassicRunner()
    yield r
    print(r.get_all_test_results(False))


def test_login_and_inventory_visual(runner):
    eyes = Eyes(runner)
    eyes.configure.set_batch(BatchInfo("SauceDemo Visual AI"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        try:
            eyes.open(page, "SauceDemo", "Login + Inventory", {"width": 1280, "height": 800})
            page.goto("https://www.saucedemo.com")
            eyes.check(Target.window().fully().with_name("Login page"))
            page.fill("[data-test=username]", "standard_user")
            page.fill("[data-test=password]", "secret_sauce")
            page.click("[data-test=login-button]")
            eyes.check(Target.window().fully().with_name("Inventory page"))
            eyes.close_async()
        finally:
            eyes.abort_async()
            browser.close()
