from fastapi import APIRouter, Depends

from beanie import PydanticObjectId

from ..models.drive import Drive, UpdateDrive, LocationDD
from ..models.user import User
from ..crud.drive import create, update, read
from ..routes.user import get_current_active_user

router = APIRouter(prefix="/drive", tags=["drive"])


@router.post("/create")
async def create_drive(drive: Drive, current_user: User = Depends(get_current_active_user)):
    drive.id_user = current_user.id
    return await create(drive)


@router.put("/update")
async def update_drive(updated_drive: UpdateDrive, doc_id: PydanticObjectId):
    # TODO: Add validation
    return await update(updated_drive, doc_id)


@router.get("/drives")
async def get_drives(longitude: float, latitude: float, skip: int = 0, limit: int = 5):
    # TODO: Add validation
    data = LocationDD(**{"_type": "Point", "coordinates": [longitude, latitude]})
    return await read(data, skip, limit)
