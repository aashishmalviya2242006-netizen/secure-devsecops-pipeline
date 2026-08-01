import httpx

from app.core.config import settings


async def send_log(
    service: str,
    level: str,
    message: str,
):
    """
    Send a log to Logging Service.
    """

    payload = {
        "service": service,
        "level": level,
        "message": message,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{settings.LOGGING_SERVICE_URL}/logs/",
            json=payload,
        )

    response.raise_for_status()

    return response.json()
