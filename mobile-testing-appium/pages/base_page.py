"""BasePage: shared, explicit-wait helpers used by every page object."""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)

    # --- locators helpers -------------------------------------------------
    @staticmethod
    def acc(value: str):
        """Accessibility-id locator (content-desc on Android)."""
        return (AppiumBy.ACCESSIBILITY_ID, value)

    # --- actions ----------------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def tap(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_down(self):
        """Native UiAutomator2 scroll gesture (more reliable than raw touch actions)."""
        self.driver.execute_script(
            "mobile: scrollGesture",
            {"left": 100, "top": 500, "width": 600, "height": 1200,
             "direction": "down", "percent": 0.8},
        )
