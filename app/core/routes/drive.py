from typing import Optional

from fastapi import APIRouter, Depends

from beanie import PydanticObjectId

from ..models.drive import Drive, UpdateDrive, LocationDD, ShowDrive, DriveType
from ..models.user import User
from ..crud.drive import create, update, read
from ..routes.user import get_current_active_user

router = APIRouter(prefix="/drive", tags=["drive"])


@router.post("/create", response_model=Drive)
async def create_drive(drive: Drive, current_user: User = Depends(get_current_active_user)):
    drive.id_user = current_user.id
    return await create(drive)


@router.put("/update")
async def update_drive(updated_drive: UpdateDrive, doc_id: PydanticObjectId):
    # TODO: Add validation
    return await update(updated_drive, doc_id)


@router.get("/drives", response_model=list[Drive])
async def get_drives(longitude: float, latitude: float, skip: int = 0, limit: int = 5,
                     drive_type: DriveType = DriveType.All):
    # TODO: Add validation and PROJECTION
    """
    Projection could be based on:
        1. drive type
        2.

    """
    print(drive_type)
    data = LocationDD(**{"_type": "Point", "coordinates": [longitude, latitude]})
    return await read(data, skip, limit)


@router.get("/is-host/{drive_id}/{current_user_id}")
async def is_host(drive_id: PydanticObjectId, current_user_id: PydanticObjectId):
    found = await Drive.find_one(Drive.id == drive_id, Drive.id_user == current_user_id)
    return True if found else False
