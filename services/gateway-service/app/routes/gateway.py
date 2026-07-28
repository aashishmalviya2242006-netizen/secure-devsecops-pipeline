from fastapi import APIRouter, HTTPException, Request, Response

from app.services.gateway_service import forward_request

router = APIRouter()

@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "gateway-service"
    }


@router.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def gateway(
    request: Request,
    service: str,
    path: str,
):
    """
    Forward requests to the appropriate microservice.
    """

    body = None

    if request.method in ("POST", "PUT", "PATCH"):
        body = await request.json()

    # Filter headers before forwarding
    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in {
            "host",
            "content-length",
            "connection",
            "transfer-encoding",
        }
    }

    response = await forward_request(
        service=service,
        path=path,
        method=request.method,
        headers=headers,
        params=dict(request.query_params),
        body=body,
    )

    if response is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found.",
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get(
            "content-type",
            "application/json",
        ),
    )
