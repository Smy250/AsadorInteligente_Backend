from decimal import Decimal

from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RegistroDePagos(Base):
    __tablename__ = "registro_de_pagos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_platillo = Column(UUID(as_uuid=True), ForeignKey("platillos.id"), nullable=False)
    id_metodo_pago = Column(UUID(as_uuid=True), ForeignKey("metodo_pago.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    total_venta = Column(DECIMAL)
    created_at = Column(TIMESTAMP, server_default=func.now())

class RegistroDePagosCreate(BaseModel):
    id_platillo: uuid.UUID
    id_metodo_pago: uuid.UUID
    cantidad: int
    total_venta: Decimal

class RegistroDePagosRead(RegistroDePagosCreate):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
