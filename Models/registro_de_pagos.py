from decimal import Decimal
from typing import List
from sqlalchemy import Integer, DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Config.DatabaseConn import Base

# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RegistroDePagos(Base):
    __tablename__ = "registro_de_pagos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_metodo_pago: Mapped[int] = mapped_column(Integer, ForeignKey("metodos_pago.id"), nullable=False)
    #id_platillo: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("platillos.id"), nullable=False)
    #cantidad: Mapped[int] = mapped_column(Integer)
    total_venta: Mapped[Decimal] = mapped_column(DECIMAL)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    # Relaciónes con DetallePago
    pago: Mapped[list['DetallePago']] = relationship(back_populates="detalles_pago") # type: ignore
    metodo_pago: Mapped['MetodoPago'] = relationship(back_populates="registros_de_pagos") # type: ignore
    #platillo: Mapped['Platillo'] = relationship(back_populates="registro_pagos") # type: ignore


class PlatilloEnRegistroDePago(BaseModel):
    id_platillo: uuid.UUID
    cantidad: int


class RegistroDePagosCreate(BaseModel):
    id_metodo_pago: int
    platillos: List[PlatilloEnRegistroDePago]
    total_venta: Decimal = 0


class RegistroDePagosRead(RegistroDePagosCreate):
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
