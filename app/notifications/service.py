from app.config import database
from app.notifications.repository.repository import NotificationClientRepository


class Service:
    def __init__(self,db):
        self.repository = NotificationClientRepository(db)

    
    


def get_service():
    svc = Service(database)
    return svc
