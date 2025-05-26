from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated, Any
from datetime import datetime
from enum import Enum

from app.utils import AppModel

PyObjectId = Annotated[str, BeforeValidator(str)]



class EmailBase(BaseModel):
    user_id: str
    agent_id: str
    template_id: str
    remark: Optional[str]=None

class EmailResponse(EmailBase):
     id: Optional[PyObjectId] = Field(alias="_id", default=None) 