import pytest
from selenium.webdriver.support import expected_conditions as EC
from ui.locators.locators import *
from tests.tests_ui.test_base import BaseCase
import requests
from lxml.html import fromstring
from selenium.webdriver import ActionChains
from unique_names_generator import gen
import allure


class Test(BaseCase):
    @pytest.mark.UI
    @allure.feature('form of authorization')
    def test_only_username(self, auth_page):
        '''
        Тест на авторизацию без ввода пароля
        Переходит на страницу авторизации и заполняет только логин, после чего нажимает кнопку авторизации
        Ждет отображения поля для ввода имени (так как авторизоваться не вышло, я остаюсь на той же странице,
        а поле ввода имени слкжит индикатором этой страницы (в других тестах тоже))
        '''
        self.auth_page = auth_page
        self.auth_page.send(self.auth_page.locators.USERNAME_FIELD, next(gen))
        self.base_page.click(self.auth_page.locators.SUBMIT_BUTTON)
        self.base_page.find(self.auth_page.locators.USERNAME_FIELD).is_displayed()
        self.base_page.make_screenshot("screen_1")

    @pytest.mark.UI
    @allure.feature('form of authorization')
    def test_only_password(self, auth_page, api_client):
        '''
        Тест на авторизацию без ввода имени
        Переходит на страницу авторизации и заполняет только пароль, после чего нажимает кнопку авторизации
        Ждет отображения поля для ввода имени
        '''
        self.auth_page = auth_page
        self.base_page.send(self.auth_page.locators.PASSWORD_FIELD, api_client.password)
        self.base_page.click(self.auth_page.locators.SUBMIT_BUTTON)
        self.base_page.find(self.auth_page.locators.USERNAME_FIELD).is_displayed()
        self.base_page.make_screenshot("screen_1")

    @pytest.mark.UI
    @allure.feature('form of authorization')
    def test_no_password_and_username(self, auth_page):
        '''
        Тест на авторизацию только с нажатием кнопки авторизации бе ввода чего-либо
        Ждет отображения поля для ввода имени
        '''
        self.auth_page = auth_page
        self.base_page.click(self.auth_page.locators.SUBMIT_BUTTON)
        self.base_page.find(self.auth_page.locators.USERNAME_FIELD).is_displayed()
        self.base_page.make_screenshot("screen_1")

    @pytest.mark.UI
    @allure.feature('form of authorization')
    def test_negative_authorization(self):
        '''
        Тест на неверную авторизацию с неверными логином и/или паролем
        Переходит на страницу авторизации и заполняяет поля логина и пароля соответсвенно значениями
        BAD_USERNAME и BAD_PASSWORD
        Ждет отображения специального сообщения об ошибке
        '''
        self.auth_page.authorize('BAD_USERNAME', 'BAD_PASSWORD')
        self.base_page.find(self.auth_page.locators.ERROR_MESSAGE_INVALID_USERNAME_OR_PASSWORD).is_displayed()
        self.base_page.make_screenshot("screen_1")

    @pytest.mark.UI
    @allure.feature('form of authorization')
    def test_positive_authorization(self, api_client, mysql_worker):
        '''
        Тест на верную авторизацию
        Заполняет данные заведомо существующего api клиента
        Ждет отображения поля c главной страницы,  также проверяет в бд, что пользователь активен и не заблокирован
        '''
        self.auth_page.authorize(api_client.username, api_client.password)
        self.base_page.find(self.main_page.locators.SUCCESS_ACCESS_LOCATOR).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.get_active_status_by_name(api_client.username) == 1
        assert mysql_worker.get_access_status_by_name(api_client.username) == 1
        # assert mysql_worker.session.query(User.username, User.start_active_time).filter(
        #     User.username == api_client.username).one().start_active_time == ???

    @pytest.mark.STRANGE_BUGS
    @allure.feature('form of authorization')
    def test_strange_positive_authorization(self, api_client):
        '''
        Тест на авторизацию с существующем логином, но другого регистра. По моему мнению баг
        Авторизуется с заведомо существующим логином и паролем, но логин в верхнем регистре
        Ждет отображения поля c сообщением о неверном логине/пароле, но по факту не дожидается, тк проходит на главную страницу
        '''
        self.auth_page.authorize(api_client.username.upper(), api_client.password)
        try:
            self.base_page.make_screenshot("screen_1")
            self.base_page.find(self.auth_page.locators.ERROR_MESSAGE_INVALID_USERNAME_OR_PASSWORD).is_displayed()
        except Exception:
            raise Exception(f"Not found locator ERROR_MESSAGE_INVALID_USERNAME_OR_PASSWORD")

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('form of registration')
    def test_good_registration_bad_db_record(self, going_to_registration, api_client, mysql_worker):
        '''
        Тест на правильную регистрацию (с валидными полями)
        Идет заполнение валидными, гарантированно уникальными логином и почтой и валидным паролем
        Ждет отображения поля c главной страницы, затем проверяет статус вошедшего пользователя в бд
        Он будет равен не 1, а 0, поэтому это баг
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.reg_page.registrate(name, f"{name}@mail.ru", '12345678')
        self.base_page.find(self.main_page.locators.SUCCESS_ACCESS_LOCATOR).is_displayed()
        self.base_page.make_screenshot("screen_1")
        count = mysql_worker.find_count_by_name(name)
        status = mysql_worker.get_active_status_by_name(name)
        api_client.delete_user(name)
        assert count == 1  # пройдет
        assert status == 1, f"Expected status is 1, but got 0"  # не пройдет

    @pytest.mark.UI
    @allure.feature('form of registration')
    def test_registration_existing_username(self, going_to_registration, api_client, mysql_worker):
        '''
        Тест на регистрацию пользователя с существующим в базе именем
        Региситрирует пользователя с заведомо существующим в базе именем (именем api клиента)
        Ждет отображения сообщения о соответствующей ошибке
        После идет в базу и проверяет, что в базе только 1 пользователь с таким именем
        '''
        self.reg_page = going_to_registration
        self.reg_page.registrate(api_client.username, 'verygood@mail.ru', '12345678')
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_USER_ALREADY_EXISTS).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(api_client.username) == 1

    @pytest.mark.STRANGE_BUGS
    @allure.feature('form of registration')
    def test_registration_existing_email(self, going_to_registration, api_client, mysql_worker):
        '''
       Тест на регистрацию пользователя с существующим в базе мейлом
       Региситрирует пользователя с заведомо существующим в базе мейлом (мейлом api клиента)
       Проверяет в базе, что после попытки регистрации в базе только один пользователь с таким мейлом
       Затем ждет отображения сообщения о соответствующей ошибке user already exist, однако вместо этого натыкается
       на непонятное INTERNAL SERVER ERROR
       Я бы это назвал багом
       '''
        self.reg_page = going_to_registration
        self.reg_page.registrate(next(gen), api_client.email, '12345678')
        assert mysql_worker.find_count_by_email(api_client.email) == 1  # пройдет
        try:
            self.base_page.make_screenshot("screen_1")
            self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_USER_ALREADY_EXISTS).is_displayed()  # не пройдет
        except Exception:
            raise Exception("Not found locator ERROR_MESSAGE_USER_ALREADY_EXISTS")

    @pytest.mark.UI
    @allure.feature('form of registration')
    @pytest.mark.parametrize('email', ['cococo', 'cococo@mail', 'mail.ru', 'cococo@mail.', '@mail.ru'])
    def test_registration_bad_email(self, going_to_registration, email, mysql_worker):
        '''
       Тест на регистрацию пользователя с мейлом с неправильным шаблоном
       Пытается заренистрирвоать пользователя с нормальным имнем и паролем и мейлом, который не удовлетворяет шаблону {1,}@{1,}.{1,}
       Ждет отображения сообщения о соответствующей ошибке invalid email address
       Также идет в базу, чтоб удостовериться, что запись с таким мейлолм не внесена
       '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.reg_page.registrate(name, email, '12345678')
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_INVALID_EMAIL_ADDRESS).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0

    @pytest.mark.UI
    @allure.feature('form of registration')
    @pytest.mark.parametrize('email', ['abc', 'a@b.c'])
    def test_registration_short_email(self, going_to_registration, email, mysql_worker):
        '''
        Тест на регистрацию пользователя с хорошими логином и паролем но
        коротким мейлом (< 6 символов) - может как удовлетворять шаблону, так и нет
        Ждет отображения сообщения о соответствующей ошибке incorrect email length
        Также идет в базу, чтоб удостовериться, что запись с таким мейлолм не внесена
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.reg_page.registrate(name, email, '12345678')
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_INCORRECT_EMAIL_LENGTH).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0

    @pytest.mark.UI
    @allure.feature('form of registration')
    def test_registration_long_mail(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию пользователя с хорошими логином и паролем но
        длинным мейлом (> 64 символов) и удовлетворяющим шаблону
        Ждет отображения сообщения о соответствующей ошибке incorrect email length
        Также идет в базу, чтоб удостовериться, что запись с таким мейлолм не внесена
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.reg_page.registrate(name, 'a' * 70 + '@mail.ru', '12345678')
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_INCORRECT_EMAIL_LENGTH).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('form of registration')
    def test_registration_with_little_username(self, going_to_registration):
        '''
        Тест на регистрацию c маленьким логином (меньше 6 символов)
        Регистрируется с логином меньше 6 символов и валидными мейлом и паролем
        Ждет отображения поля c главной страницы, но не проходит, так как система авторизации не пропускает
        В ТЗ не сказано об ограничении длины логина снизу, поэтому это баг
        '''
        self.reg_page = going_to_registration
        self.reg_page.registrate('ilya', 'ilya@mail.ru', '12345678')
        try:
            self.base_page.make_screenshot("screen_1")
            self.base_page.find(self.main_page.locators.SUCCESS_ACCESS_LOCATOR).is_displayed()
        except Exception:
            raise Exception("Not found locator SUCCESS_ACCESS_LOCATOR")

    @pytest.mark.UI
    @allure.feature('form of registration')
    def test_registration_with_long_username(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию c длинным логином (>16 символов)
         Регистрируется с логином больше 16 символов и валидными мейлом и паролем
        Ждет отображения сообщения о соответствующей ошибке incorrect username length
        Также идет в базу удостовериться, что записи в бд нет
        '''
        self.reg_page = going_to_registration
        self.reg_page.registrate('loooooooooooooong_name', f'{next(gen)}@mail.ru', '12345678')
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_INCORRECT_USERNAME_LENGTH).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name('loooooooooooooong_name') == 0

    @pytest.mark.UI
    @allure.feature('form of registration')
    def test_registration_different_passwords(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию c несовпадающими паролями
        Заполняет поля пароля и его подтверждения разными значениями, остальные поля заполняет нормально
        Ждет отображения сообщения о соответствующей ошибке passwords must match
        Также идет в базу удостовериться, что записи в базе нет
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.base_page.send(self.reg_page.locators.USERNAME_FIELD, name)
        self.base_page.send(self.reg_page.locators.EMAIL_FIELD, f'{name}test@mail.ru')
        self.base_page.send(self.reg_page.locators.PASSWORD_FIELD, '12345678')
        self.base_page.send(self.reg_page.locators.CONFIRM_PASSWORD_FIELD, '1234567')
        self.base_page.click(self.reg_page.locators.ACCEPT_CHECKBOX)
        self.base_page.click(self.reg_page.locators.SUBMIT_BUTTON)
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_PASSWORDS_MUST_MATCH).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0

    @pytest.mark.UI
    @allure.feature('form of registration')
    def test_registration_without_accept(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию без принятия условий
        Вводим по правилам все поля, но не ставим галочку
        Ждет отображения поля для ввода имени
        Также идет в базу удостовериться, что записи в бд нет
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.base_page.send(self.reg_page.locators.USERNAME_FIELD, name)
        self.base_page.send(self.reg_page.locators.EMAIL_FIELD, f'{name}test@mail.ru')
        self.base_page.send(self.reg_page.locators.PASSWORD_FIELD, '12345678')
        self.base_page.send(self.reg_page.locators.CONFIRM_PASSWORD_FIELD, '12345678')
        self.base_page.click(self.reg_page.locators.SUBMIT_BUTTON)
        self.base_page.find(self.reg_page.locators.CONFIRM_PASSWORD_FIELD).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0

    @pytest.mark.STARNGE_BUGS
    @allure.feature('form of registration')
    def test_registration_with_russian(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию с именем и паролем с юникодными символами
        Проверяет (по мейлу, который англоязычный и уникальный), что записи в базе нет
        Далее проверяет, что НЕ высветилось сообщение об internal server error и падает, потому что оно есть
        С моей точки зреня как пользователя это баг - не следует пользователю демонстрировать, что ошибка
        случилась на сервере
        '''
        self.reg_page = going_to_registration
        self.reg_page.registrate('ЧЕРЕМШАНЦЕВ', 'ODINAKOVYE_RODINKI124@MAIL.RU', 'пароль')
        assert mysql_worker.find_count_by_email('ODINAKOVYE_RODINKI124@MAIL.RU') == 0
        try:
            self.base_page.wait(timeout=2).until(EC.invisibility_of_element_located(self.reg_page.locators.ERROR_MESSAGE_INTERNAL_SERVER_ERROR))
            self.base_page.make_screenshot("screen_1")
        except Exception:
            raise Exception("ERROR_MESSAGE_INTERNAL_SERVER_ERROR appeared")

    @pytest.mark.UI
    @allure.feature('form of registration')
    def test_registration_many_problems(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию с несколькими нарушениями сразу
        Заполняет только логин и пароль без подтверждения
        Ждет отображения сообщения о соответствующей ошибке(имеет очень странный вид - мб переквалифицировать в баг)
        ПРоверяет, что записи в базе нет
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.base_page.send(self.reg_page.locators.USERNAME_FIELD, name)
        self.base_page.send(self.reg_page.locators.PASSWORD_FIELD, '12345678')
        self.base_page.click(self.reg_page.locators.ACCEPT_CHECKBOX)
        self.base_page.click(self.reg_page.locators.SUBMIT_BUTTON)
        self.base_page.find(self.reg_page.locators.ERROR_MESSAGE_MANY_PROBLEMS).is_displayed()
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0

    @pytest.mark.STRANGE_BUGS
    @allure.feature('form of registration')
    def test_registration_with_little_password(self, going_to_registration, api_client, mysql_worker):
        '''
        Тест на регистрацию c маленьким паролем (хотя бы один символ)
        Регистрирует пользователя с нормальными логином и мейлом, но очень коротким паролем
        Пропускает на главную страницу, хотя по идее не должен (это мое видение, с точки зрения безопасности это баг)
        Ждет, что в базе не будет записи
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.reg_page.registrate(name, f'{name}@mail.ru', '1')
        api_client.delete_user(name)
        try:
            self.base_page.make_screenshot("screen_1")
            self.base_page.find(self.reg_page.locators.CONFIRM_PASSWORD_FIELD).is_displayed()
        except Exception:
            raise Exception("Not found locator CONFIRM_PASSWORD_FIELD")
        assert mysql_worker.find_count_by_name(name) == 0, f'Expected 0 records for such user, got 1'

    @pytest.mark.STRANGE_BUGS
    @allure.feature('form of registration')
    def test_registration_with_long_password(self, going_to_registration, mysql_worker):
        '''
        Тест на регистрацию c длинным паролем (>256 символов)
        Пытается зарегистрировать пользователя с нормальными логином и мейлом, но очень длинным паролем
        Ждет, что в базе не будет записи
        Ждет ОТСУТСТВИИЯ специального сообщения internal server error, и падает, так как оно высвечивается
         С моей точки зреня как пользователя это баг - не следует пользователю демонстрировать, что ошибка
        случилась на сервере
        '''
        self.reg_page = going_to_registration
        name = next(gen)
        self.reg_page.registrate(name, f'{name}@mail.ru', '1' * 300)
        self.base_page.make_screenshot("screen_1")
        assert mysql_worker.find_count_by_name(name) == 0
        try:
            self.base_page.wait(timeout=2).until(
                EC.invisibility_of_element_located(self.reg_page.locators.ERROR_MESSAGE_INTERNAL_SERVER_ERROR))
            self.base_page.make_screenshot("screen_1")
        except Exception:
            raise Exception("ERROR_MESSAGE_INTERNAL_SERVER_ERROR appeared")

    @pytest.mark.UI
    @allure.feature('mock feature')
    def test_mock_existing(self, going_to_registration, api_client):
        '''
        Тест на появление записи vk id для пользователя, который есть в моке
        Добавляет пользователя good_variant в мок, затем регистрирует его
        Ожидает верную запись в правом верхнем углу главной страницы
        '''
        requests.post('http://0.0.0.0:5000/vk_id/add_user', data={"name": "good_variant", "id": '15'})
        self.reg_page = going_to_registration
        self.reg_page.registrate('good_variant', 'good_variant@mail.ru', '12345')
        self.base_page.find((By.XPATH, self.main_page.locators.VK_ID_MARK.format('15')))
        self.base_page.make_screenshot("screen_1")
        api_client.delete_user('good_variant')

    @pytest.mark.UI
    @allure.feature('mock feature')
    def test_mock_not_existing(self, going_to_registration, api_client):
        '''
        Тест на непоявление записи vk id для пользователя, которого в моке
        Регистрирует пользователя, которого заведомо нет в моке
        Ожидает отсутствие соответсвующей запси про vk id
        '''
        self.reg_page = going_to_registration
        self.reg_page.registrate('bad_variant', 'bad_variant@mail.ru', '12345')
        self.base_page.make_screenshot("screen_1")
        api_client.delete_user('bad_variant')
        self.base_page.wait().until(
            EC.invisibility_of_element_located((By.XPATH, self.main_page.locators.VK_ID_MARK.format(''))))

    @pytest.mark.STRANGE_BUGS
    @allure.feature('mock feature')
    def test_mock_existing_huge_id(self, going_to_registration, api_client, driver):
        '''
        Тест на очень большое значение vk id
        РЕгистрирует сначала в моке, а потом в приложении пользоавтеля bugger с vk id в 700 единиц
        Тест показывает, что при огромном id начинает ехать верстка и слова logged as уже не видны
        Можно отнести к багам
        '''
        r = requests.post('http://0.0.0.0:5000/vk_id/add_user', data={"name": "bugger", "id": "1" * 700})
        self.reg_page = going_to_registration
        self.reg_page.registrate('bugger', 'bug_variant@mail.ru', '12345')
        el = self.base_page.find(self.main_page.locators.LOGGED_AS)
        self.base_page.make_screenshot("screen_1")
        assert el.location['x'] >= 0, f'Expected that coords of locator LOGGED_AS are >=0 (in monitor)'
        api_client.delete_user('bugger')

    @pytest.mark.UI
    @allure.feature('main page')
    def test_right_name_in_corner(self, api_client, authorization):
        '''
        Тест на то, что в logged as находится имя авторизованного юзера
        Пользователя авторизуется и сравнивается имя пользователя и текст из локатора
        '''
        self.main_page = authorization
        right_corner_text = self.base_page.find(self.main_page.locators.LOGGED_AS).text
        self.base_page.make_screenshot("screen_1")
        assert right_corner_text == f'Logged as {api_client.username}'

    @pytest.mark.UI
    @allure.feature('main page')
    @pytest.mark.parametrize('locator,expected_title',
                             [(MainPageLocators.API_CIRCLE, 'application programming interface'),
                              (MainPageLocators.FUTURE_INTERNET_CIRCLE,
                               'what will the internet be like in the next 50 years?'),
                              (MainPageLocators.SMTP_CIRCLE, 'smtp'),
                              (MainPageLocators.PYTHON_BUTTON, 'welcome to python.org')  # ???
                              ])
    def test_click_visible_hrefs(self, authorization, locator, expected_title):
        '''
        Тест на правильность ссылок, которые могут быть кликнуты непосредственно
        Тест получает ссылку, идет по ней и смотрит title страницы, после чего проверяет
        что в title есть тематика ссылки
        '''
        self.main_page = authorization
        href = self.base_page.find(locator).get_attribute('href')
        r = requests.get(href)
        tree = fromstring(r.content)
        assert expected_title in tree.findtext('.//title').lower()

    @pytest.mark.UI
    @allure.feature('main page')
    @pytest.mark.parametrize('visible_locator,invisible_locator, expected_title',
                             [(MainPageLocators.PYTHON_BUTTON, MainPageLocators.PYTHON_HISTORY_HREF,
                               'history of python'),
                              (MainPageLocators.PYTHON_BUTTON, MainPageLocators.FLASK_HREF, 'welcome to flask'),
                              (MainPageLocators.NETWORK_BUTTON, MainPageLocators.WIRESHARK_NEWS_HREF,
                               'wireshark · news'),
                              (MainPageLocators.NETWORK_BUTTON, MainPageLocators.WIRESHARK_DOWNLOAD_HREF,
                               'wireshark · go deep'),  # плохо
                              (MainPageLocators.NETWORK_BUTTON, MainPageLocators.TCPDUMP_EXAMPLES_HREF,
                               'tcpdump examples')

                              ])
    def test_click_invisible_hrefs_good(self, authorization, visible_locator, invisible_locator, expected_title):
        '''
        Тест на правильность ссылок, которые НЕ могут быть кликнуты непосредственно
        Тест получает ссылку, идет по ней и смотрит title страницы, после чего проверяет
        что в title есть тематика ссылки
        '''
        self.main_page = authorization
        visible_element = self.base_page.find(visible_locator)
        ac = ActionChains(self.driver)
        ac.move_to_element(visible_element).perform()
        href = self.base_page.find(invisible_locator).get_attribute('href')
        r = requests.get(href)
        tree = fromstring(r.content)
        assert expected_title in tree.findtext('.//title').lower()

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('main page')
    def test_click_centos_bug(self, authorization):
        '''
        Суть теста такая же как у предыдущего, однако он выделен, так как этот случай багованной и ему нужен другой маркер
        Тест судя по названию ведет на страницу скачивания centos7, но в реальности ведет на страницу скачивания fedora
        '''
        self.main_page = authorization
        visible_element = self.base_page.find(self.main_page.locators.LINUX_BUTTON)
        ac = ActionChains(self.driver)
        ac.move_to_element(visible_element).perform()
        href = self.base_page.find(self.main_page.locators.CENTOS_HREF).get_attribute('href')
        r = requests.get(href)
        tree = fromstring(r.content)
        assert 'centos' in tree.findtext('.//title').lower()

    @pytest.mark.UI
    @allure.feature('main page')
    def test_refresh(self, authorization, driver, api_client):
        '''
        Тест на возвращение к странице авторизации при блокировке
        Тест заходит от пользователя, затем через api пользователь деавторизуется
        после чего делается рефреш страницы
        Ожидается поле с соответсвующим сообщением про авторизованных пошьзователей
        '''
        self.main_page = authorization
        self.base_page.make_screenshot("screen_1")
        api_client.block_user(api_client.username)
        driver.refresh()
        self.base_page.find(self.auth_page.locators.ERROR_MESSAGE_ONLY_AUTHORIZED_USERS).is_displayed()
        self.base_page.make_screenshot("screen_2")

    @pytest.mark.UI
    @allure.feature('main page')
    def test_logout(self, authorization, api_client, mysql_worker):
        '''
        Тест на нажатие кнопки logout
        АВторизуемя, проверяем, что active 1
        Затем нажимаем на logout и проверяем, что есть поле ввода пароля и active теперь 0
        '''
        self.main_page = authorization
        assert mysql_worker.get_active_status_by_name(api_client.username) == 1
        self.base_page.click(self.main_page.locators.LOGOUT_BUTTON)
        self.base_page.find(self.auth_page.locators.USERNAME_FIELD).is_displayed()
        assert mysql_worker.get_active_status_by_name(api_client.username) == 0
