import requests
import pytest
import allure

BASE_URL = "https://api.kinopoisk.dev/"
API_TOKEN = "EHDZWQ6-QVVMWRT-NDZTR03-77VM0K2"


@allure.feature('Позитивные кейсы')
@allure.story('Поиск фильмов по id')
def test_movie_search_by_id():
    movie_id = "535341"
    url = f"{BASE_URL}/v1.4/movie/{movie_id}"
    headers = {
        "X-API-KEY": API_TOKEN
    }

    with allure.step("Выполняем GET запрос на поиск фильма по ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверяем статус ответа"):
        assert response.status_code == 200, "Ожидаемый статус ответа 200"
        allure.attach(body=response.text, name='Response', attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем содержимое ответа"):
        data = response.json()
        assert 'id' in data and data['id'] == int(movie_id), "Идентификатор фильма должен совпадать"


@allure.feature("Позитивные кейсы")
@allure.story("Поиск по названию 'Джентльмены'")
def test_search_movie():
    with allure.step("Отправка запроса для поиска фильма"):
        url = f"{BASE_URL}v1.4/movie/search"
        headers = {
            "X-API-KEY": API_TOKEN
        }
        params = {
            "query": "Джентльмены"
        }

        response = requests.get(url, headers=headers, params=params)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Проверка содержимого ответа"):
        json_resp = response.json()
        assert "docs" in json_resp, "Response doesn’t have 'docs' key"


@allure.feature("Позитивные кейсы")
@allure.story("Получение случайного фильма")
@allure.title("Тест получения случайного фильма")
def test_get_random_movie():
    url = f"{BASE_URL}/v1.4/movie/random"
    headers = {
        "X-API-KEY": API_TOKEN
    }

    response = requests.get(url, headers=headers)

    with allure.step("Проверка кода состояния ответа"):
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    with allure.step("Проверка содержимого ответа"):
        json_response = response.json()
        assert "name" in json_response, "Response JSON does not contain 'name' key"


@allure.feature("Негативные кейсы")
@allure.story("Получение несуществующего фильма")
def test_non_existent_movie():
    url = f"{BASE_URL}/v1.4/movie/999999999999"
    headers = {
        "X-API-KEY": API_TOKEN
    }

    response = requests.get(url, headers=headers)

    with allure.step("Проверка статус кода"):
        assert response.status_code != 200, "Ожидаемый ответ не должен быть успешным для несуществующего фильма"


@pytest.fixture
def headers():
    return {
        "X-API-KEY": API_TOKEN
    }


@allure.feature("Негативные кейсы")
@allure.story("Получение фильма с неверным типом идентификатора")
def test_get_movie_with_invalid_id(headers):
    url = f"{BASE_URL}/v1.4/movie/abc"

    response = requests.get(url, headers=headers)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, "Ожидался статус-код 400"


@allure.feature("Негативные кейсы")
@allure.story("Получение фильма с отрицательным идентификатором")
def test_get_movie_with_negative_id():
    headers = {
        "X-API-KEY": API_TOKEN
    }

    url = f"{BASE_URL}/v1.4/movie/-1"

    response = requests.get(url, headers=headers)

    with allure.step("Отправка GET-запроса к API"):
        allure.attach(url, name="URL запроса")
        allure.attach(str(headers), name="Заголовки запроса")

    with allure.step("Ответ от API"):
        allure.attach(str(response.status_code), name="Код состояния")
        allure.attach(response.text, name="Тело ответа")

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, "Ожидался статус-код 400"


@allure.feature('Негативные кейсы')
@allure.story('Получение фильма с плавающим идентификатором')
def test_get_movie_by_id():
    url = f"{BASE_URL}/v1.4/movie/1.4"
    headers = {
        "X-API-KEY": API_TOKEN
    }

    response = requests.get(url, headers=headers)

    allure.attach(response.url, name='URL запроса', attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(response.status_code), name='Код состояния', attachment_type=allure.attachment_type.TEXT)
    allure.attach(response.text, name='Тело ответа', attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, "Ожидался статус-код 400"
