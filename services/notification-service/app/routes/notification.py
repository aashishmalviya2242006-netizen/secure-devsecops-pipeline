from fastapi import APIRouter, HTTPException

from app.schemas import (
    NotificationCreate,
    NotificationResponse,
)
from app.services import notification_service

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate):
    return notification_service.create_notification(notification)


@router.get("/", response_model=list[NotificationResponse])
def get_all_notifications():
    return notification_service.get_all_notifications()


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification_by_id(notification_id: int):

    notification = notification_service.get_notification_by_id(notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(notification_id: int):

    notification = notification_service.mark_as_read(notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification


@router.delete("/{notification_id}")
def delete_notification(notification_id: int):

    deleted = notification_service.delete_notification(notification_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification deleted successfully"
    }
