import decimal
import uuid

from sqlalchemy import DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict

class RecetaPlatillo(Base):
    __tablename__ = "receta_platillos"
    id_platillo: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("platillos.id"), primary_key=True)
    id_insumo: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventario.id"), primary_key=True)
    cantidad_usada: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    
    platillo: Mapped['Platillo'] = relationship(back_populates="receta_platillos") # type: ignore
    insumo: Mapped['Inventario'] = relationship(back_populates="receta_platillos") # type: ignore
    __table_args__ = (UniqueConstraint('id_platillo', 'id_insumo'),)

class RecetaPlatilloCreate(BaseModel):
    id_platillo: uuid.UUID
    id_insumo: uuid.UUID
    cantidad_usada: float

class RecetaPlatilloRead(RecetaPlatilloCreate):
    model_config = ConfigDict(from_attributes=True)