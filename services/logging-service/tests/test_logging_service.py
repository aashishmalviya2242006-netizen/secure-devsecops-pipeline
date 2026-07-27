from app.schemas import LogCreate
from app.services.logging_service import LoggingService


def test_create_log():

    service = LoggingService()

    log = LogCreate(
        service="Auth Service",
        level="INFO",
        message="User logged in"
    )

    result = service.create_log(log)

    assert result["id"] == 1
    assert result["service"] == "Auth Service"
    assert result["level"] == "INFO"
    assert result["message"] == "User logged in"


def test_get_all_logs():

    service = LoggingService()

    log = LogCreate(
        service="User Service",
        level="INFO",
        message="User created"
    )

    service.create_log(log)

    result = service.get_all_logs()

    assert len(result) == 1


def test_get_log_by_id():

    service = LoggingService()

    log = LogCreate(
        service="Notification Service",
        level="INFO",
        message="Notification sent"
    )

    service.create_log(log)

    result = service.get_log_by_id(1)

    assert result["id"] == 1


def test_get_log_by_invalid_id():

    service = LoggingService()

    result = service.get_log_by_id(100)

    assert result is None


def test_delete_log():

    service = LoggingService()

    log = LogCreate(
        service="Gateway",
        level="WARNING",
        message="Slow response"
    )

    service.create_log(log)

    result = service.delete_log(1)

    assert result is True
    assert len(service.logs) == 0


def test_delete_log_invalid_id():

    service = LoggingService()

    result = service.delete_log(100)

    assert result is False
