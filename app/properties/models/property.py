from pydantic import BaseModel, UUID4, Field, field_validator, BeforeValidator,  confloat, conint, validator
from uuid import UUID
from typing import Optional, List,Annotated
from datetime import datetime
from app.properties.utils.enums import *


class LocationBase(BaseModel):
    name: str
    longitude: float
    latitude: float


class ImageBase(BaseModel):
    is_cover: bool = False
    image_url: str
    blur_hash: Optional[str] = None

class Image(ImageBase):
    ...

class LoanerBase(BaseModel):
    logo: Optional[str] = None
    name: str
    real_state_provided: bool = False
    phone: Optional[str] = None


class PropertyBase(BaseModel):
    pictures: List[Image]
    name: str
    description: str
    location: LocationBase
    price: float
    bedroom: Optional[int] = 0
    bathroom: Optional[int] = 0
    area: Optional[float] = 0.0
    currency: str = "ETB"
    discount: Optional[float] = 0.0
    sold_out: bool = False
    is_store: bool = False
    type: Optional[str] = None
    move_in_date: Optional[datetime] = None
    rental: bool = False
    furnished: bool = False



class Property(PropertyBase):
    ...

class PropertyResponse(PropertyBase):
    id: UUID4

class LocationResponse(LocationBase):
    property: Optional[PropertyBase]


class LoanerResponse(LoanerBase):
    pass


class PropertyCreate(BaseModel):
    pictures: List[str]
    name: str = Field(..., min_length=1, max_length=255,
                     example="Modern Downtown Apartment")
    tr_name: Optional[str] = Field(None, max_length=255,
                                  example="ዘመናዊ ከተማ አፓርታማ")
    description: str = Field(..., min_length=10,
                            example="Spacious 3 bedroom apartment in city center")
    tr_description: Optional[str] = Field(None,
                                        example="በከተማ ማዕከል ውስጥ ሰፋት ያለው 3 መኝታ ቤት ያለው አፓርታማ")

    location: LocationBase
    price: confloat(gt=0) = Field(..., example=2500000.00)
    bedroom: Optional[conint(ge=0)] = Field(0, example=3)
    bathroom: Optional[conint(ge=0)] = Field(0, example=2)
    area: confloat(gt=0) = Field(..., example=150.5)
    currency: Optional[str] = Field("ETB", example="ETB")
    discount: Optional[confloat(ge=0)] = Field(None, example=100000.00)
    sold_out: Optional[bool] = Field(False)
    owner_id: Optional[UUID] = Field(None, example="550e8400-e29b-41d4-a716-446655440001")
    is_store: Optional[bool] = Field(False)
    type: PropertyType = Field(..., example=PropertyType.APARTMENT)
    move_in_date: Optional[datetime] = Field(None)
    rental: Optional[bool] = Field(False)
    furnished: Optional[bool] = Field(False)

    @validator('currency')
    def validate_currency(cls, value):
        valid_currencies = {"ETB", "USD"}
        if value.upper() not in valid_currencies:
            raise ValueError(f"Invalid currency. Valid options: {valid_currencies}")
        return value.upper()

    @validator('price', 'area')
    def validate_positive_values(cls, value):
        if value <= 0:
            raise ValueError("Value must be greater than 0")
        return value

class PropertyDBCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255,
                     example="Modern Downtown Apartment")
    tr_name: Optional[str] = Field(None, max_length=255,
                                  example="ዘመናዊ ከተማ አፓርታማ")
    description: str = Field(..., min_length=10,
                            example="Spacious 3 bedroom apartment in city center")
    tr_description: Optional[str] = Field(None,
                                        example="በከተማ ማዕከል ውስጥ ሰፋት ያለው 3 መኝታ ቤት ያለው አፓርታማ")

    location_id: UUID
    price: confloat(gt=0) = Field(..., example=2500000.00)
    bedroom: Optional[conint(ge=0)] = Field(0, example=3)
    bathroom: Optional[conint(ge=0)] = Field(0, example=2)
    area: confloat(gt=0) = Field(..., example=150.5)
    currency: Optional[str] = Field("ETB", example="ETB")
    discount: Optional[confloat(ge=0)] = Field(None, example=100000.00)
    sold_out: Optional[bool] = Field(False)
    owner_id: Optional[UUID] = Field(None, example="550e8400-e29b-41d4-a716-446655440001")
    is_store: Optional[bool] = Field(False)
    type: PropertyType = Field(..., example=PropertyType.APARTMENT)
    move_in_date: Optional[datetime] = Field(None)
    rental: Optional[bool] = Field(False)
    furnished: Optional[bool] = Field(False)


class HomeOwnerBase(BaseModel):
    name: str = Field(...,example="Landmark Apartments")
    type: OwnerType = Field(..., example=OwnerType.REGULAR)

class HomeOwnerRequest(HomeOwnerBase):
    ...

class HomeOwnerResponse(HomeOwnerBase):
    id: UUID