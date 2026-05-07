import allure
from helpers import generate_user_data, register_user, delete_user, get_ingredients
import requests

BASE_URL = "https://stellarburgers.education-services.ru/api"


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized_valid_ingredients(self):
        user_data = generate_user_data()
        reg_response = register_user(user_data)
        token = reg_response.json()["accessToken"]
        ingredients = get_ingredients().json()["data"]
        ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
        response = requests.post(f"{BASE_URL}/orders",
                                 headers={"Authorization": token},
                                 json={"ingredients": ingredient_ids})
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["order"]["number"] > 0
        delete_user(token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self):
        ingredients = get_ingredients().json()["data"]
        ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
        response = requests.post(f"{BASE_URL}/orders",
                                 json={"ingredients": ingredient_ids})
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        user_data = generate_user_data()
        reg_response = register_user(user_data)
        token = reg_response.json()["accessToken"]
        response = requests.post(f"{BASE_URL}/orders",
                                 headers={"Authorization": token},
                                 json={"ingredients": []})
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"
        delete_user(token)

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_hash(self):
        user_data = generate_user_data()
        reg_response = register_user(user_data)
        token = reg_response.json()["accessToken"]
        response = requests.post(f"{BASE_URL}/orders",
                                 headers={"Authorization": token},
                                 json={"ingredients": ["invalid_hash_123"]})
        assert response.status_code == 500
        delete_user(token)