from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Recursos(Base):
    __tablename__ = "recursos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_insumo: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventario.id"), nullable=False)
    cantidad_usada: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    update_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    
    detalles_inventario: Mapped['Inventario'] = relationship(back_populates="recurso_insumos") # type: ignore

class RecursosCreate(BaseModel):
  id_insumo: uuid.UUID
  cantidad_usada: int
  motivo: str

class RecursosRead(RecursosCreate):
  id: uuid.UUID
  created_at: datetime
  update_at: datetime
  model_config = ConfigDict(from_attributes=True)