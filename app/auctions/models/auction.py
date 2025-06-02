from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator
from typing import Optional, List,Annotated
from datetime import datetime

from app.auctions.utils.enums import StatusEnum
from app.commons.models import LocationBase

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
    id: Optional[UUID4]
    ...

class AuctionResponse(AuctionBase):
    id: UUID4

class ImageResponse(ImageBase):
    auction: AuctionBase