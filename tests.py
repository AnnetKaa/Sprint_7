import requests
from faker import Faker
import pytest
import allure
fake = Faker()

class TestCreate:
    @allure.title('Проверка создания курьера')
    def test_check_create(self, login_user):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
        data = login_user
        response = requests.post(url, json=data)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверка повторного создания курьера')
    def test_check_not_create_twice(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
        data = {
            "login": "ninja1",
            "password": "1234",
            "firstName": "saske"
        }
        response = requests.post(url, json=data)
        assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.' and response.status_code == 409

    @allure.title('Проверка повторного создания курьера с другим паролем')
    def test_check_not_create_twice_with_other_password(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
        data = {
            "login": "ninja1",
            "password": "12345",
            "firstName": "saske123"
        }
        response = requests.post(url, json=data)
        assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.' and response.status_code == 409

    @allure.title('Проверка создания курьера без ввода данных')
    def test_check_without_field(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
        data = {
        }
        response = requests.post(url, json=data)

        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи' and response.status_code == 400

    @allure.title('Проверка создания курьера без логина')
    def test_check_no_login_field(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
        data = {
            "password": fake.password(),
            "firstName": fake.name()
        }
        response = requests.post(url, json=data)
        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи' and response.status_code == 400

    @allure.title('Проверка создания курьера без пароля')
    def test_check_no_password_field(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
        data = {
            "login": fake.name(),
            "firstName": fake.name()
        }
        response = requests.post(url, json=data)
        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи' and response.status_code == 400


class TestLogin:

    @allure.title('Проверка успешной авторизации курьера')
    def test_check_login(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
        data = {
            "login": "ninja1",
            "password": "1234"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 200 and '{"id":2340}' == response.text

    @allure.title('Проверка авторизации курьера с некорректным паролем')
    def test_check_incorrect_password(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
        data = {
            "login": "ninja1",
            "password": "1234000"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка авторизации курьера с некорректным логином')
    def test_check_incorrect_login(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
        data = {
            "login": "nja1",
            "password": "1234"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка авторизации курьера без логина')
    def test_check_no_login_field(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
        data = {
            "password": "1234"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'

    @allure.title('Проверка авторизации курьера с несуществующим логином')
    def test_check_non_existent_account(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
        data = {
            "login": "abracadabra",
            "password": "1234"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка авторизации курьера без пароля')
    def test_check_no_password_field(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
        data = {
            "login": "ninja1"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 400 and response.json()['message'] == 'Учетная запись не найдена'

class TestOrder:
    @allure.title('Проверка создания заказа')
    @pytest.mark.parametrize("data", [
        {
            "firstName": "John",
            "lastName": 'lastName',
            "address": 'address',
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-10-26",
            "comment": "I'm really looking forward to it",
            "color": ["BLACK"]
        },
        {
            "firstName": "Mike",
            "lastName": 'lastName',
            "address": 'address',
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-10-26",
            "comment": "I'm really looking forward to it",
            "color": ["GREY"]
        },
        {
            "firstName": "Alice",
            "lastName": 'lastName',
            "address": 'address',
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-10-26",
            "comment": "I'm really looking forward to it",
            "color": ["BLACK", "GREY"]
        },
        {
            "firstName": "Alice",
            "lastName": 'lastName',
            "address": 'address',
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-10-26",
            "comment": "I'm really looking forward to it",
            "color": []
        }
    ])
    def test_check_order(self, data):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/orders"
        response = requests.post(url, json=data)
        assert 'track' in response.json() and response.status_code == 201

        data_track = response.json()['track']
        cancel_order = f"https://qa-scooter.praktikum-services.ru/api/v1/orders/cancel"
        requests.post(cancel_order, json=data_track)

class TestOrderlist:
    @allure.title('Проверка получения списка заказов')
    def test_check_order_list(self):
            url = "https://qa-scooter.praktikum-services.ru/api/v1/orders"
            response = requests.get(url)
            assert "orders" in response.json() and isinstance(response.json()["orders"], list)

