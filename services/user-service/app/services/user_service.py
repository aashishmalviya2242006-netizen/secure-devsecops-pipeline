from app.clients.logging_client import send_log
from app.clients.notification_client import send_notification

from app.schemas.user import User, UserCreate, UserUpdate


class UserService:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def get_all_users(self):
        return self.users

    def get_user(self, user_id: int):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    async def create_user(self, user: UserCreate):
        new_user = User(
            id=self.next_id,
            name=user.name,
            email=user.email,
        )

        self.users.append(new_user)
        self.next_id += 1

        # Send log
        try:
            await send_log(
                service="user-service",
                level="INFO",
                message=f"User '{new_user.name}' created successfully"
            )
        except Exception as e:
            print(f"Logging Service Error: {e}")

        # Send welcome notification
        try:
            await send_notification(
                user_id=new_user.id,
                title="Welcome",
                message=f"Welcome {new_user.name}! Your account has been created successfully."
            )
        except Exception as e:
            print(f"Notification Service Error: {e}")

        return new_user

    def update_user(self, user_id: int, user_data: UserUpdate):
        user = self.get_user(user_id)

        if not user:
            return None

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:
            user.email = user_data.email

        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)

        if not user:
            return False

        self.users.remove(user)
        return True


user_service = UserService()
