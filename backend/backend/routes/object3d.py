from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from ..db import get_db
from fastapi import APIRouter

import uuid

router = APIRouter()


@router.post("/object3ds", response_model=schemas.Object3D)
def create_object3d(object3d: schemas.Object3DCreate, db: Session = Depends(get_db)):
    floor = db.query(models.Floor).filter(models.Floor.uuid == object3d.floor_id).one()
    db_object3d = models.Object3D(
        name=object3d.name,
        uuid=uuid.uuid4(),
        floor_id=floor.uuid,
        x=object3d.x,
        y=object3d.y,
        z=object3d.z,
        rotation=object3d.rotation,
        data=object3d.data,
        file_uuid=object3d.file_uuid,
    )
    db.add(db_object3d)
    db.commit()
    db.refresh(db_object3d)
    return db_object3d


@router.get("/object3ds/{object3d_id}", response_model=schemas.Object3D)
def read_object3d(object3d_id: UUID, db: Session = Depends(get_db)):
    db_object3d = (
        db.query(models.Object3D).filter(models.Object3D.uuid == object3d_id).first()
    )
    if db_object3d is None:
        raise HTTPException(status_code=404, detail="Object3D not found")
    return db_object3d


@router.delete("/object3d/{object3d_id}", response_model=schemas.House)
def delete_object3d(object3d_id: UUID, db: Session = Depends(get_db)):
    db.query(models.Object3D).filter(models.Object3D.uuid == object3d_id).delete()


@router.get("/object3ds/", response_model=list[schemas.Object3D])
def read_object3ds(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Object3D).offset(skip).limit(limit).all()
