import pytest
import time

from selenium.webdriver.support import expected_conditions as EC

from ui.locators.locators import *
from tests.base import BaseCase


class Test(BaseCase):
    @pytest.mark.UI
    def test_negative_authorization(self, driver):
        self.auth_page.authorize('BAD_LOGIN@mail.ru', 'BAD_PASSWORD')
        self.base_page.find(self.auth_page.locators.BAD_AUTHORIZATION_LOCATOR).is_displayed()

    @pytest.mark.UI
    def test_positive_authorization(self, authorization):
        self.main_page = authorization

    @pytest.mark.UI
    def test_create_campaign(self, authorization):
        self.main_page = authorization
        site_name = 'https://example.com'
        campaign_name = 'QAPython' + str(int(time.time()))
        self.main_page.create_campaign(site_name, campaign_name)
        self.base_page.find((By.XPATH, self.main_page.locators.CREATED_CAMPAIGN.format(campaign_name)))

        self.base_page.click((By.XPATH, self.main_page.locators.CREATED_CAMPAIGN_CHECKBOX.format(
            campaign_name)))

        self.base_page.click(self.main_page.locators.ACTIONS)
        self.base_page.click(self.main_page.locators.DELETE_ACTION)

    @pytest.mark.UI
    def test_create_segment(self, authorization, api_client):
        self.main_page = authorization
        name = 'QAPython' + str(int(time.time()))
        self.main_page.create_segment(name)
        self.base_page.find(
            (By.XPATH, self.main_page.locators.CREATED_SEGMENT.format(name))).is_displayed()
        created_element_id = self.main_page.find(
            (By.XPATH, self.main_page.locators.CREATED_SEGMENT_ID_FIELD.format(name))).text
        api_client.delete_segment(created_element_id)

    @pytest.mark.UI
    def test_delete_segment(self, authorization):
        self.main_page = authorization
        name = 'QAPython' + str(int(time.time()))
        self.main_page.create_segment(name)
        self.main_page.delete_segment(name)
        self.base_page.wait().until(
            EC.invisibility_of_element_located((By.XPATH, self.main_page.locators.CREATED_SEGMENT.format(name))))
