from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from src.config import settings
from typing import Literal, Dict

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ROLES = ["admin", "normal", "limited"]

    USERS: Dict[str, Dict[str, str]] = {
        "admin": {"username": "admin", "password": "admin123", "role": "admin"},
        "normal": {"username": "normal", "password": "normal123", "role": "normal"},
        "limited": {"username": "limited", "password": "limited123", "role": "limited"},
    }

    def create_access_token(self, username: str, role: Literal["admin", "normal", "limited"]) -> str:
        if role not in self.ROLES:
            raise ValueError(f"Invalid role: {role}")
        to_encode = {"sub": username, "role": role}
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username = payload.get("sub")
            role = payload.get("role")
            if username is None or role not in self.ROLES:
                raise HTTPException(status_code=401, detail="Invalid token")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def authenticate_user(self, username: str, password: str):
        user = self.USERS.get(username)
        if user and user["password"] == password:
            return user
        return None