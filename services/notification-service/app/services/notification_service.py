from app.schemas import NotificationCreate


class NotificationService:

    def __init__(self):
        self.notifications = []
        self.next_id = 1

    def create_notification(self, notification: NotificationCreate):

        new_notification = {
            "id": self.next_id,
            "user_id": notification.user_id,
            "title": notification.title,
            "message": notification.message,
            "is_read": False,
        }

        self.notifications.append(new_notification)
        self.next_id += 1

        return new_notification

    def get_all_notifications(self):
        return self.notifications

    def get_notification_by_id(self, notification_id):

        for notification in self.notifications:
            if notification["id"] == notification_id:
                return notification

        return None

    def mark_as_read(self, notification_id):

        notification = self.get_notification_by_id(notification_id)

        if notification is None:
            return None

        notification["is_read"] = True

        return notification

    def delete_notification(self, notification_id):

        notification = self.get_notification_by_id(notification_id)

        if notification is None:
            return False

        self.notifications.remove(notification)

        return True


notification_service = NotificationService()
