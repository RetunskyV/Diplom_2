import allure
from helpers import generate_user_data
from api import UserApi, OrderApi
from data import MSG_UNAUTHORISED, MSG_NO_INGREDIENTS


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized_valid_ingredients(self):
        user_data = generate_user_data()
        reg_response = UserApi.register(user_data)
        token = reg_response.json()["accessToken"]
        ingredients = OrderApi.get_ingredients().json()["data"]
        ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
        response = OrderApi.create(token, ingredient_ids)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["order"]["number"] > 0
        UserApi.delete(token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self):
        ingredients = OrderApi.get_ingredients().json()["data"]
        ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
        response = OrderApi.create_without_auth(ingredient_ids)
        assert response.status_code == 401
        assert response.json()["message"] == MSG_UNAUTHORISED

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        user_data = generate_user_data()
        reg_response = UserApi.register(user_data)
        token = reg_response.json()["accessToken"]
        response = OrderApi.create(token, [])
        assert response.status_code == 400
        assert response.json()["message"] == MSG_NO_INGREDIENTS
        UserApi.delete(token)

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_hash(self):
        user_data = generate_user_data()
        reg_response = UserApi.register(user_data)
        token = reg_response.json()["accessToken"]
        response = OrderApi.create(token, ["invalid_hash_123"])
        assert response.status_code == 500
        UserApi.delete(token)