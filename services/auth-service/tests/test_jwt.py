from app.core.jwt import (
    create_access_token,
    verify_access_token,
)


def test_create_access_token():
    payload = {
        "sub": "1",
        "email": "aashish@gmail.com"
    }

    token = create_access_token(payload)

    assert token is not None
    assert isinstance(token, str)


def test_verify_access_token():
    payload = {
        "sub": "1",
        "email": "aashish@gmail.com"
    }

    token = create_access_token(payload)

    decoded_payload = verify_access_token(token)

    assert decoded_payload is not None
    assert decoded_payload["sub"] == "1"
    assert decoded_payload["email"] == "aashish@gmail.com"


def test_verify_invalid_access_token():
    payload = verify_access_token("this_is_an_invalid_token")

    assert payload is None
