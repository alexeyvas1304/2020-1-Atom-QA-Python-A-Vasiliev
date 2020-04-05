from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

RETRY_COUNT = 3


class BasePage:

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 8
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                self.scroll_to_element(element)
                element.click()
                return

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
        raise

    def send(self, locator, message, timeout=None):
        elem = self.wait(timeout).until((EC.element_to_be_clickable(locator)))  # какое событие ?
        elem.send_keys(message)

    def scroll_to_element(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)
