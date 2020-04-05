import pytest
import time

from selenium.common.exceptions import TimeoutException

from ui.locators.locators import *
from tests.base import BaseCase
from api.client import Client
from personal_data import EMAIL, PASSWORD


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
        self.main_page.find((By.XPATH, self.main_page.locators.CREATED_CAMPAIGN.format(campaign_name)))  # проверка

        self.main_page.click((By.XPATH, self.main_page.locators.CREATED_CAMPAIGN_CHECKBOX.format(
            campaign_name)))  # подчистить через апи сложно, чищу через UI

        self.base_page.click(self.main_page.locators.ACTIONS)
        self.base_page.click(self.main_page.locators.DELETE_ACTION)

    @pytest.mark.UI
    def test_create_segment(self, authorization):
        self.main_page = authorization
        name = 'QAPython' + str(int(time.time()))  # для уникальности
        self.main_page.create_segment(name)
        self.main_page.find(
            (By.XPATH, self.main_page.locators.CREATED_SEGMENT.format(name))).is_displayed()  # проверка совпадения имен
        created_element_id = self.main_page.find(
            (By.XPATH, self.main_page.locators.CREATED_SEGMENT_ID_FIELD.format(name))).text
        client = Client(EMAIL, PASSWORD)
        client.delete_segment(created_element_id)  # подчищаю за собой через API, чтоб избежать переполнения сегментов

    @pytest.mark.UI
    def test_delete_segment(self, authorization):
        self.main_page = authorization
        name = 'QAPython' + str(int(time.time()))  # для уникальности
        self.main_page.create_segment(name)
        self.main_page.delete_segment(name)
        with pytest.raises(TimeoutException):
            self.main_page.find((By.XPATH, self.main_page.locators.CREATED_SEGMENT.format(name)))
