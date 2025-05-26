from fastapi import Depends

from typing import List, Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.properties.models import Property, Image, PropertyCreate,PropertyDBCreate, LocationBase, HomeOwnerRequest, HomeOwnerResponse
from app.properties.repository.repository import PropertyRepository
from app.properties.utils.blurhash import generate_blurhash

class PropertyService:
    def __init__(self, db: Session):
        self.repository = PropertyRepository(db)

    def create_property(self, property_data: PropertyCreate, user_id: UUID) -> Property:
        """Create new property with generated blurhashes for images"""
        property_data_dict = property_data.dict()
        image_data_dict = self._process_images(property_data_dict)
        location = self.repository.create_location(location_data=LocationBase(**property_data.location.dict()))
        property_data_dict["location_id"]=location
        property = self.repository.create_property(
            property_data=PropertyDBCreate(**property_data_dict),
            user_id=user_id
        )

        images=self.repository.create_images(image_data_dict, property.id)
        return property

    def update_property(self, property_id: UUID, property_data: Property) -> Property:
        """Update property with new blurhashes for any updated images"""
        property_data_dict = property_data.dict()
        self._process_images(property_data_dict)
        
        return self.repository.update_property(
            property_id=property_id,
            property_data=Property(**property_data_dict)
        )

    def _process_images(self, property_data: dict):
        """Generate blurhashes for all images in property data"""
        pictures=[]
        if 'pictures' in property_data:
            for image_data in property_data['pictures']:
                image_url=image_data
                blur_hash = generate_blurhash(image_data)
                pictures.append({
                    "image_url": image_data,
                    "blur_hash": blur_hash
                })
        return pictures

    def search_properties(self, filters: Dict) -> List[Property]:
        return self.repository.search_properties(filters)

    def get_property(self, property_id: UUID) -> Property:
        """Get property with impression count increment"""
        property = self.repository.get_property(property_id)
        if property:
            self.repository.increment_impression_count(property_id)
        return property

    def apply_discount(self, property_id: UUID, discount: float) -> Property:
        """Apply discount with business validation"""
        if not 0 <= discount <= 100:
            raise ValueError("Discount must be between 0 and 100 percent")
        return self.repository.apply_discount(property_id, discount)

    def toggle_sold_status(self, property_id: UUID) -> Property:
        """Toggle sold status with additional business checks"""
        property = self.repository.get_property(property_id)
        if property and property.rental:
            raise ValueError("Rental properties cannot be marked as sold")
        return self.repository.toggle_sold_status(property_id)

    def get_premium_properties(self) -> List[Property]:
        """Get premium properties with business logic definition"""
        return self.repository.search_properties({
            'type': ['Luxury Apartment', 'Penthouse', 'Villa'],
            'sort_by': 'price_desc'
        })

    def get_property_stats(self) -> Dict:
        """Get property statistics with formatted output"""
        raw_stats = self.repository.get_property_stats()
        return {
            'labels': raw_stats['labels'],
            'series': [str(count) for count in raw_stats['series']]
        }

    def get_admin_insights(self) -> Dict:
        """Get admin insights with combined business data"""
        stats = self.repository.get_admin_property_stats()
        monthly_data = self.repository.get_monthly_property_data()
        
        return {
            'total_properties': self.repository.get_property_count(),
            'wishlist_stats': stats,
            'monthly_trends': monthly_data
        }

    def bulk_update_status(self, property_ids: List[UUID], status: bool) -> int:
        """Bulk update property status with business validation"""
        if not property_ids:
            return 0
            
        return self.repository.bulk_update(
            property_ids=property_ids,
            update_data={'sold_out': status}
        )
    def create_property_owners(self, property_owner_data: HomeOwnerRequest) -> Optional[HomeOwnerResponse]:
        """Create new property owners"""
        property_owner = self.repository.create_property_owners(property_owner_data)
        return property_owner

    def update_property_owner(self, property_id: UUID, property_data: HomeOwnerRequest) -> Property:
        """Update property owners"""
        property_data_dict = property_data.dict()
        self._process_images(property_data_dict)
        
        return self.repository.update_property(
            property_id=property_id,
            property_data=Property(**property_data_dict)
        )
    
    def get_all_property_owners(self) -> Optional[HomeOwnerResponse]:
        """Get all property owners"""
        property_owner = self.repository.get_property_owners()
        return property_owner


def get_property_service(db: Session = Depends(get_db)):
    svc = PropertyService(db)
    return svc
