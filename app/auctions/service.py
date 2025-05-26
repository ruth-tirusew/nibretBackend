from app.config import database
from app.auctions.repository.repository import AuctionRepository


class Service:
    def __init__(self,db):
        self.repository = AuctionRepository(db)


def get_service():
    svc = Service(database)
    return svc
