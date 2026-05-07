import allure
from helpers import generate_user_data, register_user, login_user, delete_user


class TestLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self):
        user_data = generate_user_data()
        register_user(user_data)
        response = login_user({"email": user_data["email"], "password": user_data["password"]})
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == user_data["email"]
        assert "accessToken" in body
        assert "refreshToken" in body
        delete_user(body["accessToken"])

    @allure.title("Логин с неверным логином и паролем")
    def test_login_wrong_credentials(self):
        response = login_user({"email": "wrong@test.com", "password": "wrongpass"})
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"