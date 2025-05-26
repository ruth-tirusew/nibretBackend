from fastapi import APIRouter

from app.utils import import_routers

router = APIRouter(prefix='/notification', tags=['Notification'])
import_routers(__name__)
