from fastapi import FastAPI
from app.routes.users import router as user_router

app = FastAPI(
    title="User Service",
    description="User Management Microservice for Secure DevSecOps Pipeline",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to User Service",
        "service": "user-service",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "user-service"
    }


app.include_router(user_router)
