import blurhash
import numpy as np
import requests
from io import BytesIO
from PIL import Image as pil_image
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload, Query
from sqlalchemy.sql import Select
from typing import Optional, List, Tuple

def get_paginated_query(
        query: Select,
        db_session: Session,
        offset: int = 0,
        limit: int = 10,
        filters: Optional[list] = None
    ) -> Tuple[Query, int]:
        if filters:
            query = query.where(*filters)
        
        count_query = select(func.count()).select_from(query.alias())
        total = db_session.execute(count_query).scalar()

        paginated_query = query.offset(offset).limit(limit)
        
        return paginated_query, total

def generate_blurhash(image_url:str)-> str:
    print(image_url)
    image = pil_image.open(BytesIO(requests.get(image_url).content))
    image.thumbnail((50,50))
    numpy_image = np.array(image)
    hash = blurhash.encode(numpy_image, components_x=4, components_y=3)
    return hash