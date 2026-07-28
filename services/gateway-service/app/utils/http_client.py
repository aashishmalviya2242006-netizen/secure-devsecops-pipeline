import httpx

TIMEOUT = 10

async def send_request(
    method: str,
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    json: dict | None = None,
):
    async with httpx.AsyncClient(
    timeout=TIMEOUT,
    follow_redirects=True,
    ) as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
        )


    return response
