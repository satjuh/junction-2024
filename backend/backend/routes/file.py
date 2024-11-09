import uuid
import aiofiles
import os
from fastapi import Depends, UploadFile, APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import json

from backend import models, schemas
from backend.db import get_db
from backend.models import UploadedFile
from backend.process import (
    pdf_to_nparray,
    create_simple_floorplan,
    array_into_png,
    png_to_nparray,
)
from backend.numpy_to_glb import image_data_to_glb
from backend.floor import create_simple_floor

router = APIRouter()

file_folder = "files"


@router.post("/file/")
async def upload_file(in_file: UploadFile, db: Session = Depends(get_db)):
    try:
        os.makedirs(file_folder)
    except FileExistsError:
        pass

    img_bytes = await in_file.read()
    content_type = in_file.content_type
    img = 0
    if content_type == "application/pdf":
        # Handle PDF to NumPy array conversion
        img = pdf_to_nparray(img_bytes)
    elif content_type == "image/png":
        # Handle PNG to NumPy array conversion
        img = png_to_nparray(img_bytes)

    # img = pdf_to_nparray(img)
    # img = np.array(convert_from_path("/root/code/Hackathon/junction-2024/backend/floor_1.pdf", grayscale=True)).astype(np.float32)[0]
    img2 = img.copy()
    walls = create_simple_floorplan(img, 9, 190, 1500, 20)
    floor = create_simple_floor(img2, 5, 190, 1500, 20)
    with open("/tmp/floor.png", "wb") as f:
        f.write(array_into_png(floor))
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
        walls,
        floor_ceiling_data=floor,
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

    file_uuid3 = uuid.uuid4()
    filename = os.path.join(file_folder, str(file_uuid3))
    u_file = UploadedFile(uuid=file_uuid3, content_type=in_file.content_type)
    db.add(u_file)
    image_data_to_glb(
        walls,
        floor_ceiling_data=floor,
        output_filename=filename + ".glb",
        wall_height=2.5,  # Set realistic wall height in meters
        floor_height=0.25,
        ceiling_height=0.25,
        buffer_distance=0.1,
        walls=True,
        floor=True,
        ceiling=False,
        scaling_factor=0.07,  # Pass the scaling factor
        scaling_method="resize",  # Choose the scaling method
        contour_filter=1.0,  # Filter out small contours
    )
    os.rename(filename + ".glb", filename)
    db.commit()

    return {
        "floor_png": file_uuid,
        "floor_3D": file_uuid2,
        "floor_3D_walls": file_uuid3,
    }


@router.get("/file/{file_uuid}")
async def get_file(file_uuid: uuid.UUID):
    filename = os.path.join(file_folder, str(file_uuid))
    return FileResponse(path=filename, filename=str(file_uuid))


@router.post("/file/3d-model")
async def upload_3d_model(
    data: str, in_file: UploadFile, db: Session = Depends(get_db)
):
    try:
        os.makedirs(file_folder)
    except FileExistsError:
        pass

    img_bytes = await in_file.read()

    file_uuid = uuid.uuid4()
    filename = os.path.join(file_folder, str(file_uuid))
    u_file = UploadedFile(uuid=file_uuid, content_type=in_file.content_type, data=data)
    db.add(u_file)
    async with aiofiles.open(filename, "wb+") as out_file:
        await out_file.write(img_bytes)

    db.commit()

    return file_uuid


@router.get("/files", response_model=List[schemas.File])
def get_files(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.UploadedFile).offset(skip).limit(limit).all()
