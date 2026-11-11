from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CatalogPage(BasePage):
    PRODUCT_TITLE = BasePage.acc("store item text")
    PRODUCT_CARD = BasePage.acc("store item")
    CART_BADGE = BasePage.acc("cart badge")
    ADD_TO_CART = BasePage.acc("Add To Cart button")
    CATALOG_HEADER = (AppiumBy.XPATH, "//android.widget.TextView[@text='Products']")

    def is_loaded(self) -> bool:
        return self.is_visible(self.CATALOG_HEADER, timeout=10)

    def product_titles(self) -> list[str]:
        return [e.text for e in self.find_all(self.PRODUCT_TITLE)]

    def open_first_product(self):
        self.find_all(self.PRODUCT_CARD)[0].click()
        return self

    def add_current_product_to_cart(self):
        self.tap(self.ADD_TO_CART)
        return self

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE, timeout=3):
            return 0
        text = self.text_of((AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='cart badge']/android.widget.TextView"))
        return int(text or 0)

    def open_cart(self):
        self.tap(self.CART_BADGE)
        return self
