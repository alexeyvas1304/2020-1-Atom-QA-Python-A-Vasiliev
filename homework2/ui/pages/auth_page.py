from selenium.webdriver.common.keys import Keys

from ui.pages.base_page import BasePage
from ui.locators.locators import AuthPageLocators


class AuthPage(BasePage):
    locators = AuthPageLocators()

    def authorize(self, email, password):
        self.click(self.locators.ENTER_BUTTON)
        self.send(self.locators.EMAIL_FIELD, email)
        self.send(self.locators.PASSWORD_FIELD, password)
        self.send(self.locators.PASSWORD_FIELD, Keys.RETURN)
