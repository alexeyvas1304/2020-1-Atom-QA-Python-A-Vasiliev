from selenium.webdriver.common.by import By


class AuthPageLocators:
    USERNAME_FIELD = (By.ID, 'username')
    PASSWORD_FIELD = (By.ID, 'password')
    REGISTRATION_HREF = (By.CSS_SELECTOR, 'a')
    SUBMIT_BUTTON = (By.ID, 'submit')
    ERROR_MESSAGE_INVALID_USERNAME_OR_PASSWORD = (By.XPATH, '//div[contains(text(),"Invalid username or password")]')
    ERROR_MESSAGE_ONLY_AUTHORIZED_USERS = (
    By.XPATH, '//div[contains(text(),"This page is available only to authorized users")]')


class RegPageLocators:
    USERNAME_FIELD = (By.ID, 'username')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    CONFIRM_PASSWORD_FIELD = (By.ID, 'confirm')
    ACCEPT_CHECKBOX = (By.ID, 'term')
    SUBMIT_BUTTON = (By.ID, 'submit')

    ERROR_MESSAGE_USER_ALREADY_EXISTS = (By.XPATH, '//div[contains(text(),"User already exist")]')
    ERROR_MESSAGE_INTERNAL_SERVER_ERROR = (By.XPATH, '//div[contains(text(),"Internal Server Error")]')
    ERROR_MESSAGE_INCORRECT_USERNAME_LENGTH = (By.XPATH, '//div[contains(text(),"Incorrect username length")]')
    ERROR_MESSAGE_INCORRECT_EMAIL_LENGTH = (By.XPATH, '//div[contains(text(),"Incorrect email length")]')
    ERROR_MESSAGE_INVALID_EMAIL_ADDRESS = (By.XPATH, '//div[contains(text(),"Invalid email address")]')
    ERROR_MESSAGE_PASSWORDS_MUST_MATCH = (By.XPATH, '//div[contains(text(),"Passwords must match")]')
    ERROR_MESSAGE_MANY_PROBLEMS = (By.XPATH,
                                   '''//div[contains(text(),"{'email': ['Incorrect email length', 'Invalid email address'], 'password': ['Passwords must match']}")]''')


class MainPageLocators:
    SUCCESS_ACCESS_LOCATOR = (By.ID, 'login-controls')
    VK_ID_MARK = '//li[contains(text(),"VK ID: {}")]'

    API_CIRCLE = (By.XPATH, '//div[contains(text(),"What is an API")]/..//a')
    FUTURE_INTERNET_CIRCLE = (By.XPATH, '//div[contains(text(),"Future of internet")]/..//a')
    SMTP_CIRCLE = (By.XPATH, '//div[contains(text(),"SMTP")]/..//a')

    PYTHON_BUTTON = (By.XPATH, '//a[contains(text(),"HOME")]/../../li/a[contains(text(),"Python")]')
    LINUX_BUTTON = (By.XPATH, '//a[contains(text(),"Linux")]')
    NETWORK_BUTTON = (By.XPATH, '//a[contains(text(),"Network")]')
    HOME_BUTTON = (By.XPATH, '//a[contains(text(),"HOME")]')
    VERSION_BUTTON = (By.XPATH, '//a[contains(text(),"version")]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '#logout a')

    PYTHON_HISTORY_HREF = (By.XPATH, '//a[contains(text(),"Python history")]')
    FLASK_HREF = (By.XPATH, '//a[contains(text(),"About Flask")]')
    CENTOS_HREF = (By.XPATH, '//a[contains(text(),"Download Centos7")]')
    WIRESHARK_NEWS_HREF = (By.XPATH, '//a[contains(text(),"News")]')
    WIRESHARK_DOWNLOAD_HREF = (By.XPATH, '//li[contains(text(),"Wireshark")]/ul/li/a[contains(text(),"Download")]')
    TCPDUMP_EXAMPLES_HREF = (By.XPATH, '//a[contains(text(),"Examples")]')

    LOGGED_AS = (By.CSS_SELECTOR, '#login-name ul li:first-child')
    PYTHON_FACT = (By.CSS_SELECTOR, 'footer div  p:last-child')
