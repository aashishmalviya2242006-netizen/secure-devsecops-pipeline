class Settings:
    """
    Central configuration for User Service.
    """

    APP_NAME = "User Service"

    LOGGING_SERVICE_URL = "http://logging-service:8004"

    NOTIFICATION_SERVICE_URL = "http://notification-service:8003"


settings = Settings()
