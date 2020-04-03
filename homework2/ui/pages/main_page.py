import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage
from ui.locators.locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    def create_campaign(self, site_name, campaign_name):
        try:
            self.click(self.locators.CREATE_FIRST_CAMPAIGN_HREF)
        except TimeoutException:
            self.click(self.locators.CREATE_NOT_FIRST_CAMPAIGN_HREF)
        self.click(self.locators.TRAFIC_BUTTON)
        self.send(self.locators.SITE_NAME_FIELD, site_name)
        self.send(self.locators.CAMPAIGN_NAME_FIELD, campaign_name)
        self.click(self.locators.BANNER_OPTION)
        self.click(self.locators.DOWNLOAD_IMAGE_BUTTON)
        form = self.find(self.locators.DOWNLOAD_IMAGE_INPUT)  # send не вышел, видимо нужно другое событие
        form.send_keys(os.getcwd() + "/images/image.jpg")

        self.click(self.locators.SAVE_IMAGE)
        self.click(self.locators.SUBMIT_BUTTON)

    def create_segment(self, name):
        self.click(self.locators.GO_TO_SEGMENTS)
        try:
            self.click(self.locators.CREATE_FIRST_SEGMENT_HREF)
        except TimeoutException:
            self.click(self.locators.CREATE_NOT_FIRST_SEGMENT_HREF)

        segment_name = self.find(self.locators.SEGMENT_NAME)
        segment_name.clear()
        self.send(self.locators.SEGMENT_NAME, name)

        self.click(self.locators.ADD_SEGMENT)
        self.click(self.locators.OK_MY_MIR)
        self.click(self.locators.CHECKBOX)
        self.click(self.locators.ADD_SEGMENT_SUBMIT)
        self.click(self.locators.CREATE_SEGMENT_SUBMIT)
        CREATED_SEGMENT_TUPLE = (By.XPATH, self.locators.CREATED_SEGMENT.format(name))
        self.find(CREATED_SEGMENT_TUPLE)  # аналог time.sleep()

    def delete_segment(self, name):
        self.click(self.locators.GO_TO_SEGMENTS)
        CREATED_SEGMENT_DELETE_BUTTON_TUPLE = (By.XPATH, self.locators.CREATED_SEGMENT_DELETE_BUTTON.format(name))
        self.click(CREATED_SEGMENT_DELETE_BUTTON_TUPLE)
        self.click(self.locators.DELETE_CONFIRM_BUTTON)
        self.click(self.locators.GO_TO_SEGMENTS)  # аналог time.sleep()
