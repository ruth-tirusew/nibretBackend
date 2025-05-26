from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from datetime import datetime
from enum import Enum
import re
from typing import Optional, List,Annotated, Any

from app.utils import AppModel

PHONE_REGEX = r"^\+[1-9]\d{1,14}$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"



class Role(str, Enum):
    ADMIN='ADMIN'
    CUSTOMER='CUSTOMER'


class UserBase(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: str | None
    phone: str
    role: Role
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
        use_enum_values = True


class AuthorizeUserResponse(AppModel):
    access_token: str
    token_type: str = "Bearer"


class UserMutationBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    email: Optional[str] = Field(
        None,
        pattern=EMAIL_REGEX,
        example="user@example.com",
        description="Must be a valid email address"
    )
    phone: str = Field(
        ...,
        pattern=PHONE_REGEX,
        example="+1234567890",
        min_length=7,
        max_length=15,
        description="Phone number in E.164 international format"
    )

    @field_validator('phone', mode='before')
    def validate_phone(cls, value):
        if not re.match(PHONE_REGEX, value):
            raise ValueError("Invalid phone number format.")
        return value.strip()

    @field_validator('email', mode='before')
    def validate_email(cls, value):
        if value is None:
            return value
        if not re.match(EMAIL_REGEX, value):
            raise ValueError("Invalid email address format")
        return value.strip().lower()


class RegisterUserRequest(UserMutationBase):
    password1: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="StrongPass123!",
        description="Must contain uppercase, lowercase, number, and special character"
    )

    password2: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="StrongPass123!",
        description="Must contain uppercase, lowercase, number, and special character"
    )


    @field_validator('password1', mode='before')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{};':,./<>?~" for c in value):
            raise ValueError("Password must contain at least one special character")
        return value

class UpdateUserRequest(UserMutationBase):
    ...

class GetAllUsersResponse(BaseModel):
    users: List[UserBase]

class RegisterUserResponse(BaseModel):
    email: str

class JWTData(BaseModel):
    user_id: str = Field(alias="sub")


class UserResponse(UserBase):
    ...