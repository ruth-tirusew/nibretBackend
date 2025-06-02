from datetime import datetime
from typing import Optional, List
from fastapi import  HTTPException, status

from bson.objectid import ObjectId
from pymongo.database import Database

from app.auth.models.customers import *
from ..utils.security import hash_password


class CustomerRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_customer_by_id(self, user_id: str) -> Optional[dict]:
        try:
            user = self.database["users"].find_one(
                {
                    "_id": ObjectId(user_id),
                    "role":"CUSTOMER"
                },
                projection={
                    "password":False
                }
            )
            return user
        except:
            raise Exception(
                "Failed to fetch user",
            )

    def get_customer_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
                "role":"CUSTOMER"
            }
        )
        return user

    def get_customer_by_phone(self, phone: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "phone": phone,
                "role":"CUSTOMER"
            }
        )
        return user

    def get_all_customers(self)-> List[UserBase]:
        cursor = self.database["users"].find( 
            filter={
                "role":"CUSTOMER"
            },
            projection={
                "password": False,
                "created_at": False
            })
        users = cursor.to_list()
        return users