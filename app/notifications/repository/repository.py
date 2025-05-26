from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from app.notificationClients.models.notificationClient import *
from app.notificationClients.utils.blurhash import generate_blurhash



class NotificationClientRepository:
    def __init__(self, database: Database):
        self.database = database

    def register_notification_client(self, notificationClient: NotificationClient) -> Optional[NotificationClient]:
        notification_client_saved = notificationClient.model_dump()
        self.database["notificationClients"].insert_one(
            **notification_client_saved
        )
        return notification_client_saved

    def get_notification_client_by_id(self, id: str) -> Optional[NotificationClient]:
        notificationClient = self.database["notificationClient"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if notificationClient:
            return NotificationClient.model_validate(notificationClient)
    
    def update_notification_client(self, id:str,notificationClient:NotificationClient)->Optional[NotificationClient]:
        notificationClient_saved = notificationClient.model_dump()
        notificationClient = self.database["notificationClients"].find_one_and_update(
            filter={
                "_id": ObjectId(id),
            },
            update={
                "$set": {
                    **notificationClient_saved}}
            )

        return notificationClient

    def delete_notification_client(self, id:str)->bool:
        notificationClient = self.database["notificationClients"].delete_one(
            filter={
                "_id": ObjectId(id),
            },
            )
        return notificationClient.deleted_count >0


    def get_notification_clients(self)-> Optional[List[PropertyResponse]]:
        notificationClients = self.database['notificationClients'].find()
        return notificationClients


    def filter_by_fcm(self, fcm_token: str) -> Optional[NotificationClient]:
        notificationClient = self.database["notificationClient"].find_one(
            {
                "fcm_token": fcm_token,
            }
        )
        if notificationClient:
            return NotificationClient.model_validate(notificationClient)