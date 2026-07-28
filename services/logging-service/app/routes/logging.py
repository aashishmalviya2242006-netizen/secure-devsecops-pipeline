from fastapi import APIRouter, HTTPException

from app.schemas import (
    LogCreate,
    LogResponse,
)
from app.services import logging_service

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "logging-service"
    }


@router.post("/", response_model=LogResponse)
def create_log(log: LogCreate):
    return logging_service.create_log(log)


@router.get("/", response_model=list[LogResponse])
def get_all_logs():
    return logging_service.get_all_logs()


@router.get("/{log_id}", response_model=LogResponse)
def get_log_by_id(log_id: int):

    log = logging_service.get_log_by_id(log_id)

    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return log


@router.delete("/{log_id}")
def delete_log(log_id: int):

    deleted = logging_service.delete_log(log_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return {
        "message": "Log deleted successfully"
    }
