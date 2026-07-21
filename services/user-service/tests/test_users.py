from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


def test_create_user():
    service = UserService()

    user = service.create_user(
        UserCreate(
            name="Aashish",
            email="aashish@gmail.com"
        )
    )

    assert user.id == 1
    assert user.name == "Aashish"
    assert user.email == "aashish@gmail.com"


def test_get_user():
    service = UserService()

    created = service.create_user(
        UserCreate(
            name="John",
            email="john@example.com"
        )
    )

    user = service.get_user(created.id)

    assert user is not None
    assert user.name == "John"


def test_update_user():
    service = UserService()

    created = service.create_user(
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


def test_delete_user():
    service = UserService()

    created = service.create_user(
        UserCreate(
            name="John",
            email="john@example.com"
        )
    )

    deleted = service.delete_user(created.id)

    assert deleted is True
    assert service.get_user(created.id) is None
