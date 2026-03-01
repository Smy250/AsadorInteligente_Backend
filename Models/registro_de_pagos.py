from decimal import Decimal
from typing import List
from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped, relationship
from Config.DatabaseConn import Base

# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RegistroDePagos(Base):
    __tablename__ = "registro_de_pagos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_metodo_pago = Column(UUID(as_uuid=True), ForeignKey("metodo_pago.id"), nullable=False)
    total_venta = Column(DECIMAL)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    detalles: Mapped[List["DetallePago"]] = relationship(
        "DetallePago",
        back_populates="pago",
        cascade="all, delete-orphan"
    )


class PlatilloEnRegistroDePago(BaseModel):
    id_platillo: uuid.UUID
    cantidad: int


class RegistroDePagosCreate(BaseModel):
    platillos: List[PlatilloEnRegistroDePago]
    id_metodo_pago: uuid.UUID
    total_venta: Decimal = 0


class RegistroDePagosRead(RegistroDePagosCreate):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
