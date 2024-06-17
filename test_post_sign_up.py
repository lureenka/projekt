import pytest
from api.post_sign_up import SignUp
from api.data.register import RegisterRequestDto
from dotenv import load_dotenv
from generators.user_generator import get_random_user

load_dotenv()


@pytest.fixture
def sign_up_api():
    return SignUp()


def get_random_user():
    return RegisterRequestDto(username="random_user", password="random_password")


def test_return_200_api_signup(sign_up_api):
    user = get_random_user()
    response = sign_up_api.api_call(user)

    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("token") is not None, "Token should not be None"


def test_return_400_api_signup(sign_up_api):
    user = RegisterRequestDto(username="abc", password="abc")  # Invalid user data
    response = sign_up_api.api_call(user)

    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Bad Request", "Expected error message"


def test_return_422_api_signup(sign_up_api):
    user = RegisterRequestDto(username="existing_user",
                              password="weakpassword")  # Assume this user already exists or weak password
    response = sign_up_api.api_call(user)

    assert response.status_code == 422, "Expected status code 422"
    assert response.json().get("error") == "Unprocessable Entity", "Expected error message"
