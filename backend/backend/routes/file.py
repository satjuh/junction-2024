import uuid
import aiofiles
import os

from fastapi import Depends, UploadFile, APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from backend import models, schemas
from backend.db import get_db
from backend.models import UploadedFile


router = APIRouter()

file_folder = "files"


@router.post("/file/", response_model=uuid.UUID)
async def upload_file(in_file: UploadFile, db: Session = Depends(get_db)):
    file_uuid = uuid.uuid4()
    filename = os.path.join(file_folder, str(file_uuid))
    u_file = UploadedFile(uuid=file_uuid, content_type=in_file.content_type)
    db.add(u_file)
    db.commit()

    try:
        os.makedirs(file_folder)
    except FileExistsError:
        pass

    async with aiofiles.open(filename, "wb+") as out_file:
        content = await in_file.read()
        await out_file.write(content)
    return file_uuid


@router.get("/file/{file_id}")
async def get_file(file_uuid: uuid.UUID):
    filename = os.path.join(file_folder, str(file_uuid))
    return FileResponse(path=filename, filename=str(file_uuid))


@router.get("/files", response_model=List[schemas.File])
def get_files(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.UploadedFile).offset(skip).limit(limit).all()
