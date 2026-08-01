import httpx

from app.core.config import settings


async def send_notification(
    user_id: int,
    title: str,
    message: str,
):
    """
    Send a notification to Notification Service.
    """

    payload = {
        "user_id": user_id,
        "title": title,
        "message": message,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{settings.NOTIFICATION_SERVICE_URL}/notifications/",
            json=payload,
        )

    response.raise_for_status()

    return response.json()
