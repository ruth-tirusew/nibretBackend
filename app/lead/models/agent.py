from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated, Any
from datetime import datetime
from enum import Enum


from app.lead.models.lead_management import LeadActivity
from app.auth.models.users import UserBase
from app.utils import AppModel

PyObjectId = Annotated[str, BeforeValidator(str)]

class lead(BaseModel): 
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    @field_validator('id', mode="before", )
    def validate_id(cls, v):
        if v:
            return str(v)

class AgentProfileReponse(UserBase):
    ...

class AgentDetailResponseModel(lead):
    leads=List[LeadActivity]


