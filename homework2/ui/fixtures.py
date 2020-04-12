import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from ui.pages.auth_page import AuthPage
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from personal_data import EMAIL, PASSWORD


class UnsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    browser = config['browser']
    version = config['version']
    selenoid = config['selenoid']
    if browser == 'chrome':
        if selenoid == 'False':
            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install())
        else:
            capabilities = {
                'acceptInsecureCerts': True,
                'browserName': 'chrome',
                'version': '80.0'
            }
            driver = webdriver.Remote(command_executor=selenoid,
                                      desired_capabilities=capabilities)
    else:
        raise UnsupportedBrowserException(f'Браузер {browser} не поддерживается')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.fixture(scope='function')
def base_page(driver, config):
    return BasePage(driver, config)


@pytest.fixture(scope='function')
def auth_page(driver, config):
    return AuthPage(driver, config)


@pytest.fixture(scope='function')
def main_page(driver, config):
    return MainPage(driver, config)


@pytest.fixture(scope='function')
def authorization(driver, config, auth_page):
    page = auth_page
    page.authorize(EMAIL, PASSWORD)
    return MainPage(driver, config)
