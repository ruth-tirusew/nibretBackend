from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from app.homeloan.models.loan import *

class HomeloanRepository:
    def __init__(self, database: Database):
        self.database = database

    def register_loan(self,loan: Homeloan) -> Optional[Homeloan]:
        loan_saved = loan.model_dump()
        # loan_saved['id'] = str(ObjectId())
        self.database["loans"].insert_one(loan_saved)
        
        return loan_saved

    def get_loan_by_id(self, id: str) -> Optional[Homeloan]:
        loan = self.database["loans"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if loan:
            return Homeloan.model_validate(loan)
    
    def update_loan(self, id:str,loan:Homeloan)->Optional[Homeloan]:
        loan_saved = loan.model_dump()
        loan = self.database["loans"].find_one_and_update(
            filter={
                "_id": ObjectId(id),
            },
            update={
                "$set": {
                    **loan_saved}}
            )

        return loan

    def delete_loan(self, id:str)->bool:
        loan = self.database["loans"].delete_one(
            filter={
                "_id": ObjectId(id),
            },
            )
        return loan.deleted_count >0


    def get_loans(self)-> Optional[List[HomeloanResponse]]:
        loans = self.database['loans'].find()
        return loans


