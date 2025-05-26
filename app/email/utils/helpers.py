from jinja2 import Template as JinjaTemplate
from jinja2 import TemplateSyntaxError

from app.email.utils.errors import *

def is_renderable(template:str):
        try:
            JinjaTemplate(template).render()
        except TemplateSyntaxError as e:
            raise INVALID_TEMPLATE_EXCEPTION