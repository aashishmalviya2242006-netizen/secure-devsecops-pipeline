from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Logging Service",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Logging Service is Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service":"logging-service"
    }
