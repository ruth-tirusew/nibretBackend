import importlib
import pkgutil
from datetime import datetime
from typing import Any, Callable, Optional
from zoneinfo import ZoneInfo

import orjson
from bson.objectid import ObjectId
from pydantic import BaseModel, model_validator


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class AppModel(BaseModel):
    class Config:
        json_encoders = {datetime: convert_datetime_to_gmt, ObjectId: str}
        populate_by_name = True

    @model_validator(mode='before')
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


def import_routers(package_name):
    package = importlib.import_module(package_name)
    prefix = package.__name__ + "."

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, prefix):
        if not module_name.startswith(prefix + "router_"):
            continue

        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"Failed to import {module_name}, error: {e}")
