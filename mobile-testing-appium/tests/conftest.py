"""Fixtures: one fresh Appium session per test, screenshot on failure."""
import os
from datetime import datetime
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config import settings
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


def _options() -> UiAutomator2Options:
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.device_name = settings.DEVICE_NAME
    opts.automation_name = "UiAutomator2"
    opts.app = settings.APP_PATH
    opts.new_command_timeout = 120
    opts.auto_grant_permissions = True
    opts.no_reset = False
    if settings.PLATFORM_VERSION:
        opts.platform_version = settings.PLATFORM_VERSION
    return opts


@pytest.fixture
def driver(request):
    drv = webdriver.Remote(settings.APPIUM_URL, options=_options())
    drv.implicitly_wait(settings.IMPLICIT_WAIT)
    request.node.driver = drv
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    drv = getattr(item, "driver", None)
    if report.when == "call" and report.failed and drv:
        Path("screenshots").mkdir(exist_ok=True)
        name = f"screenshots/{item.name}_{datetime.now():%H%M%S}.png"
        drv.save_screenshot(name)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def catalog_page(driver):
    return CatalogPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)
