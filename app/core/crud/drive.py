from fastapi import HTTPException

from beanie import PydanticObjectId

from ..models.drive import Drive, UpdateDrive, LocationDD


async def create(drive: Drive):
    # Check if same user made drive already that he isn't completed:
    is_existed = await Drive.find_one(Drive.status == "pending",
                                      Drive.id_user == drive.id_user)
    if is_existed is not None:
        raise HTTPException(status_code=404, detail="there is a pending drive for the user")

    print("Drive created")
    await Drive.insert(drive)
    return drive


async def read(location: LocationDD, skip, limit):
    """All users should be able to read the drives by the radius

    we want to find the first 5 drives which are most closes to the user location.

    """
    result = await Drive.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [location.coordinates[0], location.coordinates[1]],
                },
            }
        }
    }, Drive.status == "pending").limit(limit).to_list()
    return result


async def update(updated_drive: UpdateDrive, doc_id: PydanticObjectId):
    curr_drive = await Drive.get(doc_id)
    # TODO : add some validation etc
    curr_drive.status = updated_drive.status
    curr_drive.body = updated_drive.body
    curr_drive.type = updated_drive.type
    await curr_drive.save()
    return "resource updated successfully"


async def delete():
    pass
