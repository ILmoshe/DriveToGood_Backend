from enum import Enum
from typing import Optional
import datetime

import pymongo
from pydantic import BaseModel, Field, ValidationError, validator
from beanie import Document, Indexed
from beanie import PydanticObjectId

from ..helpers.util import random_room


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


class BaseDrive(BaseModel):
    id: Optional[PydanticObjectId]
    id_user: Optional[PydanticObjectId]
    ver: DriveType
    location: Indexed(dict, index_type=pymongo.GEOSPHERE)
    to: dict
    body: str
    status: Status = Status.pending
    header: str
    city: str
    dst_city: str
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @validator('header')
    def header_most_32_chars(cls, v):
        if len(v) > 40:
            raise ValueError("header too long")
        return v.title()


class Drive(Document, BaseDrive):
    room_id: str = Field(default_factory=random_room)

    class Config:
        schema_extra = {
            'example':
                {
                    'ver': 'transporting_patient',
                    'location': {
                        'type': "Point",
                        'coordinates': [34, 34]
                    },
                    'to': {
                        'type': "Point",
                        'coordinates': [35, 35]
                    },
                    'body': 'This is the body of the Drive',
                    'status': 'pending',
                    'header': 'This is my Stupid Header',
                    'city': 'Petha Tikwa',
                    'dst_city': 'Jerusalem',
                }
        }


class ShowDrive(Document, BaseDrive):
    pass


class UpdateDrive(BaseModel):
    type: DriveType
    location: Indexed(LocationDD, index_type=pymongo.GEOSPHERE)
    body: str
    is_completed: bool
