import uuid

from sqlalchemy import Column, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict

class RecetaPlatillo(Base):
    __tablename__ = "receta_platillo"
    id_platillo = Column(UUID(as_uuid=True), ForeignKey("platillos.id"), primary_key=True)
    id_insumo = Column(UUID(as_uuid=True), ForeignKey("inventario.id"), primary_key=True)
    cantidad_usada = Column(DECIMAL)

class RecetaPlatilloCreate(BaseModel):
    id_platillo: uuid.UUID
    id_insumo: uuid.UUID
    cantidad_usada: float

class RecetaPlatilloRead(RecetaPlatilloCreate):
    model_config = ConfigDict(from_attributes=True)