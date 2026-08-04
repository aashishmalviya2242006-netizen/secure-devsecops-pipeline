from unittest.mock import AsyncMock, patch

import pytest

from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.mark.asyncio
@patch("app.services.user_service.send_notification", new_callable=AsyncMock)
@patch("app.services.user_service.send_log", new_callable=AsyncMock)
async def test_create_user(mock_send_log, mock_send_notification):

    service = UserService()

    user = await service.create_user(
        UserCreate(
            name="Aashish",
            email="aashish@gmail.com"
        )
    )

    assert user.id == 1
    assert user.name == "Aashish"
    assert user.email == "aashish@gmail.com"

    mock_send_log.assert_awaited_once()
    mock_send_notification.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.user_service.send_notification", new_callable=AsyncMock)
@patch("app.services.user_service.send_log", new_callable=AsyncMock)
async def test_get_user(mock_send_log, mock_send_notification):

    service = UserService()

    created = await service.create_user(
        UserCreate(
            name="John",
            email="john@example.com"
        )
    )

    user = service.get_user(created.id)

    assert user is not None
    assert user.name == "John"


@pytest.mark.asyncio
@patch("app.services.user_service.send_notification", new_callable=AsyncMock)
@patch("app.services.user_service.send_log", new_callable=AsyncMock)
async def test_update_user(mock_send_log, mock_send_notification):

    service = UserService()

    created = await service.create_user(
        UserCreate(
            name="John",
            email="john@example.com"
        )
    )

    updated = service.update_user(
        created.id,
        UserUpdate(name="Johnny")
    )

    assert updated is not None
    assert updated.name == "Johnny"


@pytest.mark.asyncio
@patch("app.services.user_service.send_notification", new_callable=AsyncMock)
@patch("app.services.user_service.send_log", new_callable=AsyncMock)
async def test_delete_user(mock_send_log, mock_send_notification):

    service = UserService()

    created = await service.create_user(
        UserCreate(
            name="John",
            email="john@example.com"
        )
    )

    deleted = service.delete_user(created.id)

    assert deleted is True
    assert service.get_user(created.id) is None
