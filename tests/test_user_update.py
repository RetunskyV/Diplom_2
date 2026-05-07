import allure
from helpers import generate_user_data, register_user, delete_user, generate_random_string
import requests

BASE_URL = "https://stellarburgers.education-services.ru/api"


class TestUserUpdate:

    @allure.title("Изменение данных авторизованного пользователя — email")
    def test_update_authorized_email(self):
        user_data = generate_user_data()
        reg_response = register_user(user_data)
        token = reg_response.json()["accessToken"]
        new_email = f"new_{generate_random_string()}@test.com"
        response = requests.patch(f"{BASE_URL}/auth/user",
                                  headers={"Authorization": token},
                                  json={"email": new_email})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == new_email
        delete_user(token)

    @allure.title("Изменение данных авторизованного пользователя — name")
    def test_update_authorized_name(self):
        user_data = generate_user_data()
        reg_response = register_user(user_data)
        token = reg_response.json()["accessToken"]
        new_name = f"new_{generate_random_string()}"
        response = requests.patch(f"{BASE_URL}/auth/user",
                                  headers={"Authorization": token},
                                  json={"name": new_name})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == new_name
        delete_user(token)

    @allure.title("Изменение данных неавторизованного пользователя")
    def test_update_unauthorized(self):
        new_name = f"new_{generate_random_string()}"
        response = requests.patch(f"{BASE_URL}/auth/user",
                                  json={"name": new_name})
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"