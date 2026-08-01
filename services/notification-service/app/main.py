from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Notification Service",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Notification Service is Running"
    }

@app.get("/health")
def health():
    return {"status": "healthy",
            "service":"notification-service"}

