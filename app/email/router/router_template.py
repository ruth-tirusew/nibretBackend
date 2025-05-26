from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.email.models import *
from ..service import Service, get_service
from . import router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/", auto_error=True)

@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=TemplateResponse
)
def add_template(
    input: TemplateBase,
    svc: Service = Depends(get_service),
):
    return svc.create_template(input)

@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=GetAllResponse
)
def get_all_templates(
    svc: Service=Depends(get_service)
): 
    return svc.get_all_templates()