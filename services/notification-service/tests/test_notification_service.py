from app.schemas import NotificationCreate
from app.services.notification_service import NotificationService


def test_create_notification():

    service = NotificationService()

    notification = NotificationCreate(
        user_id=1,
        title="Welcome",
        message="Welcome to our application"
    )

    result = service.create_notification(notification)

    assert result["id"] == 1
    assert result["user_id"] == 1
    assert result["title"] == "Welcome"
    assert result["message"] == "Welcome to our application"
    assert result["is_read"] is False


def test_get_all_notifications():

    service = NotificationService()

    notification = NotificationCreate(
        user_id=1,
        title="Test",
        message="Testing"
    )

    service.create_notification(notification)

    result = service.get_all_notifications()

    assert len(result) == 1


def test_get_notification_by_id():

    service = NotificationService()

    notification = NotificationCreate(
        user_id=1,
        title="Hello",
        message="World"
    )

    service.create_notification(notification)

    result = service.get_notification_by_id(1)

    assert result["id"] == 1


def test_get_notification_by_invalid_id():

    service = NotificationService()

    result = service.get_notification_by_id(100)

    assert result is None


def test_mark_as_read():

    service = NotificationService()

    notification = NotificationCreate(
        user_id=1,
        title="Reminder",
        message="Meeting at 10 AM"
    )

    service.create_notification(notification)

    result = service.mark_as_read(1)

    assert result["is_read"] is True


def test_mark_as_read_invalid_id():

    service = NotificationService()

    result = service.mark_as_read(100)

    assert result is None


def test_delete_notification():

    service = NotificationService()

    notification = NotificationCreate(
        user_id=1,
        title="Delete",
        message="Delete this notification"
    )

    service.create_notification(notification)

    result = service.delete_notification(1)

    assert result is True
    assert len(service.notifications) == 0


def test_delete_notification_invalid_id():

    service = NotificationService()

    result = service.delete_notification(100)

    assert result is False
