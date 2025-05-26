from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from app.auctions.models.auction import *
from app.properties.utils.blurhash import generate_blurhash



class AuctionRepository:
    def __init__(self, database: Database):
        self.database = database

    def register_auction(self,auction: Auction) -> Optional[Auction]:
        auction_saved = auction.model_dump()
        # auction_saved['id'] = str(ObjectId())
        images = []
        pictures=auction.pictures
        for picture in pictures:
            picture.blur_hash = generate_blurhash(picture.image_url)
            images.append(picture.model_dump())

        auction_saved['pictures']=images
        self.database["auctions"].insert_one(auction_saved)
        
        return auction_saved

    def get_auction_by_id(self, id: str) -> Optional[Auction]:
        auction = self.database["auctions"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if auction:
            return Auction.model_validate(auction)
    
    def update_auction(self, id:str,auction:Auction)->Optional[Auction]:
        auction_saved = auction.model_dump()
        images = []
        pictures=auction_saved['pictures']
        for picture in pictures:
            picture['blur_hash'] = generate_blurhash(picture['image_url'])
            images.append(picture)

        auction_saved['pictures']=images
        auction = self.database["auctions"].find_one_and_update(
            filter={
                "_id": ObjectId(id),
            },
            update={
                "$set": {
                    **auction_saved}}
            )

        return auction

    def delete_auction(self, id:str)->bool:
        auction = self.database["auctions"].delete_one(
            filter={
                "_id": ObjectId(id),
            },
            )
        return auction.deleted_count >0


    def get_auctions(self)-> Optional[List[AuctionResponse]]:
        auctions = self.database['auctions'].find()
        return auctions


    def get_auctions_by_location(self, coordiantes: List[float])-> Optional[List[AuctionResponse]]:
        auctions =  self.database['auctions'].find({
            "location":{ "$geoWithin": { "$center": [ coordiantes, 5 ] } }})
        return auctions