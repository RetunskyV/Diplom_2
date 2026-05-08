import allure
import pytest
from helpers import generate_user_data
from api import UserApi
from data import MSG_USER_EXISTS, MSG_REQUIRED_FIELDS


class TestRegister:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()
        response = UserApi.register(user_data)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == user_data["email"]
        assert body["user"]["name"] == user_data["name"]
        assert "accessToken" in body
        assert "refreshToken" in body
        UserApi.delete(body["accessToken"])

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        user_data = generate_user_data()
        register_response = UserApi.register(user_data)
        token = register_response.json()["accessToken"]
        response = UserApi.register(user_data)
        assert response.status_code == 403
        assert response.json()["message"] == MSG_USER_EXISTS
        UserApi.delete(token)

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, field):
        user_data = generate_user_data()
        del user_data[field]
        response = UserApi.register(user_data)
        assert response.status_code == 403
        assert response.json()["message"] == MSG_REQUIRED_FIELDS