import requests
from faker import Faker
import pytest
fake = Faker()

@pytest.fixture
def login_user():
    data = {
        "login": fake.name(),
        "password": fake.password(),
        "firstName": fake.name()
    }
    yield data
    login_url = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"
    login_data = {
        "login": data['login'],
        "password": data['password']
    }
    login_response = requests.post(login_url, json=login_data)
    id = login_response.json()['id']
    delete_url = f"https://qa-scooter.praktikum-services.ru/api/v1/courier/{id}"
    requests.delete(delete_url)
