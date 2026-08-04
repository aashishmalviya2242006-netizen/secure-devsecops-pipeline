from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "gateway-service",
    }


@patch("app.routes.gateway.forward_request", new_callable=AsyncMock)
def test_get_forward(mock_forward):

    mock_forward.return_value = httpx.Response(
        status_code=200,
        json={
            "message": "success"
        }
    )

    response = client.get("/user/users")

    assert response.status_code == 200
    assert response.json() == {
        "message": "success"
    }

    mock_forward.assert_called_once()


@patch("app.routes.gateway.forward_request", new_callable=AsyncMock)
def test_post_forward(mock_forward):

    mock_forward.return_value = httpx.Response(
        status_code=201,
        json={
            "created": True
        }
    )

    response = client.post(
        "/user/users",
        json={
            "name": "Aashish",
            "email": "aashish@gmail.com"
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "created": True
    }

    mock_forward.assert_called_once()


@patch("app.routes.gateway.forward_request", new_callable=AsyncMock)
def test_unknown_service(mock_forward):

    mock_forward.return_value = None

    response = client.get("/unknown/test")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Service not found."
    }

    mock_forward.assert_called_once()
