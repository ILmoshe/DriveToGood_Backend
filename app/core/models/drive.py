from enum import Enum
from typing import Optional
import string
import random

import pymongo
from pydantic import BaseModel, Field, ValidationError, validator
from beanie import Document, Indexed
from beanie import PydanticObjectId


def random_room():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(6))
    return result_str


class DriveType(str, Enum):
    transporting_patient = "transporting_patient"
    hospital = "hospital"
    food_distribution = "food_distribution"
    roadside_assistance = "roadside_assistance"
    transportation_of_medical_equipment = "transportation_of_medical_equipment"


class Status(str, Enum):
    pending = "pending"
    occupied = "occupied"
    completed = "completed"


class LocationDD(BaseModel):
    """It is not working with INDEXED idk why"""
    type: str = "Point"
    coordinates: list[float, float]


# Becuase we are using beenie we have the priviliege of making evrything in the same file
class BaseDrive(BaseModel):
    id_user: Optional[PydanticObjectId]
    ver: DriveType
    location: Indexed(dict, index_type=pymongo.GEOSPHERE)
    to: dict
    body: str
    status: Status = Status.pending
    header: str

    @validator('header')
    def header_most_32_chars(cls, v):
        if len(v) > 40:
            raise ValueError("header too long")
        return v.title()


# We have UPDATE drive, CREATE drive,
class Drive(Document, BaseDrive):
    room_id: str = Field(default_factory=random_room)


# TODO: make a model just for showing which exclude room_id(should be secret)
class ShowDrive(BaseDrive):
    pass


class UpdateDrive(BaseModel):
    type: DriveType
    location: Indexed(LocationDD, index_type=pymongo.GEOSPHERE)
    body: str
    is_completed: bool
