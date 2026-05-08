import allure
from helpers import generate_user_data
from api import UserApi
from data import MSG_WRONG_CREDENTIALS


class TestLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self):
        user_data = generate_user_data()
        UserApi.register(user_data)
        response = UserApi.login({"email": user_data["email"], "password": user_data["password"]})
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == user_data["email"]
        assert "accessToken" in body
        assert "refreshToken" in body
        UserApi.delete(body["accessToken"])

    @allure.title("Логин с неверным логином и паролем")
    def test_login_wrong_credentials(self):
        response = UserApi.login({"email": "wrong@test.com", "password": "wrongpass"})
        assert response.status_code == 401
        assert response.json()["message"] == MSG_WRONG_CREDENTIALS