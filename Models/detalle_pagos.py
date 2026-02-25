from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from Config.DatabaseConn import Base
import uuid

class DetallePago(Base):
    __tablename__ = "detalle_pago"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_pago = Column(UUID(as_uuid=True), ForeignKey("registro_de_pagos.id"), nullable=False)
    id_platillo = Column(UUID(as_uuid=True), ForeignKey("platillos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Evita import circular usando string
    pago: Mapped["RegistroDePagos"] = relationship(
        "RegistroDePagos",
        back_populates="detalles"
    )