from sqlalchemy import String,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from Config.DatabaseConn import Base
from pydantic import BaseModel, ConfigDict # DTOs Pydantic

class MetodoPago(Base):
    __tablename__ = "metodos_pago"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    
    #Relación
    registros_de_pagos: Mapped[list['RegistroDePagos']] = relationship(back_populates="metodo_pago")   # type: ignore

class MetodoPagoCreate(BaseModel):
    nombre: str

class MetodoPagoRead(MetodoPagoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
