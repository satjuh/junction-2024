from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from ..db import get_db
from fastapi import APIRouter

router = APIRouter()


@router.post("/floor", response_model=schemas.Floor)
def create_floor(floor: schemas.FloorCreate, db: Session = Depends(get_db)):
    house = db.query(models.House).filter(models.House.uuid == floor.house_id).one()
    db_floor = models.Floor(name=floor.name, house_id=house.uuid)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor


@router.get("/floors/{floor_id}", response_model=schemas.Floor)
def read_floor(floor_id: UUID, db: Session = Depends(get_db)):
    db_floor = db.query(models.Floor).filter(models.Floor.uuid == floor_id).first()
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return db_floor


@router.delete("/floor/{floor_id}", response_model=UUID)
def read_house(floor_id: UUID, db: Session = Depends(get_db)):
    db.query(models.Floor).filter(models.Floor.uuid == floor_id).delete()
    return UUID


@router.put("/floor/{floor_id}")
def update_floor(
    floor_id: UUID, floor: schemas.FloorCreate, db: Session = Depends(get_db)
):
    new_floor = db.query(models.Floor).filter(models.Floor.uuid == floor_id).one()

    if new_floor.floor_png is not None:
        new_floor.floor_png = floor.floor_png
    if new_floor.floor_3D is not None:
        new_floor.floor_3D = floor.floor_3D
    if new_floor.height is not None:
        new_floor.height = floor.height
    if new_floor.name is not None:
        new_floor.name = floor.name
    if new_floor.index is not None:
        new_floor.index = floor.index
    try:
        db.add(new_floor)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed")
    return ""


@router.get("/floors", response_model=list[schemas.Floor])
def read_floors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Floor).offset(skip).limit(limit).all()
