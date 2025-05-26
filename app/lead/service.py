from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from sqlalchemy.orm import Session
from typing import Annotated, Optional

from app.config import env
from app.database import get_db
from app.auth.service import  get_service as auth_service
from app.lead.repository.repository import AgentRepository
from app.lead.models.lead_management import *
from app.auth.utils.security import *

class Service:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.repository = AgentRepository(db)
        self.authService = auth_service()

    def add_activity(self, activity: LeadActivity)->Optional[LeadActivityResponse]:
        print(activity.user_id)
        self.authService.get_user_by_id(activity.user_id)
        
        return self.repository.register_lead(activity)
    def get_all_activities(self)->Optional[List[LeadActivityResponse]]:
        leads=self.repository.get_leads()
        return leads
    

def get_service():
    svc = Service(database)
    return svc
