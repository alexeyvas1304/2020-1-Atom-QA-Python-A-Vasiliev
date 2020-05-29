from ui.locators.locators import AuthPageLocators
from ui.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class AuthPage(BasePage):
    locators = AuthPageLocators()

    def authorize(self, email, password):
        self.send(self.locators.USERNAME_FIELD, email)
        self.send(self.locators.PASSWORD_FIELD, password)
        self.send(self.locators.PASSWORD_FIELD, Keys.RETURN)

    def go_to_registration(self):
        self.click(self.locators.REGISTRATION_HREF)
