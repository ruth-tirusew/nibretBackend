from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]




class LoanerBase(BaseModel):
    logo: Optional[str] = None
    name: str
    real_state_provided: bool = False
    phone: Optional[str] = None


class HomeloanBase(BaseModel):
    name: str
    description: str
    loaner: LoanerBase
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class Homeloan(HomeloanBase):
    ...

class HomeloanResponse(Homeloan):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

