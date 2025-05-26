from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated, Any
from datetime import datetime
from enum import Enum

from app.utils import AppModel

PyObjectId = Annotated[str, BeforeValidator(str)]



class TemplateBase(BaseModel):
    name: Optional[str]=None
    content: str

class TemplateResponse(TemplateBase):
     id: Optional[PyObjectId] = Field(alias="_id", default=None) 

class GetAllResponse(BaseModel):
    templates: List[Optional[TemplateBase]]