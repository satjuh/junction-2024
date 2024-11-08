from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True


class HouseBase(BaseModel):
    name: str


class HouseCreate(HouseBase):
    pass

class House(HouseBase):
    uuid: UUID
    floors: Optional[List[Floor]]

    class Config:
        from_attributes = True

class FloorBase(BaseModel):
    name: str

class FloorCreate(FloorBase):
    house_id : UUID

class Floor(FloorBase):
    uuid: UUID 
    objects: Optional[List[Object3D]] 

    class Config:
        from_attributes = True

class Object3DBase(BaseModel):
    name: str

class Object3DCreate(Object3DBase):
    floor_id: UUID

class Object3D(Object3DBase):
    uuid: UUID

    class Config:
        from_attributes = True
