from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class TokenRequest(BaseModel):

    account_no: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AccountCreatedEvent(BaseModel):

    account_id: int
    account_no: str = Field(..., min_length=6, max_length=6)
    email: EmailStr
    # This will become password_hash later
    password: str