from datetime import datetime
from typing import Optional, List
from fastapi import  HTTPException, status

from bson.objectid import ObjectId
from pymongo.database import Database

from app.email.models import *


class EmailRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_template(self, template: dict):
        result = self.database["templates"].insert_one(template)

        return result

    def get_all_templates(self) -> Optional[List]:
        cursor = self.database["templates"].find()
        templates = cursor.to_list()
        return templates

    def get_template_by_id(self, template_id: str) -> Optional[dict]:
        try:
            template = self.database["templates"].find_one(
                {
                    "_id": ObjectId(template_id),
                }
            )
            return template
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch template",
            )

    def update_template(self, template: dict):
        template_id = template.get("id")
        update_result = self.database["templates"].find_one_and_update(
            filter={
                "_id": ObjectId(id),
            },
            update={
                "$set": {
                    **template}}
            )

        return update_result

    def delete_template(self, template: dict):
        template_id = template.get("id")
        delete_result = self.database["templates"].delete_one(
            filter={
                "_id": ObjectId(id),
            }
        )
        return delete_result



    def create_email(self, email: dict):
        result = self.database["emails"].insert_one(email)

        return result

    def get_email_by_id(self, email_id: str) -> Optional[dict]:
        try:
            user = self.database["emails"].find_one(
                {
                    "_id": ObjectId(user_id),
                }
            )
            return user
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch email",
            )

    def update_email(self, email: dict):
        email_id = email.get("id")
        update_result = self.database["emails"].find_one_and_update(
            filter={
                "_id": ObjectId(id),
            },
            update={
                "$set": {
                    **email}}
            )

        return update_result

    def delete_email(self, email: dict):
        email_id = email.get("id")
        delete_result = self.database["emails"].delete_one(
            filter={
                "_id": ObjectId(id),
            }
        )
        return delete_result
