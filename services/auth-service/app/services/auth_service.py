from app.schemas import RegisterRequest
from app.core import (
    hash_password,
    verify_password,
    create_access_token,
)


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

    def get_user_by_id(self, user_id: int):
        for user in self.users:
            if user["id"] == user_id:
                return {
                   "id": user["id"],
                   "name": user["name"],
                   "email": user["email"],
            }

        return None

    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email)

        if user is None:
            return None

        if not verify_password(password, user["password"]):
            return None

        access_token = create_access_token(
          {
            "sub": str(user["id"]),
            "email": user["email"],
          }
         )

        return {
             "access_token": access_token,
             "token_type": "bearer",
         }

auth_service = AuthService()
