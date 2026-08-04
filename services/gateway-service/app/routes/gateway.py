from fastapi import APIRouter, HTTPException, Request, Response
from json import JSONDecodeError

from app.services.gateway_service import forward_request

router = APIRouter()

@router.get("/")
async def root():
    return {
        "service": "Gateway Service",
        "project": "Secure DevSecOps Pipeline",
        "status": "healthy",
        "version": "1.0.0",
        "message": "Welcome to the Secure DevSecOps API Gateway"
    }


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "gateway-service"
    }


async def gateway_handler(
    request: Request,
    service: str,
    path: str,
):
    """
    Common handler for forwarding requests to the appropriate microservice.
    """

    body = None

    # Read request body only for methods that can contain one
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except JSONDecodeError:
            body = None

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


# -------------------- GET --------------------

@router.get("/{service}/{path:path}")
async def gateway_get(
    request: Request,
    service: str,
    path: str,
):
    return await gateway_handler(request, service, path)


# -------------------- POST --------------------

@router.post("/{service}/{path:path}")
async def gateway_post(
    request: Request,
    service: str,
    path: str,
):
    return await gateway_handler(request, service, path)


# -------------------- PUT --------------------

@router.put("/{service}/{path:path}")
async def gateway_put(
    request: Request,
    service: str,
    path: str,
):
    return await gateway_handler(request, service, path)


# -------------------- PATCH --------------------

@router.patch("/{service}/{path:path}")
async def gateway_patch(
    request: Request,
    service: str,
    path: str,
):
    return await gateway_handler(request, service, path)


# -------------------- DELETE --------------------

@router.delete("/{service}/{path:path}")
async def gateway_delete(
    request: Request,
    service: str,
    path: str,
):
    return await gateway_handler(request, service, path)
