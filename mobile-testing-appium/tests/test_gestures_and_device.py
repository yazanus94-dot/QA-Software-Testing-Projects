"""Mobile-specific behaviour: scrolling, orientation, app lifecycle."""
import pytest
from selenium.webdriver.common.by import By  # noqa: F401  (kept for readers extending locators)


@pytest.mark.gestures
def test_scroll_reveals_more_products(catalog_page):
    assert catalog_page.is_loaded()
    before = set(catalog_page.product_titles())
    catalog_page.scroll_down()
    after = set(catalog_page.product_titles())
    assert after - before, "Scrolling should reveal products that were off-screen"


@pytest.mark.gestures
def test_orientation_change_keeps_state(driver, catalog_page):
    assert catalog_page.is_loaded()
    driver.orientation = "LANDSCAPE"
    try:
        assert driver.orientation == "LANDSCAPE"
        assert catalog_page.product_titles(), "Catalog should still render in landscape"
    finally:
        driver.orientation = "PORTRAIT"


@pytest.mark.gestures
def test_app_survives_background_and_resume(driver, catalog_page):
    assert catalog_page.is_loaded()
    driver.background_app(3)  # send app to background for 3 seconds
    assert catalog_page.is_loaded(), "App should resume on the same screen"
