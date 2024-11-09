from typing import List
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from .db import Base
import uuid


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


class House(Base):
    __tablename__ = "house"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    floors: Mapped[List["Floor"]] = relationship()
    image = Column(String)
    address = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)


class Floor(Base):
    __tablename__ = "floor"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    height = Column(Integer)
    house_id: Mapped[UUID] = mapped_column(ForeignKey("house.uuid"), nullable=True)
    objects: Mapped[List["Object3D"]] = relationship()

    # svg
    # svg_model
    # svg_simplified


class Object3D(Base):
    __tablename__ = "objects3D"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    floor_id: Mapped[UUID] = mapped_column(ForeignKey("floor.uuid"), nullable=True)


class UploadedFile(Base):
    __tablename__ = "uploaded_file"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_type = Column(String)
