from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated, Any
from datetime import datetime
from enum import Enum

from app.properties.models.property import PropertyResponse
from app.auth.models.user import UserResponse
from app.utils import AppModel

PyObjectId = Annotated[str, BeforeValidator(str)]

class CallLog(BaseModel):
    call_duration: int
    notes: str

class MessageLogs(BaseModel):
    text: str
    notes: str



class LeadActivity(BaseModel):
    user_id: str
    agent_id: Optional[str]=None

    property_id: str
    call_log: Optional[CallLog]=None
    message: Optional[MessageLogs]=None
    additional_notes: Optional[str]=None


class LeadActivityResponse(LeadActivity):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user: UserResponse
    agent: UserResponse
    
   
class LeadActivityDetail(LeadActivity):
    property:  PropertyResponse