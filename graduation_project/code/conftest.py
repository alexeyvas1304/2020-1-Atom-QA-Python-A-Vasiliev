import pytest
import time
import os
import requests
import logging
import allure
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.auth_page import AuthPage
from ui.pages.reg_page import RegPage
from ui.pages.main_page import MainPage
from api.client import Client
from db.orm_connection import MysqlOrmConnection
from db.orm_worker import MysqlOrmWorker
from db.models import User
from unique_names_generator import gen


class UnsupportedBrowserException(Exception):
    pass


def pytest_addoption(parser):
    parser.addoption('--url', default='http://0.0.0.0:7000')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='latest')
    parser.addoption('--selenoid', default='False')


def pytest_configure(config):
    if not hasattr(config, "slaveinput"):
        os.system('docker-compose up -d')
        while True:
            try:
                requests.get('http://0.0.0.0:7000')
                break
            except requests.exceptions.ConnectionError:
                pass


def pytest_unconfigure(config):
    if not hasattr(config, "slaveinput"):
        os.system('docker-compose down')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')
    return {'url': url, 'browser': browser, 'version': version, 'selenoid': selenoid}


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
            url = 'http://application:7000'
            capabilities = {
                'acceptInsecureCerts': True,
                'browserName': 'chrome',
                'version': '80.0'
            }
            st = time.time()
            driver = webdriver.Remote(command_executor=selenoid,
                                      desired_capabilities=capabilities)
            print(time.time() - st)
    else:
        raise UnsupportedBrowserException(f'Браузер {browser} не поддерживается')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def base_page(driver, config):
    return BasePage(driver, config)


@pytest.fixture(scope='function')
def auth_page(driver, config):
    return AuthPage(driver, config)


@pytest.fixture(scope='function')
def reg_page(driver, config):
    return RegPage(driver, config)


@pytest.fixture(scope='function')
def main_page(driver, config):
    return MainPage(driver, config)


@pytest.fixture(scope='function')
def authorization(driver, config, auth_page, api_client):
    page = auth_page
    page.authorize(api_client.username, api_client.password)
    return MainPage(driver, config)


@pytest.fixture(scope='function')
def going_to_registration(driver, config, auth_page):
    page = auth_page
    page.go_to_registration()
    return RegPage(driver, config)


@pytest.fixture(scope='function')
def registration(driver, config, reg_page):
    page = reg_page
    page.registrate('qwertyui', 'qwertyui@mail.ru', '12345678')
    return MainPage(driver, config)


@pytest.fixture(scope='function')
def tmp_user(api_client):
    username = next(gen)
    r = api_client.add_user(username=username, email=f'{username}@mail.ru', password='12345678')
    yield (username, r.status_code)
    api_client.delete_user(username)


@pytest.fixture(scope='function')
def api_client(mysql_orm_client, mysql_worker, logger_api):
    username = next(gen)
    password = f'{username}_pass'
    email = f'{username}@mail.ru'
    client = User(username=username, password=password, email=email, access=1, active=0)  # это запись в базу
    mysql_orm_client.session.add(client)
    mysql_orm_client.session.query(User.id).count()  # любой запрос в базу
    yield Client(username, password, email, logger_api)  # это клиент API
    mysql_orm_client.session.delete(client)
    mysql_orm_client.session.query(User.id).count()


@pytest.fixture(scope='session')
def mysql_orm_client():
    conn = MysqlOrmConnection('test_qa', 'qa_test', 'diplom_db')
    yield conn
    conn.connection.close()


@pytest.fixture(scope='function')
def mysql_worker(mysql_orm_client):
    return MysqlOrmWorker(mysql_orm_client)


@pytest.fixture(scope="function")
def logger_api(request):
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = request.node.location[-1]

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    log = logging.getLogger('api_log')
    log.propogate = False
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    failed_count = request.session.testsfailed
    yield log

    if request.session.testsfailed > failed_count:
        with open(log_file, 'r') as f:
            allure.attach(f.read(), name=log.name, attachment_type=allure.attachment_type.TEXT)

    os.remove(log_file)
