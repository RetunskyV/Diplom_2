import random
import string


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_user_data():
    return {
        "email": f"{generate_random_string()}_{generate_random_string()}@test.com",
        "password": generate_random_string(10),
        "name": generate_random_string(6)
    }