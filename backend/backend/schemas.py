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
    image: str
    description: str
    address: str
    longitude: float
    latitude: float


class HouseCreate(HouseBase):
    pass


class House(HouseBase):
    uuid: UUID
    floors: Optional[List[Floor]]

    class Config:
        from_attributes = True


class FloorBase(BaseModel):
    name: Optional[str]
    height: Optional[int]
    index: Optional[int]
    floor_3D: Optional[UUID]
    floor_png: Optional[UUID]
    house_id: Optional[UUID]


class FloorCreate(FloorBase):
    pass


class FloorUpdate(FloorBase):
    name: Optional[str]


class Floor(FloorBase):
    uuid: UUID
    objects: Optional[List[Object3D]]

    class Config:
        from_attributes = True


class Object3DBase(BaseModel):
    name: str
    x: float
    y: float
    z: float
    data: str
    rotation: float
    data: str
    file_uuid: UUID


class Object3DCreate(Object3DBase):
    floor_id: UUID


class Object3D(Object3DBase):
    uuid: UUID

    class Config:
        from_attributes = True


class File(BaseModel):
    uuid: UUID
    content_type: str
    data: str | None

    class Config:
        from_attributes = True
