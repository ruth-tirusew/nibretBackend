from fastapi import Depends

from typing import List, Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.commons.models import *
from app.auctions.models import Auction
from app.auctions.repository.repository import AuctionRepository
from app.commons.utils import generate_blurhash

class AuctionService:
    def __init__(self, db: Session):
        self.repository = AuctionRepository(db)

    def create_auction(self, auction_data: Auction, user_id: UUID) -> Auction:
        auction_data_dict = auction_data.dict()
        location = self.repository.create_location(location_data=LocationBase(**auction_data.location.dict()))
        auction_data_dict["location_id"]=location
        auction = self.repository.create_auction(
            auction_data=AuctionDBCreate(**auction_data_dict),
            user_id=user_id
        )

        return auction

    def update_auction(self, auction_id: UUID, auction_data: Auction) -> Auction:
        auction_data_dict = auction_data.dict()
        self._process_images(auction_data_dict)
        
        return self.repository.update_auction(
            auction_id=auction_id,
            auction_data=Auction(**auction_data_dict)
        )

    def _process_images(self, auction_data: dict):
        pictures=[]
        if 'pictures' in auction_data:
            for image_data in auction_data['pictures']:
                image_url=image_data
                blur_hash = generate_blurhash(image_data)
                pictures.append({
                    "image_url": image_data,
                    "blur_hash": blur_hash
                })
        return pictures

    def get_auction(self, auction_id: UUID) -> Auction:
        auction = self.repository.get_auction(auction_id)
        if auction:
            self.repository.increment_impression_count(auction_id)
        return auction


def get_service(db: Session = Depends(get_db)):
    svc = AuctionService(db)
    return svc
