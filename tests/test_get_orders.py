import allure
from helpers import generate_user_data, register_user, delete_user, get_ingredients
import requests

BASE_URL = "https://stellarburgers.education-services.ru/api"


class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self):
        user_data = generate_user_data()
        reg_response = register_user(user_data)
        token = reg_response.json()["accessToken"]
        response = requests.get(f"{BASE_URL}/orders",
                                headers={"Authorization": token})
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert "total" in body
        assert "totalToday" in body
        delete_user(token)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"