import pytest
import requests
from api.client import Client
from unique_names_generator import gen
import allure


class Test:
    @pytest.mark.API
    @allure.feature('api tests without need to login')
    def test_status(self):
        '''
        Тест на статус готовности приложения
        Проверяет код и результат
        '''
        r = requests.get('http://0.0.0.0:7000/status')
        assert r.status_code == 200
        assert r.json() == {'status': 'ok'}

    @pytest.mark.API
    @allure.feature('api tests without need to login')
    def test_try_without_login(self):
        '''
        Тест - Попытка сделать что-то через api без авторизации
        Возвращает код 401, как и ожидается
        '''
        r = requests.get("http://0.0.0.0:7000/api/del_user/kirill")
        assert r.status_code == 401

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    def test_post_new_user(self, tmp_user, mysql_worker):
        '''
        Тест на добавление нового пользователя с валидными новыми данными
        Проверяет, что в базе появилась запись (само добавление происходит в фикстуре tmp_user)
        ВОзвращает код 210 вместо 201, БАГ !!!
        '''
        assert mysql_worker.find_count_by_name(tmp_user[0]) == 1
        status_code = tmp_user[1]
        assert status_code == 201, f"Expected code 201, got {status_code}"

    @pytest.mark.API
    @allure.feature('api tests on post method')
    def test_post_existing_username(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на добавление пользователя с уже существующим именем
        ПРоверяет, что в базе по этому имени только одна запись
        Возвращает 304, как и ожидается
        '''
        r = api_client.add_user(username=tmp_user[0], email='qwerty@mail.ru', password='12345678')
        assert mysql_worker.find_count_by_name(tmp_user[0]) == 1
        assert r.status_code == 304

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    def test_post_existing_email(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на добавление пользователя с уже существующим мейлом
        ПРоверяет, что в базе по этому мейлу только одна запись
        Возвращает 210, должен быть 304, БАГ!!!
        '''
        r = api_client.add_user(username='qwerty', email=f'{tmp_user[0]}@mail.ru', password='12345678')
        assert mysql_worker.find_count_by_name(tmp_user[0]) == 1
        assert r.status_code == 304, f"Expected code 201, got {r.status_code}"

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    @pytest.mark.parametrize('username', [' ', 'w'])
    def test_post_with_bad_username_with_record(self, api_client, username, mysql_worker):
        '''
        Тест на добавление пользователя с плохим логином (слишком коротким или пробелом)
        Проверяет на запись в базу - и падает, так как запись реально появляется (кстати, код 210 а не 400)
        '''
        api_client.add_user(username=username, email='random@mail.ru', password='12345678')
        count = mysql_worker.find_count_by_email('random@mail.ru')
        api_client.delete_user(username)
        assert count == 0, f"Expected 0 users in db with this username, {count} got"

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    @pytest.mark.parametrize('username', ['кирилл', 'w' * 30])
    def test_post_with_very_bad_username_without_record(self, api_client, username, mysql_worker):
        '''
        Тест на добавление пользователя с плохим логином, ломающим базу (юникодным или очень длинным)
        Идет проверка на добавление в базу (проверка проходит)
        Но  также смотрится код возврата и он 210 вместо 400
        '''
        r = api_client.add_user(username=username, email='random@mail.ru', password='12345678')
        count = mysql_worker.find_count_by_email('random@mail.ru')
        status_code = r.status_code
        api_client.delete_user(username)
        assert count == 0, f"Expected 0 users in db with this username, {count} got"
        assert status_code == 400, f"Expected code 400, got {status_code}"

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    @pytest.mark.parametrize('email', ['a@b.c', '@', ''])
    def test_post_with_bad_email_with_record(self, api_client, email, mysql_worker):
        '''
        Тест на добавление пользователя с плохой почтой - плохой шаблон или пустая
        ПРоверяет на запись в базу - и падает, так как запись реально появляется
        '''
        username = next(gen)
        api_client.add_user(username=username, email=email, password='12345678')
        count = mysql_worker.find_count_by_name(username)
        api_client.delete_user(username)
        assert count == 0, f"Expected 0 users in db with this username, {count} got"

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    @pytest.mark.parametrize('email', ['кирилл@мэйл.ру', 'w' * 70 + '@mail.ru'])
    def test_post_with_very_bad_email_without_record(self, api_client, email, mysql_worker):
        '''
        Тест на добавление пользователя с плохой почтой - длинная или юникодная
        ПРоверяет на запись в базу и проходит, так как записи не появилось
        Но статус код не 400 а 210
        '''
        username = next(gen)
        r = api_client.add_user(username=username, email=email, password='12345678')
        count = mysql_worker.find_count_by_name(username)
        status_code = r.status_code
        api_client.delete_user(username)
        assert count == 0, f"Expected 0 users in db with this username, {count} got"
        assert status_code == 400, f"Expected code 400, got {status_code}"

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    @pytest.mark.parametrize('password', ['a', ' ', ''])
    def test_post_with_bad_password_with_record(self, api_client, mysql_worker, password):
        '''
        Тест на добавление пользователя с плохим паролем - короткий, из пробела, пустой
         ПРоверяет на запись в базу - и падает, так как запись реально появляется
        '''
        username = next(gen)
        api_client.add_user(username=username, email=f'{username}@mail.ru',
                            password=password)
        count = mysql_worker.find_count_by_name(username)
        api_client.delete_user(username)
        assert count == 0, f"Expected 0 users in db with this username, {count} got"

    @pytest.mark.CRITICAL_BUGS
    @allure.feature('api tests on post method')
    @pytest.mark.parametrize('password', ['парольчик', 'w_long'])
    def test_post_with_very_bad_password_without_record(self, api_client, mysql_worker, password):
        '''
        Тест на добавление пользователя с плохим паролем - юникодный, длинный
        ПРоверяет на запись в базу и проходит, так как записи не появилось
        Но статус код не 400 а 210
        '''
        username = next(gen)
        if password == 'w_long':  # костыль для логгера
            password = 'w' * 300
        r = api_client.add_user(username=username, email=f'{username}@mail.ru',
                                password=password)
        count = mysql_worker.find_count_by_name(username)
        status_code = r.status_code
        api_client.delete_user(username)
        assert count == 0, f"Expected 0 users in db with this username, {count} got"
        assert status_code == 400, f"Expected code 400, got {status_code}"

    @pytest.mark.API
    @allure.feature('api tests on post method')
    def test_post_with_short_name(self, api_client, mysql_worker):
        '''
        Тест на добавление пользователя с логином ,<6 символов
        В отличие от ui хотя бы регистируется в базе, на что идет проверка
        '''
        username = 'api'
        r = api_client.add_user(username=username, email=f'{username}@mail.ru',
                                password='12345678')
        count = mysql_worker.find_count_by_name(username)
        api_client.delete_user(username)
        assert count == 1

    @pytest.mark.STRANGE_BUGS
    @allure.feature('api tests on post method')
    def test_use_user_with_little_name(self, api_client, logger_api):
        '''
        Тест на каки-нибудь действия пользователя с логином <6 символов
        апи клиент создает такого пользователя, после чего этот пользователь пытается заблокировать апи клиента
        Ожидается что это получится (код 200), однако на самом деле будет код 401
        По итогам, как и в ui с таким коротким логином ничего нельзя сделать
        '''
        username = 'api2'
        r = api_client.add_user(username=username, email=f'{username}@mail.ru',
                                password='12345678')
        new_user_with_little_name = Client(username, '12345678', f'{username}@mail.ru', logger_api)
        r = new_user_with_little_name.block_user(api_client.username)
        api_client.delete_user(username)
        assert r.status_code == 200, f"Expected code 200, got {r.status_code}"

    @pytest.mark.API
    @allure.feature('api tests on delete method')
    def test_delete_existing_user(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на удаление другого существующего пользователя
        Возвращает 204, как и ожидалось
        Также проверяет, что в базе была одна запись по удаляемому имени, а стало 0
        '''
        assert mysql_worker.find_count_by_name(tmp_user[0]) == 1
        r = api_client.delete_user(tmp_user[0])
        assert r.status_code == 204
        assert mysql_worker.find_count_by_name(tmp_user[0]) == 0

    @pytest.mark.API
    @allure.feature('api tests on delete method')
    def test_delete_not_existing_user(self, api_client):
        '''
        Тест на удаление самого себя
        АПи клиент создает пользователя, который удаляет сам себя
        Идет проверка, что до удаления была 1 запись в бд, помле удаления их нет
        Также проверяет, что статус-код 204
        '''
        r = api_client.delete_user('abacaba')
        assert r.status_code == 404

    @pytest.mark.API
    @allure.feature('api tests on delete method')
    def test_delete_self_user(self, api_client, mysql_worker, logger_api):
        '''
        Тест на удаление несуществующего пользователя
        Возвращает 404, как и ожидалось
        '''
        username = next(gen)
        r = api_client.add_user(username=username, email=f'{username}@mail.ru',
                                password='12345678')
        new_user_for_deleting_himself = Client(username, '12345678', f'{username}@mail.ru', logger_api)
        assert mysql_worker.find_count_by_name(username) == 1
        r = new_user_for_deleting_himself.delete_user(username)
        assert r.status_code == 204
        assert mysql_worker.find_count_by_name(username) == 0

    @pytest.mark.API
    @allure.feature('api tests on block method')
    def test_block_self_user(self, api_client, mysql_worker):
        '''
        Тест на блокировку самого себя и  дальнейшую попытку разблокироваться или сделать что-то еще
        1. проверяем, что у апи клиента доступ 1
        2. апи клиент сам себя блокирует
        3. ПРоверяем что код 200 и доступ в базк поменялся на 0
        4. Пытаемся заблокироваться
        5. Получаем код 401 и неизменеившийся доступ 0
        6. Пытаемся добавить нового пользователя
        7. смотри 5 пункт
        '''
        assert mysql_worker.get_access_status_by_name(api_client.username) == 1

        r = api_client.block_user(api_client.username)
        assert r.status_code == 200
        assert mysql_worker.get_access_status_by_name(api_client.username) == 0

        r = api_client.accept_user(api_client.username)
        assert r.status_code == 401
        assert mysql_worker.get_access_status_by_name(api_client.username) == 0

        r = api_client.add_user(username='somebody', email='somebody@mail.ru', password='1234567')
        assert r.status_code == 401
        assert mysql_worker.get_access_status_by_name(api_client.username) == 0

    @pytest.mark.API
    @allure.feature('api tests on block method')
    def test_block_existing_active_user(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на блокировку существующего незаблокированного пользователя
        Проверяет, что доступ сменился с 1 на 0 и статус код 200
        '''
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 1
        r = api_client.block_user(tmp_user[0])
        assert r.status_code == 200
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 0

    @pytest.mark.API
    @allure.feature('api tests on block method')
    def test_block_existing_blocked_user(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на блокировку существующего уже заблокированного пользователя
        Проверяет, что код доступа после блокировки так и остается 0
        а статус код запроса 304
        '''
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 1
        api_client.block_user(tmp_user[0])
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 0
        r = api_client.block_user(tmp_user[0])
        assert r.status_code == 304
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 0

    @pytest.mark.API
    @allure.feature('api tests on block method')
    def test_block_not_existing_user(self, api_client):
        '''
        Тест на блокировку несуществующего пользователя
        Возвращает 404, как и ожидалось
        '''
        r = api_client.block_user('abacaba')
        assert r.status_code == 404

    @pytest.mark.API
    @allure.feature('api tests on accept method')
    def test_accept_existing_blocked_user(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на разблокировку существующего заблокированного пользователя
        Проверяет, что код доступа сменился с 0 на 1 и ствтус код 200
        '''
        api_client.block_user(tmp_user[0])
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 0
        r = api_client.accept_user(tmp_user[0])
        assert r.status_code == 200
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 1

    @pytest.mark.API
    @allure.feature('api tests on accept method')
    def test_accept_existing_not_blocked_user(self, api_client, tmp_user, mysql_worker):
        '''
        Тест на разблокировку существующего незаблокированного пользователя
        Проверяет, что код доступа как был 1, так и остался и код доступа 304
        '''
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 1
        r = api_client.accept_user(tmp_user[0])
        assert r.status_code == 304
        assert mysql_worker.get_access_status_by_name(tmp_user[0]) == 1

    @pytest.mark.API
    @allure.feature('api tests on accept method')
    def test_accept_not_existing_blocked_user(self, api_client):
        '''
        Тест на разблокировку несуществующего пользователя
        Возвращает 404, как и ожидалось
        '''
        r = api_client.accept_user('abacaba')
        assert r.status_code == 404

    @pytest.mark.API
    @allure.feature('api-way tests on registration')
    def test_registration_in_api_way_good(self, api_client, mysql_worker):
        '''
        Тест на регистрацию через http запрос (не api из тз !!!) нового пользователя
        с валидными и несуществующими в базе логином и мейлом
        Формируется специальный словарь установленной формы ( посмотрел в devtools -> Network) c нормальными полями,
        после чего через библиотеку requests осуществляется post запрос
        Ждет статус код 200, его и получает
        Также идет проверка, что соответствующая запись появилаь  в бд
        '''
        username = next(gen)
        data = {
            'username': username,
            'email': f'{username}@mail.ru',
            'password': '12345678',
            'confirm': '12345678',
            'term': 'y',
            'submit': 'Register'
        }
        r = requests.post('http://0.0.0.0:7000/reg', data=data)
        count = mysql_worker.find_count_by_name(username)
        api_client.delete_user(username)
        assert r.status_code == 200
        assert count == 1

    @pytest.mark.STRANGE_BUGS
    @allure.feature('api-way tests on registration')
    def test_registration_in_api_way_existing_username(self, api_client, logger_api):
        '''
        Тест на регистрацию через http запрос (не api из тз !!!) пользователя с логином, который уже есть в базе
        Формируется специальный словарь установленной формы c заведомо существующим логином (логином api клиента)
        Ждет статус код 304, но получает 409.
        Можно расценить как баг, если учитывать, что инструкция из тз распространяется и на такие http запросы тоже, а не только на API
        '''
        username = api_client.username
        email = f'{next(gen)}@mail.ru'
        data = {
            'username': username,
            'email': email,
            'password': '12345678',
            'confirm': '12345678',
            'term': 'y',
            'submit': 'Register'
        }
        url = 'http://0.0.0.0:7000/reg'
        logger_api.info('Performing request(api_way):')
        logger_api.info(f'URL: {url}')
        logger_api.info(f'BODY: {data}')
        logger_api.info('-' * 20 + '\n')

        r = requests.post(url, data=data)

        logger_api.info('Got response(api_way):')
        logger_api.info(f'Status code: {r.status_code}')
        logger_api.info(f'Content: {r.text}')
        logger_api.info('-' * 50 + '\n')

        assert r.status_code == 304, f"Expected code 304, got {r.status_code}"

    @pytest.mark.STRANGE_BUGS
    @allure.feature('api-way tests on registration')
    def test_registration_in_api_way_existing_email(self, api_client, logger_api):
        '''
        Тест на регистрацию через http запрос (не api из тз!!!) пользователя с мейлом, который уже есть в базе
        Формируется специальный словарь установленной формы c заведомо существующим мейлом (мейлом api клиента)
        Ждет статус код 304, но получает 500
        Можно расценить как баг, если учитывать, что инструкция из тз распространяется и на такие http запросы тоже, а не только на API
        '''
        username = next(gen)
        email = api_client.email
        data = {
            'username': username,
            'email': email,
            'password': '12345678',
            'confirm': '12345678',
            'term': 'y',
            'submit': 'Register'
        }
        url = 'http://0.0.0.0:7000/reg'
        logger_api.info('Performing request(api_way):')
        logger_api.info(f'URL: {url}')
        logger_api.info(f'BODY: {data}')
        logger_api.info('-' * 20 + '\n')

        r = requests.post('http://0.0.0.0:7000/reg', data=data)

        logger_api.info('Got response(api_way):')
        logger_api.info(f'Status code: {r.status_code}')
        logger_api.info(f'Content: {r.text}')
        logger_api.info('-' * 50 + '\n')

        api_client.delete_user(username)
        assert r.status_code == 304, f"Expected code 304, got {r.status_code}"

    @pytest.mark.API
    @allure.feature('api-way tests on registration')
    def test_registration_in_api_way_long_email(self, api_client, mysql_worker):
        '''
        Тест на регистрацию через http запрос (не api из тз !!!) нового пользователя,пользователя с длинным мейлом
        Формируется специальный словарь установленной формы c мейлом длины > 64
        Ждет статус код 400, его и получает
        Также идет в базу посмотреть, что записи нет
        '''
        username = next(gen)
        email = 'a' * 100 + '@mail.ru'
        data = {
            'username': username,
            'email': email,
            'password': '12345678',
            'confirm': '12345678',
            'term': 'y',
            'submit': 'Register'
        }
        r = requests.post('http://0.0.0.0:7000/reg', data=data)
        count = mysql_worker.find_count_by_name(username)
        api_client.delete_user(username)
        assert r.status_code == 400
        assert count == 0

    @pytest.mark.STRANGE_BUGS
    @allure.feature('api-way tests on registration')
    @pytest.mark.parametrize('password', ['парольчик', 'w_long'])
    def test_registration_in_api_way_bad_password(self, api_client, mysql_worker, logger_api, password):
        '''
        Тест на регистрацию через http запрос (не api из тз!!!) нового пользователя с паролем > 256 симвлов
        Формируется специальный словарь установленной формы c очень длинным паролем
        Идет в базу посмотреть, что такой записи нет
        Ждет статус код 400, но получает 500
        Можно расценить как баг, если учитывать, что инструкция из тз распространяется и на такие http запросы тоже, а не только на API
        '''
        username = next(gen)
        email = f'{username}@mail.ru'
        if password == "w_long":
            password = 'w'*300
        data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm': password,
            'term': 'y',
            'submit': 'Register'
        }
        url = 'http://0.0.0.0:7000/reg'
        logger_api.info('Performing request(api_way):')
        logger_api.info(f'URL: {url}')
        logger_api.info(f'BODY: {data}')
        logger_api.info('-' * 20 + '\n')

        r = requests.post('http://0.0.0.0:7000/reg', data=data)

        logger_api.info('Got response(api_way):')
        logger_api.info(f'Status code: {r.status_code}')
        logger_api.info(f'Content: {r.text}')
        logger_api.info('-' * 60 + '\n')

        count = mysql_worker.find_count_by_name(username)
        api_client.delete_user(username)
        assert count == 0
        assert r.status_code == 400, f"Expected code 400, got {r.status_code}"
