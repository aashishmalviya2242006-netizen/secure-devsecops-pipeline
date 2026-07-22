from app.schemas import RegisterRequest
from app.core.password import hash_password, verify_password


class AuthService:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def register(self, user: RegisterRequest):
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

    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email)

        if user is None:
            return None

        if not verify_password(password, user["password"]):
            return None

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        }


auth_service = AuthService()
