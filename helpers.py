import requests
import random
import string

BASE_URL = "https://stellarburgers.education-services.ru/api"


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_user_data():
    return {
        "email": f"{generate_random_string()}_{generate_random_string()}@test.com",
        "password": generate_random_string(10),
        "name": generate_random_string(6)
    }


def register_user(data):
    return requests.post(f"{BASE_URL}/auth/register", json=data)


def login_user(data):
    return requests.post(f"{BASE_URL}/auth/login", json=data)


def delete_user(token):
    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})


def get_ingredients():
    return requests.get(f"{BASE_URL}/ingredients")