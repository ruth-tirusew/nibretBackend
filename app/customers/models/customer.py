from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated, Any
from datetime import datetime
from enum import Enum

from app.utils import AppModel

PyObjectId = Annotated[str, BeforeValidator(str)]


class CustomerBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    first_name: str
    last_name:str
    email: Optional[str]=None
    phone: str

class GetAllCustomersResponse(BaseModel):
    customers: List[CustomerBase]
