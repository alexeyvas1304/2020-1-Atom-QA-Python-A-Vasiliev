from selenium.webdriver.common.by import By


class AuthPageLocators:
    ENTER_BUTTON = (By.XPATH, '//div[contains(text(),"Войти")]')
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    BAD_AUTHORIZATION_LOCATOR = (By.CLASS_NAME, 'formMsg_text')  # подстава с англом, на текст не натравляться
    RIGHT_AUTHORIZATION_LOCATOR = (By.CLASS_NAME, 'balance-panel')  # подстава, на блок из трех шагов не натравляться


class MainPageLocators:
    CREATE_FIRST_CAMPAIGN_HREF = (By.XPATH, '//a[contains(text(),"оздайте")]')  # лучше так
    CREATE_NOT_FIRST_CAMPAIGN_HREF = (By.XPATH, '//a/span[contains(text(),"Создать кампанию")]')
    TRAFIC_BUTTON = (By.XPATH, '// div[contains(text(), "Трафик")]')
    SITE_NAME_FIELD = (By.CSS_SELECTOR, '.input_create-main-url input')
    CAMPAIGN_NAME_FIELD = (By.CSS_SELECTOR, '.campaign-name input')
    BANNER_OPTION = (By.ID, '192')
    DOWNLOAD_IMAGE_BUTTON = (By.CSS_SELECTOR, '.form-element button')  # ???
    DOWNLOAD_IMAGE_INPUT = (By.CSS_SELECTOR, '.form-element input')
    SAVE_IMAGE = (By.CSS_SELECTOR, '.image-cropper__buttons-footer input')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '.footer .button_submit')
    CREATED_CAMPAIGN = '//a[contains(text(),"{}")]'

    CREATED_CAMPAIGN_CHECKBOX = '//a[contains(text(),"{}")]/../../../input'  # для подчистки
    ACTIONS = (By.XPATH, '//div[contains(text(),"Действия")]')
    DELETE_ACTION = (By.XPATH, '//span[contains(text(),"Удалить")]')

    GO_TO_SEGMENTS = (By.XPATH, '//a[contains(text(),"Аудитории")]')
    CREATE_FIRST_SEGMENT_HREF = (By.XPATH, '//a[contains(text(),"оздайте")]')  # лучше так
    CREATE_NOT_FIRST_SEGMENT_HREF = (By.XPATH, '//div [contains(text(),"оздать сегмент")]')
    SEGMENT_NAME = (By.CSS_SELECTOR, '.js-segment-name input')
    ADD_SEGMENT = (By.CLASS_NAME, 'create-segment-form__block')
    OK_MY_MIR = (By.XPATH, '//div[contains(text(),"Приложения (ОК и МойМир)")]')
    CHECKBOX = (By.CLASS_NAME, 'adding-segments-source__checkbox')
    ADD_SEGMENT_SUBMIT = (By.CSS_SELECTOR, '.adding-segments-modal__footer button')
    CREATE_SEGMENT_SUBMIT = (By.CSS_SELECTOR, '.create-segment-form button')
    CREATED_SEGMENT = '//a[contains(text(),"{}")]'

    DELETE_BUTTON = (By.CLASS_NAME, 'icon-cross')
    DELETE_CONFIRM_BUTTON = (By.CLASS_NAME, 'button_confirm-remove')
    CREATED_SEGMENT_DELETE_BUTTON = '//a[contains(text(),"{}")]/../..//span[@class="icon-cross"]'  # как бы попроще ?
    CREATED_SEGMENT_ID_FIELD = '//a[contains(text(),"{}")]/../../td/span[@class="adv-camp-cell adv-camp-cell_name"]'
