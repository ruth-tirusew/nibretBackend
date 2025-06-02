from pydantic import BaseModel, UUID4, Field

from typing import Optional, List,Annotated
from datetime import datetime


class NotificationClient(BaseModel):
    user_id: str
    fwc_token: str


class NotificationResponse(NotificationClient):
    id: UUID4