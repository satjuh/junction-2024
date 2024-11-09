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
from backend.process import pdf_to_nparray, create_simple_floorplan, array_into_png
from backend.numpy_to_glb import image_data_to_glb
from backend.floor import create_simple_floor

router = APIRouter()

file_folder = "files"


@router.post("/file/", response_model=uuid.UUID)
async def upload_file(in_file: UploadFile, db: Session = Depends(get_db)):
    try:
        os.makedirs(file_folder)
    except FileExistsError:
        pass

    img = await in_file.read()
    img = pdf_to_nparray(img)
    walls = create_simple_floorplan(img, 9, 190, 1500, 20)
    floor = create_simple_floor(img, 9, 190, 1500, 20)
    png_walls = array_into_png(walls)

    file_uuid = uuid.uuid4()
    filename = os.path.join(file_folder, str(file_uuid))
    u_file = UploadedFile(uuid=file_uuid, content_type=in_file.content_type)
    db.add(u_file)
    async with aiofiles.open(filename, "wb+") as out_file:
        await out_file.write(png_walls)

    file_uuid2 = uuid.uuid4()
    filename = os.path.join(file_folder, str(file_uuid2))
    u_file = UploadedFile(uuid=file_uuid2, content_type=in_file.content_type)
    db.add(u_file)
    image_data_to_glb(
        floor,
        floor_ceiling_data=walls,
        output_filename=filename + ".glb",
        wall_height=2.5,  # Set realistic wall height in meters
        floor_height=0.25,
        ceiling_height=0.25,
        buffer_distance=0.1,
        walls=True,
        floor=True,
        ceiling=True,
        scaling_factor=0.07,  # Pass the scaling factor
        scaling_method="resize",  # Choose the scaling method
        contour_filter=1.0,  # Filter out small contours
    )
    os.rename(filename + ".glb", filename)
    db.commit()

    return [file_uuid, file_uuid2]


@router.get("/file/{file_id}")
async def get_file(file_uuid: uuid.UUID):
    filename = os.path.join(file_folder, str(file_uuid))
    return FileResponse(path=filename, filename=str(file_uuid))


@router.get("/files", response_model=List[schemas.File])
def get_files(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.UploadedFile).offset(skip).limit(limit).all()
