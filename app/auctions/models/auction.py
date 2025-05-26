from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator
from typing import Optional, List,Annotated
from datetime import datetime

from app.auctions.utils.enums import StatusEnum



PyObjectId = Annotated[str, BeforeValidator(str)]

class LocationBase(BaseModel):
    name: str
    type: Optional[str]="Point"
    coordinates: List[float]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ImageBase(BaseModel):
    is_cover: bool = False
    image_url: str
    blur_hash: Optional[str] = None


class AuctionBase(BaseModel):
    pictures: List[ImageBase]
    name: str
    description: str
    location: LocationBase
    starting_bid: float
    start_date: datetime
    end_date: datetime
    status: StatusEnum
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class Auction(AuctionBase):
    ...

class AuctionResponse(AuctionBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)


class ImageResponse(ImageBase):
    auction: AuctionBase
