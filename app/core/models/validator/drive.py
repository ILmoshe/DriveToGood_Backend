""" Module for validation the drive schema/model"""
from pydantic import BaseModel, ValidationError, validator


def ensure_len(field: str, size: int = 10):
    assert len(field) > size, f'{field} is longer then {size} character'
    return field


class DemoModel(BaseModel):
    title: str
    body: str

    _ensure_len = validator('title')(ensure_len)


ensure_len.__annotations__["field"] = "some defult value"
print(ensure_len.__defaults__)
print(ensure_len.__annotations__)

try:
    print(DemoModel(title="WIll work", body="will work"))
    print(DemoModel(title="WIll not work its too long work", body="will work"))
except ValidationError as e:
    print(e, "WAS HERE")
