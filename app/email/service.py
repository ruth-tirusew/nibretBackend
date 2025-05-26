from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jinja2 import Template
from typing import Annotated, Optional, List

from app.config import database, env
from app.email.models import *
from app.email.repository.repository import EmailRepository
from app.email.utils.helpers import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/")
SECRET=env.SECRET

BASE_DOC = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        {template_html}
    </body>
</html>
"""


class Service:
    def __init__(self, db) -> None:
        self.repository = EmailRepository(db)
       
    def create_template(self, template:TemplateBase):
        is_renderable(template.content)
        return self.repository.create_template(template.dict())


    def get_template_by_id(self, id: str):
        template =  self.repository.get_template_by_id(id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Template doesn't exist.",
            )
        return template

    def get_all_templates(self)->GetAllResponse:
        templates =  self.repository.get_all_templates()
        return {
            "templates": templates
        }
        


def get_service():
    svc = Service(database)
    return svc
