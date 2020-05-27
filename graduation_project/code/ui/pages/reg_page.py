from ui.locators.locators import RegPageLocators
from ui.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class RegPage(BasePage):
    locators = RegPageLocators()

    def registrate(self, username, email, password):
        self.send(self.locators.USERNAME_FIELD, username)
        self.send(self.locators.EMAIL_FIELD, email)
        self.send(self.locators.PASSWORD_FIELD, password)
        self.send(self.locators.CONFIRM_PASSWORD_FIELD, password)
        self.click(self.locators.ACCEPT_CHECKBOX)
        self.click(self.locators.SUBMIT_BUTTON)
