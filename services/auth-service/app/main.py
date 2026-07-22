from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Auth Service",
    description="Authentication Microservice for Secure DevSecOps Pipeline",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Auth Service",
        "service": "auth-service",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "auth-service"
    }


app.include_router(auth_router)
