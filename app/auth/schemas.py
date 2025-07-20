from typing import Annotated

from pydantic import BaseModel
from pydantic import EmailStr as EmailString
from pydantic import Field

EmailStr = Annotated[
    EmailString,
    Field(
        ...,
        description="Email пользователя",
        json_schema_extra={"example": "user@example.com"},
    ),
]
PassStr = Annotated[
    str,
    Field(
        ...,
        min_length=8,
        description="Пароль не короче 8 символов",
        json_schema_extra={"example": "qwerty123"},
    ),
]


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserDTO(BaseModel):
    id: int = Field(..., ge=0)
    email: EmailStr
    hashed_password: str
    active: bool = True


class UserRegisterDTO(BaseModel):
    email: EmailStr
    password: PassStr


class MessageResponse(BaseModel):
    message: str
