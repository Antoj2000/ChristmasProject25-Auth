import os
from datetime import datetime, timedelta, timezone

import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev_change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_ISS = os.getenv("JWT_ISS", "auth-service")
JWT_AUD = os.getenv("JWT_AUD", "dpd-app")
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))


def hash_password(password: str) -> str:
    #Replace with bcrypt hash later
    return password

def verify_password(plain_password: str, stored_password: str) -> bool:
    #Replace with bcrypt verify later
    return plain_password == stored_password

def create_access_token(*, account_id: int, account_no: str, email: str) -> str:
    #Create a JWT access token
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(account_id),
        "account_no": account_no,
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_MINUTES)).timestamp()),
        "iss": JWT_ISS,
        "aud": JWT_AUD,
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)





