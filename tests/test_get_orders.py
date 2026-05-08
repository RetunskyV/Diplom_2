import allure
from helpers import generate_user_data
from api import UserApi
import requests
from data import BASE_URL, MSG_UNAUTHORISED


class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self):
        user_data = generate_user_data()
        reg_response = UserApi.register(user_data)
        token = reg_response.json()["accessToken"]
        response = requests.get(f"{BASE_URL}/orders",
                                headers={"Authorization": token})
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert "total" in body
        assert "totalToday" in body
        UserApi.delete(token)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        assert response.json()["message"] == MSG_UNAUTHORISED