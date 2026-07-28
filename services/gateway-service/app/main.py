from fastapi import FastAPI

from app.routes.gateway import router

app = FastAPI(
    title="Gateway Service",
    version="1.0.0",
)

app.include_router(router)
