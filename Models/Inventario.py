# DTOs Pydantic
import decimal
import uuid

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from sqlalchemy import DECIMAL, TIMESTAMP, UUID, String, func
from sqlalchemy.orm import mapped_column, relationship, Mapped
from Config.DatabaseConn import Base


class Inventario(Base):
    __tablename__ = "inventario"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_insumo: Mapped[str] = mapped_column(String, nullable=False)
    categoria: Mapped[str] = mapped_column(String, nullable=False)
    cantidad: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    precio_compra: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    update_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    
    receta_platillos: Mapped[list['RecetaPlatillo']] = relationship(back_populates="insumo") # type: ignore
    recurso_insumos: Mapped[list['Recursos']] = relationship(back_populates="detalles_inventario") #type: ignore


class InventarioCreate(BaseModel):
    nombre_insumo: str
    categoria: str
    cantidad: int
    precio_compra: decimal.Decimal


class InventarioRead(InventarioCreate):
    id: uuid.UUID
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)
