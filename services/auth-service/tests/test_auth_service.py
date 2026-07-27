from app.services.auth_service import AuthService
from app.schemas import RegisterRequest


def test_register_success():
    service = AuthService()

    user = RegisterRequest(
        name="Aashish",
        email="aashish@gmail.com",
        password="admin123"
    )

    registered_user = service.register(user)

    assert registered_user is not None
    assert registered_user["id"] == 1
    assert registered_user["name"] == "Aashish"
    assert registered_user["email"] == "aashish@gmail.com"


def test_register_duplicate_email():
    service = AuthService()

    user = RegisterRequest(
        name="Aashish",
        email="aashish@gmail.com",
        password="admin123"
    )

    first_user = service.register(user)
    second_user = service.register(user)

    assert first_user is not None
    assert second_user is None


def test_get_user_by_email():
    service = AuthService()

    user = RegisterRequest(
        name="Aashish",
        email="aashish@gmail.com",
        password="admin123"
    )

    service.register(user)

    found_user = service.get_user_by_email("aashish@gmail.com")

    assert found_user is not None
    assert found_user["id"] == 1
    assert found_user["name"] == "Aashish"
    assert found_user["email"] == "aashish@gmail.com"


def test_get_user_by_email_not_found():
    service = AuthService()

    found_user = service.get_user_by_email("unknown@gmail.com")

    assert found_user is None

def test_get_user_by_id():
    service = AuthService()

    user = RegisterRequest(
        name="Aashish",
        email="aashish@gmail.com",
        password="admin123"
    )

    service.register(user)

    found_user = service.get_user_by_id(1)

    assert found_user is not None
    assert found_user["id"] == 1
    assert found_user["name"] == "Aashish"
    assert found_user["email"] == "aashish@gmail.com"

def test_get_user_by_id_not_found():
    service = AuthService()

    found_user = service.get_user_by_id(100)

    assert found_user is None


def test_authenticate_user_success():
    service = AuthService()

    user = RegisterRequest(
        name="Aashish",
        email="aashish@gmail.com",
        password="admin123"
    )

    service.register(user)

    token = service.authenticate_user(
        "aashish@gmail.com",
        "admin123"
    )

    assert token is not None
    assert isinstance(token, dict)
    assert "access_token" in token
    assert "token_type" in token
    assert token["token_type"] == "bearer"
    assert isinstance(token["access_token"], str)

def test_authenticate_user_wrong_password():
    service = AuthService()

    user = RegisterRequest(
        name="Aashish",
        email="aashish@gmail.com",
        password="admin123"
    )

    service.register(user)

    token = service.authenticate_user(
        "aashish@gmail.com",
        "wrongpassword"
    )

    assert token is None


def test_authenticate_user_non_existing_email():
    service = AuthService()

    token = service.authenticate_user(
        "unknown@gmail.com",
        "admin123"
    )

    assert token is None
