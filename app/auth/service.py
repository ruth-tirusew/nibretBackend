from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from sqlalchemy.orm import Session
from typing import Annotated, Optional, List

from app.auth.models.user import JWTData, RegisterUserRequest, GetAllUsersResponse, UserBase, UpdateUserRequest
from app.auth.repository.repository import AuthRepository
from app.auth.utils.security import *
from app.auth.utils.errors import *
from app.config import env
from app.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/")
SECRET=env.SECRET

class Service:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.repository = AuthRepository(db)
        self.algorithm = 'HS256'
        self.expiration = 25

    def create_user(self, user:RegisterUserRequest):  
        if user.password1 != user.password2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords don't match",
            )

        if user.email and self.repository.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already taken.",
            )

        if self.repository.get_user_by_phone(user.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is already taken.",
            )

        user = self.repository.create_user(user)
        if user:
            token = self.create_access_token(user)

        return token

    def get_user_by_id(self, id: str):
        user =  self.repository.get_user_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist.",
            )
        return user

    async def get_current_user(self,token: str):
        try:
            payload = jwt.decode(token, SECRET, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise AuthenticationRequiredException
        except Exception as e:
            raise e
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise AuthenticationRequiredException
        return user

    def create_access_token(
        self,
        user: dict,
    ) -> str:
        expires_delta = timedelta(minutes=self.expiration)

        jwt_data = {
            "sub": str(user["id"]),
            "exp": datetime.utcnow() + expires_delta,
        }

        return jwt.encode(jwt_data, SECRET, algorithm=self.algorithm)

    def login(self, input):
        user = self.repository.get_user_by_phone(input.username)

        if not user:
            raise InvalidCredentialsException

        if not check_password(input.password, user["password"]):
            raise InvalidCredentialsException

        return self.create_access_token(user)

    def parse_jwt_user_data(self, token: str) -> Optional[JWTData]:
        if not token:
            return None

        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except JWTError:
            raise Exception(
                "Authentication Failed"
            )

        return JWTData(**payload)

    def get_all_users(self)->List[UserBase]:
        users =  self.repository.get_all_users()
        return users

    def update_profile(self, token: str, input: UpdateUserRequest):
        payload = jwt.decode(token, SECRET, algorithms=[self.algorithm])
        user_id: str = payload.get("sub")
        return self.repository.update_user(user_id, input)
    
    def update_user(self, user_id: int, input: UpdateUserRequest):
        return self.repository.update_user(user_id, input)

    def update_user_status(self,user_id:str, user_status: bool):
        return self.repository.update_user_status(user_id, user_status)
        


def get_service(db: Session = Depends(get_db)):
    svc = Service(db)
    return svc
