from app.core.config import SERVICE_MAP
from app.utils.http_client import send_request


async def forward_request(
    service: str,
    path: str,
    method: str,
    headers: dict | None = None,
    params: dict | None = None,
    body: dict | None = None,
):
    """
    Forward an HTTP request to the appropriate microservice.
    """

    base_url = SERVICE_MAP.get(service)

    if base_url is None:
        return None

    destination_url = f"{base_url}/{service}"

    if path:
        destination_url += f"/{path}"

    response = await send_request(
        method=method,
        url=destination_url,
        headers=headers,
        params=params,
        json=body,
    )

    return response
