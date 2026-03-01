import decimal

from sqlalchemy import String, DECIMAL, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Platillo(Base):
    __tablename__ = "platillos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String, nullable=True)
    precio: Mapped[decimal.Decimal] = mapped_column(DECIMAL, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    update_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, onupdate=func.now())
    
    #Relacion.
    detalles_pago: Mapped[list['DetallePago']] = relationship(back_populates="platillo") # type: ignore
    #registro_pagos: Mapped[list['RegistroDePagos']] = relationship(back_populates="platillo") # type: ignore
    receta_platillos: Mapped[list['RecetaPlatillo']] = relationship(back_populates="platillo") # type: ignore

class PlatilloCreate(BaseModel):
    nombre: str
    precio: decimal.Decimal

class PlatilloRead(PlatilloCreate):
    id: uuid.UUID
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)
