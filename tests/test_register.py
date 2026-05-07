import allure
import pytest
from helpers import generate_user_data, register_user, delete_user


class TestRegister:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()
        response = register_user(user_data)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == user_data["email"]
        assert body["user"]["name"] == user_data["name"]
        assert "accessToken" in body
        assert "refreshToken" in body
        delete_user(body["accessToken"])

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        user_data = generate_user_data()
        register_response = register_user(user_data)
        token = register_response.json()["accessToken"]
        response = register_user(user_data)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"
        delete_user(token)

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, field):
        user_data = generate_user_data()
        del user_data[field]
        response = register_user(user_data)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"