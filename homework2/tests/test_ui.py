import pytest
import time

from selenium.common.exceptions import TimeoutException

from ui.locators.locators import *
from tests.base import BaseCase


class Test(BaseCase):
    # @pytest.mark.skip
    @pytest.mark.UI
    def test_negative_authorization(self, driver):
        self.auth_page.authorize('BAD_LOGIN@mail.ru', 'BAD_PASSWORD')
        self.base_page.find(self.auth_page.locators.BAD_AUTHORIZATION_LOCATOR).is_displayed()  # base_page -> bad_page ?

    # @pytest.mark.skip
    @pytest.mark.UI
    def test_positive_authorization(self, authorization):
        self.main_page = authorization

    # @pytest.mark.skip
    @pytest.mark.UI
    def test_create_campaign(self, authorization):
        self.main_page = authorization
        site_name = 'https://example.com'
        campaign_name = 'QAPython'
        self.main_page.create_campaign(site_name, campaign_name)
        CREATED_CAMPAIGN_TUPLE = (By.XPATH, self.main_page.locators.CREATED_CAMPAIGN.format(campaign_name))
        self.main_page.find(CREATED_CAMPAIGN_TUPLE)

    # @pytest.mark.skip
    @pytest.mark.UI
    def test_create_segment(self, authorization):
        self.main_page = authorization
        name = 'QAPython' + str(int(time.time()))  # для уникальности
        self.main_page.create_segment(name)
        CREATED_SEGMENT_TUPLE = (By.XPATH, self.main_page.locators.CREATED_SEGMENT.format(name))
        self.main_page.find(CREATED_SEGMENT_TUPLE)

    # @pytest.mark.skip
    @pytest.mark.UI
    def test_delete_segment(self, authorization):
        self.main_page = authorization
        name = 'QAPython' + str(int(time.time()))  # для уникальности
        self.main_page.create_segment(name)
        CREATED_SEGMENT_TUPLE = (By.XPATH, self.main_page.locators.CREATED_SEGMENT_DELETE_BUTTON.format(name))
        self.main_page.delete_segment(name)
        with pytest.raises(TimeoutException):
            self.main_page.find(CREATED_SEGMENT_TUPLE)
