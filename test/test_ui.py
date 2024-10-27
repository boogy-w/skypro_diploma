import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def setup_browser():
    driver = webdriver.Chrome()  # Инициализация веб-драйвера Chrome
    driver.implicitly_wait(10)  # Ожидание загрузки элементов
    yield driver
    driver.quit()


@allure.title("Проверка заголовка главной страницы")
@allure.description("Проверяем, что заголовок главной страницы отображается корректно")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Главная страница")
def test_homepage_title(setup_browser):
    driver = setup_browser
    with allure.step("Открываем главную страницу"):
        driver.get("https://www.kinopoisk.ru/")

    # Явное ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Попробуем несколько раз проверять заголовок, чтобы дать время человеческого вмешательства
    for attempt in range(3):
        with allure.step(f"Попытка {attempt+1}: Проверяем наличие и кликаем по 'Я не робот'"):
            captcha_elements = driver.find_elements(By.CLASS_NAME, "CheckboxCaptcha-Button")
            if captcha_elements:
                captcha_button = captcha_elements[0]
                captcha_button.click()

                # Явное ожидание завершения проверки CAPTCHA
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "CheckboxCaptcha-Button"))
                )
            else:
                break

    with allure.step("Проверяем заголовок страницы"):
        WebDriverWait(driver, 10).until(
            lambda driver: "Кинопоиск" in driver.title
        )
        assert "Кинопоиск" in driver.title, "Заголовок страницы не соответствует ожидаемому"


@allure.title("Проверка ссылок в шапке сайта по aria-label='presentation'")
@allure.description("Проверяем работоспособность всех ссылок с атрибутом aria-label='presentation' в шапке сайта")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Главная страница")
def test_header_links_presentation(setup_browser):
    driver = setup_browser

    with allure.step("Открываем главную страницу"):
        driver.get("https://www.kinopoisk.ru/")

    # Явное ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Обработка потенциальной CAPTCHA
    for attempt in range(3):
        with allure.step(f"Попытка {attempt + 1}: Проверяем наличие и кликаем по 'Я не робот'"):
            captcha_elements = driver.find_elements(By.CLASS_NAME, "CheckboxCaptcha-Button")
            if captcha_elements:
                captcha_button = captcha_elements[0]
                captcha_button.click()

                # Явное ожидание завершения проверки CAPTCHA
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "CheckboxCaptcha-Button"))
                )
            else:
                break

    with allure.step("Ищем ссылки в шапке сайта с aria-label='presentation'"):
        header_links = driver.find_elements(By.XPATH, "//header//a[@aria-label='presentation']")

    with allure.step("Проверяем каждую ссылку"):
        original_window = driver.current_window_handle
        for index, link in enumerate(header_links):
            with allure.step(f"Кликаем по ссылке {index + 1} и проверяем переход"):
                # Запоминаем текущий URL
                current_url = driver.current_url

                # Кликаем по ссылке
                link.click()

                # Даем время браузеру завершить переход
                WebDriverWait(driver, 10).until(
                    lambda d: len(d.window_handles) > 1 or d.current_url != current_url
                )

                if len(driver.window_handles) > 1:
                    # Если открылась новая вкладка, переключаемся на нее
                    new_window = [window for window in driver.window_handles if window != original_window][0]
                    driver.switch_to.window(new_window)

                    # Проверяем, что страница действительно загрузилась
                    assert "Error" not in driver.title, f"Ошибка: Заголовок страницы в новой вкладке содержит 'Error'"

                    # Закрываем новую вкладку и возвращаемся обратно
                    driver.close()
                    driver.switch_to.window(original_window)
                else:
                    # Проверяем, что URL изменился
                    assert driver.current_url != current_url, "Ошибка: Переход по ссылке не изменил URL страницы"


@allure.title("Проверка работоспособности формы входа")
@allure.description("Проверяем наличие и работоспособность формы входа")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Авторизация и регистрация")
def test_login_form(setup_browser):
    driver = setup_browser
    with allure.step("Открываем главную страницу"):
        driver.get("https://www.kinopoisk.ru/")
    # Явное ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Обработка потенциальной CAPTCHA
    for attempt in range(3):
        with allure.step(f"Попытка {attempt + 1}: Проверяем наличие и кликаем по 'Я не робот'"):
            captcha_elements = driver.find_elements(By.CLASS_NAME, "CheckboxCaptcha-Button")
            if captcha_elements:
                captcha_button = captcha_elements[0]
                captcha_button.click()

                # Явное ожидание завершения проверки CAPTCHA
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "CheckboxCaptcha-Button"))
                )
            else:
                break

    with allure.step("Кликаем на кнопку входа"):
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
        login_button.click()
    with allure.step("Проверяем наличие формы входа"):
        login_form = driver.find_elements(By.ID, "passp-field-login")
        assert len(login_form) > 0


@allure.title("Проверка поиска на главной странице")
@allure.description("Проверяем поле поиска и корректность работы автоподстановки")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Стандартный поиск")
def test_search_functionality(setup_browser):
    driver = setup_browser
    with allure.step("Открываем главную страницу"):
        driver.get("https://www.kinopoisk.ru/")
    # Явное ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Обработка потенциальной CAPTCHA
    for attempt in range(3):
        with allure.step(f"Попытка {attempt + 1}: Проверяем наличие и кликаем по 'Я не робот'"):
            captcha_elements = driver.find_elements(By.CLASS_NAME, "CheckboxCaptcha-Button")
            if captcha_elements:
                captcha_button = captcha_elements[0]
                captcha_button.click()

                # Явное ожидание завершения проверки CAPTCHA
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "CheckboxCaptcha-Button"))
                )
            else:
                break

    with allure.step("Находим поле поиска"):
        search_field = driver.find_element(By.NAME, "kp_query")
    with allure.step("Вводим поисковый запрос"):
        search_field.send_keys("Интерстеллар")
    with allure.step("Проверяем автоподстановку"):
        auto_suggestions = driver.find_elements(By.ID, "suggest-item-film-258687")
        assert len(auto_suggestions) > 0, "Автоподстановка не работает"


@allure.title("Проверка фильтрации по странам на главной странице")
@allure.description("Проверяем фильтр по странам и его применение к результатам поиска")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Расширенный поиск и фильтрация")
def test_genre_filter(setup_browser):
    driver = setup_browser
    with allure.step("Открываем главную страницу"):
        driver.get("https://www.kinopoisk.ru/")
    # Явное ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Обработка потенциальной CAPTCHA
    for attempt in range(3):
        with allure.step(f"Попытка {attempt + 1}: Проверяем наличие и кликаем по 'Я не робот'"):
            captcha_elements = driver.find_elements(By.CLASS_NAME, "CheckboxCaptcha-Button")
            if captcha_elements:
                captcha_button = captcha_elements[0]
                captcha_button.click()

                # Явное ожидание завершения проверки CAPTCHA
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "CheckboxCaptcha-Button"))
                )
            else:
                break

    with allure.step("Выбираем фильтр по странам"):
        filter_button = driver.find_element(By.XPATH, "//header//a[@aria-label='Расширенный поиск']")
        filter_button.click()
        genre_filter = driver.find_element(By.ID, "country")
        genre_filter.click()

    with allure.step("Проверяем наличие фильтров"):
        genres = driver.find_elements(By.ID, "country")
        assert len(genres) > 0, "Фильтры по жанрам не отображаются"
