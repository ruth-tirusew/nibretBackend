from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator

from typing import Optional, List,Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class NotificationClient(BaseModel):
    user_id: str
    fwc_token: str


class NotificationResponse(NotificationClient):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)