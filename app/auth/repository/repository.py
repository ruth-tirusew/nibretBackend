from datetime import datetime
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth.models.user import RegisterUserRequest, UpdateUserRequest
from app.auth.schema import User
from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, user_data: RegisterUserRequest):
        hashed_password = hash_password(user_data.password1)
        user = User(
            email=user_data.email,
            password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
        )

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or phone already exists"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return {
            "id": user.id,
            "first_name": user.first_name,"last_name": user.last_name,
            "email": user.email,
            "role":user.role,
            "phone": user.phone,
            "is_active":user.is_active,
            "created_at": user.created_at
        }

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "password": user.password,
            "created_at": user.created_at
        }

    def get_user_by_phone(self, phone: str) -> Optional[dict]:
        user = self.db.query(User).filter(User.phone == phone).first()
        if not user:
            return None
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "password": user.password,
            "created_at": user.created_at
        }

    def get_all_users(self) -> List[dict]:
        users = self.db.query(User).all()
        return users

    def update_user(self, user_id: str, user_data: UpdateUserRequest):
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate email or phone number"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone
        }

    def update_user_status(self, user_id: str, user_status: bool):
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.is_active = user_status

        try:
            self.db.commit()
            self.db.refresh(user)
        except Exception as e:
            print(e)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update status"
            )

        return user