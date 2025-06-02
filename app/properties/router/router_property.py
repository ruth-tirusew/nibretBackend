from fastapi import Depends, HTTPException, status, Body, Query, Request
from fastapi.security import OAuth2PasswordBearer

from uuid import UUID
from typing import List, Optional, Annotated

from app.auth.service import get_service
from app.properties.service import PropertyService, get_property_service
from app.properties.models import Property, PropertyResponse, PropertyCreate, HomeOwnerResponse, HomeOwnerRequest
from . import router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/")

@router.post("", status_code=status.HTTP_201_CREATED, response_model=PropertyResponse)
async def register_property(
    property_data: PropertyCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    service: PropertyService = Depends(get_property_service),
    auth_service = Depends(get_service)
):
    current_user = await auth_service.get_current_user(token)
    return service.create_property(property_data, current_user["id"])
    

@router.put("/{property_id}", status_code=status.HTTP_200_OK, response_model=PropertyResponse)
async def update_property(
    property_id: UUID,
    property_data: PropertyCreate,
    service: PropertyService = Depends(get_property_service),
):
    try:            
        return service.update_property(property_id, property_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to update property"
        )

@router.delete("/{property_id}", status_code=status.HTTP_200_OK)
async def delete_property(
    property_id: UUID,
    service: PropertyService = Depends(get_property_service),
):
    try:            
        if service.delete_property(property_id):
            return {"detail": "Property deleted successfully"}
        raise HTTPException(status_code=404, detail="Property not found")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete property"
        )

@router.get("/premium", status_code=status.HTTP_200_OK)
def get_premium_property(
    request: Request,
    limit:Optional[int]=Query(10),
    offset:Optional[int]=Query(0),
    service: PropertyService = Depends(get_property_service),
):
    return service.get_premium_properties(offset=offset, limit=limit, request=request)

@router.get("", status_code=status.HTTP_200_OK)
async def fetch_properties(
    request: Request,
    limit:Optional[int]=Query(10),
    offset:Optional[int]=Query(0),
    search: Optional[str] = Query(None),
    type: Optional[List[str]] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    bedroom: Optional[int] = Query(None),
    bathroom: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    service: PropertyService = Depends(get_property_service)
):
    filters = {
        "search": search,
        "type": type,
        "min_price": min_price,
        "max_price": max_price,
        "bedroom": bedroom,
        "bathroom": bathroom,
        "status": status
    }
    return service.get_properties(limit=limit, offset=offset, request=request, filters={k: v for k, v in filters.items() if v is not None})

@router.get("/{property_id}", status_code=status.HTTP_200_OK, response_model=PropertyResponse)
async def fetch_property(
    property_id: UUID,
    service: PropertyService = Depends(get_property_service)
):
    property = service.get_property(property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.get("/nearby", status_code=status.HTTP_200_OK, response_model=List[PropertyResponse])
async def fetch_nearby_properties(
    lat: float = Query(..., description="Latitude of center point"),
    lng: float = Query(..., description="Longitude of center point"),
    radius: float = Query(5.0, description="Search radius in kilometers"),
    service: PropertyService = Depends(get_property_service)
):
    return service.get_nearby_properties(lat, lng, radius)

@router.patch("/{property_id}/status", status_code=status.HTTP_200_OK, response_model=PropertyResponse)
async def toggle_sold_status(
    property_id: UUID,
    service: PropertyService = Depends(get_property_service),
):
    try:
        return service.toggle_sold_status(property_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to update property status"
        )

@router.get("/stats/monthly", status_code=status.HTTP_200_OK)
async def get_monthly_stats(
    service: PropertyService = Depends(get_property_service)
):
    return service.get_monthly_property_data()

@router.get("/stats/breakdown", status_code=status.HTTP_200_OK)
async def get_property_breakdown(
    service: PropertyService = Depends(get_property_service)
):
    return service.get_property_stats()


@router.get("/owner", status_code=status.HTTP_200_OK)
async def get_all_property_owners(
    service: PropertyService = Depends(get_property_service)
):
    return service.get_all_property_owners()

@router.post("/owner", status_code=status.HTTP_201_CREATED, response_model=HomeOwnerResponse)
async def register_property_owner(
    owner_data: HomeOwnerRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    service: PropertyService = Depends(get_property_service),
    auth_service = Depends(get_service)
):
    try:
        return service.create_property_owners(owner_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to create property"
        )