import requests
from data import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, DELETE_USER_ENDPOINT, INGREDIENTS_ENDPOINT, ORDERS_ENDPOINT


class UserApi:
    @staticmethod
    def register(data):
        return requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=data)

    @staticmethod
    def login(data):
        return requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=data)

    @staticmethod
    def delete(token):
        requests.delete(f"{BASE_URL}{DELETE_USER_ENDPOINT}", headers={"Authorization": token})


class OrderApi:
    @staticmethod
    def get_ingredients():
        return requests.get(f"{BASE_URL}{INGREDIENTS_ENDPOINT}")

    @staticmethod
    def create(token, ingredients):
        return requests.post(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            headers={"Authorization": token},
            json={"ingredients": ingredients}
        )

    @staticmethod
    def create_without_auth(ingredients):
        return requests.post(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            json={"ingredients": ingredients}
        )