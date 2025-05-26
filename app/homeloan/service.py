from app.config import database
from app.homeloan.repository.repository import HomeloanRepository


class Service:
    def __init__(self,db):
        self.repository = HomeloanRepository(db)


def get_service():
    svc = Service(database)
    return svc
