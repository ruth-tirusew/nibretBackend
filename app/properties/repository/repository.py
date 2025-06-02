from datetime import datetime
from fastapi import Request
from sqlalchemy import func, text, or_, and_, case, extract, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict,Any
from uuid import UUID

from app.commons.models import LocationBase
from app.commons.schema import  *
from app.commons.utils.pagination_result import PaginatedResult
from app.commons.utils import get_paginated_query
from app.properties.utils.enums import *
from app.properties.schema import Property, Image, HomeOwners
from app.properties.models import PropertyDBCreate, Image as ImageRequest, HomeOwnerRequest, HomeOwnerResponse

class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def _build_filters(self, filters: Dict[str, Any]) -> List:
        """Convert API filters to SQLAlchemy filter conditions"""
        filter_conditions = []
        
        if filters.get("search"):
            filter_conditions.append(
                or_(
                    Property.title.ilike(f"%{filters['search']}%"),
                    Property.description.ilike(f"%{filters['search']}%")
                )
            )
        
        if filters.get("type"):
            filter_conditions.append(Property.type.in_(filters["type"]))
            
        if filters.get("min_price"):
            filter_conditions.append(Property.price >= filters["min_price"])
            
        if filters.get("max_price"):
            filter_conditions.append(Property.price <= filters["max_price"])
            
        if filters.get("bedroom"):
            filter_conditions.append(Property.bedroom_count == filters["bedroom"])
            
        if filters.get("bathroom"):
            filter_conditions.append(Property.bathroom_count == filters["bathroom"])
            
        if filters.get("status"):
            filter_conditions.append(Property.status == filters["status"])
            
        return filter_conditions

    def create_property_owners(self, owners_data: HomeOwnerRequest)->Optional[HomeOwnerResponse]:
        try:
            property_owner = HomeOwners(**owners_data.dict())
            self.db.add(property_owner)
            self.db.commit()
            self.db.refresh(property_owner)
            return property_owner
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_property_owner(self, property_owner_id: UUID, property_owner_data: HomeOwnerRequest) -> Optional[HomeOwnerResponse]:
        try:
            property_owner = self.get_property(property_id)
            if not property_owner:
                return None

            for key, value in property_owner_data.dict(unset=True).items():
                setattr(property_owner, key, value)

            self.db.commit()
            self.db.refresh(property_owner)
            return property_owner
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_property_owner(self, property_owner_id: UUID) -> Optional[HomeOwnerResponse]:
        return self.db.query(HomeOwners)\
            .filter(HomeOwners.id == property_owner_id)\
            .first()
    def delete_property_owner(self, property_owner_id: UUID) -> bool:
        try:
            property_owner = self.get_property_owner(property_owner_id)
            if property_owner:
                self.db.delete(property_owner)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_property_owners(self) -> List[HomeOwners]:
        return self.db.query(HomeOwners).order_by(HomeOwners.created_at.desc()).all()

    def create_property(self, property_data: PropertyDBCreate, user_id: UUID) -> Property:
        try:
            property = Property(**property_data.dict(), created_by_id=user_id)
            self.db.add(property)
            self.db.commit()
            self.db.refresh(property)
            return property
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    def create_images(self, image_data:List[ImageRequest], property_id:str) -> Optional[bool]:
        try:
            for image in image_data:
                img = Image(**image, property_id=property_id)
                self.db.add(img)
                self.db.commit()
                self.db.refresh(img)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def create_location(self, location_data: LocationBase)-> Optional[str]:
        try:
            location = Location(**location_data.dict())
            self.db.add(location)
            self.db.commit()
            self.db.refresh(location)
            return location.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_property(self, property_id: UUID) -> Optional[Property]:
        return self.db.query(Property)\
            .options(joinedload(Property.location), joinedload(Property.pictures))\
            .filter(Property.id == property_id)\
            .first()
    def delete_property(self, property_id: UUID) -> bool:
        try:
            property = self.get_property(property_id)
            if property:
                self.db.delete(property)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_properties( 
        self,
        request: Request,
        offset: int = 0,
        limit: int = 10,
        filters: Optional[list] = None) -> PaginatedResult:
        base_query = select(Property).options(
                joinedload(Property.location),
                joinedload(Property.pictures)
            )
        filter_conditions = self._build_filters(filters or {})
            
        query, total = get_paginated_query(
                base_query, 
                self.db, 
                offset, 
                limit, 
                filter_conditions
            )
            
        results = self.db.execute(query).unique().scalars().all()
        return PaginatedResult(
                items=results,
                total=total,
                offset=offset,
                limit=limit,
                request=request,
                route_name="fetch_properties"
            )

    def update_property(self, property_id: UUID, property_data: PropertyDBCreate) -> Optional[Property]:
        try:
            property = self.get_property(property_id)
            if not property:
                return None

            for key, value in property_data.dict(unset=True).items():
                setattr(property, key, value)

            self.db.commit()
            self.db.refresh(property)
            return property
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_premium_properties(
        self,
        request: Request,
        offset: int = 0,
        limit: int = 10,
        filters: Optional[list] = None
    ):
        base_query = select(Property).options(
            joinedload(Property.location),
            joinedload(Property.pictures)
        ).join(Location).join(HomeOwners)

        base_query = base_query.filter(
            HomeOwners.type == OwnerType.PREMIUM.value
        )
        query, total = get_paginated_query(
                base_query, 
                self.db, 
                offset, 
                limit, 
                filters
            )
            
        results = self.db.execute(query).unique().scalars().all()
        
        return PaginatedResult(
                items=results,
                total=total,
                offset=offset,
                limit=limit,
                request=request,
                route_name="get_premium_property"
            )


    def search_properties(self, filters: Dict) -> List[Property]:
        query = self.db.query(Property).options(
            joinedload(Property.location),
            joinedload(Property.pictures)
        ).join(Location)

        if search_term := filters.get('search'):
            query = query.filter(
                or_(
                    Property.name.ilike(f"%{search_term}%"),
                    Property.description.ilike(f"%{search_term}%"),
                    Location.name.ilike(f"%{search_term}%")
                )
            )

        if property_types := filters.get('type'):
            if isinstance(property_types, str):
                property_types = [property_types]
            query = query.filter(Property.type.in_(property_types))

        if status := filters.get('status'):
            status = status.lower()
            if status == 'sold':
                query = query.filter(Property.sold_out.is_(True))
            elif status == 'rental':
                query = query.filter(and_(
                    Property.sold_out.is_(False),
                    Property.rental.is_(True)
                ))

        if min_price := filters.get('min_price'):
            query = query.filter(Property.price >= min_price)
        if max_price := filters.get('max_price'):
            query = query.filter(Property.price <= max_price)

        if bedrooms := filters.get('bedroom'):
            query = query.filter(Property.bedroom == bedrooms)
        if bathrooms := filters.get('bathroom'):
            query = query.filter(Property.bathroom == bathrooms)

        if furnished := filters.get('furnished'):
            query = query.filter(Property.furnished.is_(furnished))

        if all(key in filters for key in ['min_lat', 'min_lng', 'max_lat', 'max_lng']):
            query = query.filter(and_(
                Location.latitude >= filters['min_lat'],
                Location.longitude >= filters['min_lng'],
                Location.latitude <= filters['max_lat'],
                Location.longitude <= filters['max_lng']
            ))

        if all(key in filters for key in ['lat', 'lng', 'radius']):
            query = query.filter(
                text("ST_DWithin(ST_MakePoint(location.longitude, location.latitude)::geography, "
                    "ST_MakePoint(:lng, :lat)::geography, :radius)")
            ).params(
                lat=filters['lat'],
                lng=filters['lng'],
                radius=filters['radius']
            )

        sort_by = filters.get('sort_by', '-created_at')
        if sort_by == 'price_asc':
            query = query.order_by(Property.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Property.price.desc())
        else:
            query = query.order_by(Property.created_at.desc())

        return query.all()

    def get_properties_in_bounds(self, min_lat: float, min_lng: float, 
                               max_lat: float, max_lng: float) -> List[Property]:
        return self.db.query(Property)\
            .join(Location)\
            .filter(and_(
                Location.latitude >= min_lat,
                Location.longitude >= min_lng,
                Location.latitude <= max_lat,
                Location.longitude <= max_lng
            ))\
            .all()

    def get_monthly_property_data(self) -> Dict:
        result = self.db.query(
                func.date_trunc('month', Property.created_at).label('month'),
                func.count(Property.id).label('count')
            )\
            .group_by('month')\
            .order_by('month')\
            .all()

        return {
            "labels": [row[0].strftime('%B %Y') for row in result],
            "series": [row[1] for row in result]
        }

    def get_property_stats(self) -> Dict:
        labels = [
            'Luxury Apartment', 'Apartment', 'Office Space', 
            'Single Family', 'Condominium', 'Plot Land',
            'Penthouse', 'Townhouse', 'Villa', 'Commercial', 'Warehouse'
        ]

        series = [
            self.db.query(Property).filter(Property.type == label).count()
            for label in labels
        ]

        return {"labels": labels, "series": series}

    # def get_admin_property_stats(self) -> Dict:
    #     wishlist_counts = self.db.query(
    #             Property.id,
    #             func.count(SearchHistory.id).label('wishlist_count')
    #         )\
    #         .join(SearchHistory.properties)\
    #         .group_by(Property.id)\
    #         .subquery()

    #     result = self.db.query(
    #             func.sum(wishlist_counts.c.wishlist_count).label('total_wishlists'),
    #             func.max(wishlist_counts.c.wishlist_count).label('max_wishlists')
    #         )\
    #         .first()

    #     return {
    #         "total_wishlisted": result[0] or 0,
    #         "most_wishlisted": result[1] or 0
    #     }

    def toggle_sold_status(self, property_id: UUID) -> Optional[Property]:
        try:
            property = self.get_property(property_id)
            if property:
                property.sold_out = not property.sold_out
                self.db.commit()
                self.db.refresh(property)
            return property
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_nearby_properties(self, lat: float, lng: float, radius: float) -> List[Property]:
        query = text("""
            SELECT p.*
            FROM properties p
            JOIN locations l ON p.location_id = l.id
            WHERE ST_DWithin(
                ST_MakePoint(l.longitude, l.latitude)::geography,
                ST_MakePoint(:lng, :lat)::geography,
                :radius
            )
        """)

        return self.db.execute(
            query,
            {"lat": lat, "lng": lng, "radius": radius}
        ).fetchall()

    def increment_impression_count(self, property_id: UUID) -> None:
        try:
            self.db.query(Property)\
                .filter(Property.id == property_id)\
                .update({Property.impression_count: Property.impression_count + 1})
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def apply_discount(self, property_id: UUID, discount: float) -> Optional[Property]:
        try:
            property = self.get_property(property_id)
            if property:
                property.discount = discount
                self.db.commit()
                self.db.refresh(property)
            return property
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e