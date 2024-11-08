from uuid import UUID
from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from ..db import get_db
from fastapi import APIRouter

import uuid

router = APIRouter()

@router.post("/houses/", response_model=schemas.House)
def create_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    db_house = models.House(
        name=house.name, 
        uuid=uuid.uuid4(), 
        image=house.image, 
        description=house.description, 
        address=house.address,
        longitude=house.longitude,
        latitude=house.latitude,
    )
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


@router.get("/houses/{house_id}", response_model=schemas.House)
def read_house(house_id: UUID, db: Session = Depends(get_db)):
    db_house = db.query(models.House).filter(models.House.uuid == house_id).first()
    if db_house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return db_house

@router.get("/houses/", response_model=list[schemas.House])
def read_houses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.House).offset(skip).limit(limit).all()
