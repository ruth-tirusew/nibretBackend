from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator,  confloat, conint, validator
from uuid import UUID
from typing import Optional, List,Annotated
from datetime import datetime
from app.properties.utils.enums import *


class LocationBase(BaseModel):
    name: str
    longitude: float
    latitude: float