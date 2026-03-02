from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, Mapped
from Config.DatabaseConn import Base
import uuid

class DetallePago(Base):
    __tablename__ = "detalle_pagos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_pago: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("registro_de_pagos.id"), nullable=False)
    id_platillo: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("platillos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    # Relaciones
    detalles_pago: Mapped['RegistroDePagos'] = relationship(back_populates="pago") # type: ignore
    platillo: Mapped['Platillo'] = relationship(back_populates="detalles_pago") # type: ignore

class DetallePagoCreate(BaseModel):
    id_pago: uuid.UUID
    id_platillo: uuid.UUID
    cantidad: int
