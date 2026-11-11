from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CartPage(BasePage):
    HEADER = (AppiumBy.XPATH, "//android.widget.TextView[@text='My Cart']")
    ITEM_TITLE = BasePage.acc("product label")
    REMOVE = BasePage.acc("remove item")
    CHECKOUT = BasePage.acc("Proceed To Checkout button")

    def is_loaded(self) -> bool:
        return self.is_visible(self.HEADER, timeout=10)

    def item_titles(self) -> list[str]:
        return [e.text for e in self.find_all(self.ITEM_TITLE)]

    def remove_first_item(self):
        self.tap(self.REMOVE)
        return self

    def proceed_to_checkout(self):
        self.tap(self.CHECKOUT)
