from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage(BasePage):
    # NOTE: verify with Appium Inspector if you use a different APK version.
    MENU_BUTTON = BasePage.acc("open menu")
    MENU_LOGIN = BasePage.acc("menu item log in")
    EMAIL = BasePage.acc("Username input field")
    PASSWORD = BasePage.acc("Password input field")
    LOGIN_BUTTON = BasePage.acc("Login button")
    ERROR_TEXT = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'Provided credentials') or contains(@text,'locked out')]")
    MENU_LOGOUT = BasePage.acc("menu item log out")

    def open_login(self):
        self.tap(self.MENU_BUTTON)
        self.tap(self.MENU_LOGIN)
        return self

    def login(self, email: str, password: str):
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.tap(self.LOGIN_BUTTON)
        return self

    def error_message(self) -> str:
        return self.text_of(self.ERROR_TEXT)

    def logout(self):
        self.tap(self.MENU_BUTTON)
        self.tap(self.MENU_LOGOUT)
