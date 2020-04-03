import pytest

RETRY_COUNT = 3


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.base_page = request.getfixturevalue('base_page')
        self.auth_page = request.getfixturevalue('auth_page')
        self.main_page = request.getfixturevalue('main_page')



