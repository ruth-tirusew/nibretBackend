from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from app.lead.models.lead_management import *

class AgentRepository:
    def __init__(self, database: Database):
        self.database = database

    def register_lead(self,lead: LeadActivity) -> Optional[LeadActivityResponse]:
        lead_saved = lead.model_dump()
       
        result = self.database["leads"].insert_one(lead_saved)
        lead_saved["_id"] = result.inserted_id
        print(lead_saved)
        return lead_saved
        
    def get_lead_by_id(self, id: str) -> Optional[LeadActivityDetail]:
        lead = self.database["leads"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if lead:
            return lead.model_validate(lead)
    
    def update_lead(self, id:str,lead:LeadActivity)->Optional[LeadActivity]:
        lead = self.database["leads"].find_one_and_update(
            filter={
                "_id": ObjectId(id),
            },
            update={
                "$set": {
                    **lead}}
            )

        return lead

    def delete_lead(self, id:str)->bool:
        lead = self.database["leads"].delete_one(
            filter={
                "_id": ObjectId(id),
            },
            )
        return lead.deleted_count >0


    def get_leads(self)-> Optional[List[LeadActivity]]:
        leads = self.database['leads'].find()
        return leads