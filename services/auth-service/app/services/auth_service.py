from app.schemas import RegisterRequest
from app.core.security import hash_password


class AuthService:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def register(self, user: RegisterRequest):
        # Check if email already exists
        for existing_user in self.users:
            if existing_user["email"] == user.email:
                return None

        new_user = {
            "id": self.next_id,
            "name": user.name,
            "email": user.email,
            "password": hash_password(user.password),
        }

        self.users.append(new_user)
        self.next_id += 1

        return {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
        }

    def get_user_by_email(self, email: str):
        for user in self.users:
            if user["email"] == email:
                return user
        return None


auth_service = AuthService()
