from enum import Enum
from typing import Optional

import pymongo
from pydantic import BaseModel
from beanie import Document, Indexed
from beanie import PydanticObjectId


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
    """It is not working in location IDK why"""
    type: str = "Point"
    coordinates: list[float, float]


# Becuase we are using beenie we have the priviliege of making evrything in the same file

# We have UPDATE drive, CREATE drive,
class Drive(Document):
    id_user: Optional[PydanticObjectId]
    ver: DriveType
    location: Indexed(dict, index_type=pymongo.GEOSPHERE)
    body: str
    status: Status = Status.pending

    # class Config:
    #     schema_extra = {
    #         'examples': [
    #             {
    #                 "id_user": "5eb7cf5a86d9755df3a6c593",
    #                 "type": "roadside_assistance",
    #                 "location": {"longitude": 0.232323, "latitude": 0.2323233},
    #                 "body": "Hello friend I would be glad if you can help me",
    #                 "is_completed": False
    #             }
    #         ]
    #     }


class UpdateDrive(BaseModel):
    type: DriveType
    location: Indexed(LocationDD, index_type=pymongo.GEOSPHERE)
    body: str
    is_completed: bool

    # class Config:
    #     schema_extra = {
    #         'examples': [
    #             {
    #                 "type": "roadside_assistance",
    #                 "location": {"longitude": 0.232323, "latitude": 0.2323233},
    #                 "body": "Hello friend I would be glad if you can help me",
    #                 "is_completed": False
    #             }
    #         ]
    #     }
