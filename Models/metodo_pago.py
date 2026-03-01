from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from Config.DatabaseConn import Base
from pydantic import BaseModel, ConfigDict # DTOs Pydantic

class MetodoPago(Base):
    __tablename__ = "metodos_pago"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String)
    
    #Relación
    registros_de_pagos: Mapped[list['RegistroDePagos']] = relationship(back_populates="metodo_pago")   # type: ignore

class MetodoPagoCreate(BaseModel):
    nombre: str

class MetodoPagoRead(MetodoPagoCreate):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
