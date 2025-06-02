from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, select, and_
from sqlalchemy.orm import Session, joinedload, Query

from app.auctions.models.auction import *
from app.commons.models import LocationBase
from app.commons.schema import  *
from app.commons.utils.pagination_result import PaginatedResult
from app.commons.utils import generate_blurhash, get_paginated_query
from app.auctions.schema import Auctions, AuctionImages
from app.auctions.models import Auction

class AuctionRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def register_auction(self, auction: Auctions):
        try:
            if auction.location:
                location = Location(**auction.location.dict())
                self.db_session.add(location)
                self.db_session.flush()
            else:
                location = None

            auction_data = auction.dict(exclude={"pictures", "location"})
            db_auction = Auctions(**auction_data)
            
            if location:
                db_auction.location = location

            # Add pictures
            for picture in auction.pictures:
                blur_hash = generate_blurhash(picture.image_url)
                db_picture = AuctionImage(
                    image_url=picture.image_url,
                    blur_hash=blur_hash
                )
                db_auction.pictures.append(db_picture)
            
            self.db_session.add(db_auction)
            self.db_session.commit()
            self.db_session.refresh(db_auction)
            return db_auction
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_auctions(
        self,
        offset: int = 0,
        limit: int = 10,
        filters: Optional[list] = None
    ) -> PaginatedResult[AuctionResponse]:
        try:
            base_query = select(Auctions).options(
                joinedload(Auctions.location),
                joinedload(Auctions.pictures)
            )
            
            query, total = get_paginated_query(
                base_query, 
                self.db_session, 
                offset, 
                limit, 
                filters
            )
            
            results = self.db_session.execute(query).unique().scalars().all()
            return PaginatedResult(
                items=results,
                total=total,
                offset=offset,
                limit=limit
            )
        except Exception as e:
            self.db_session.rollback()
            raise e