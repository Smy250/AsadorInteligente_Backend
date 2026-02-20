# DTOs Pydantic
import uuid

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from sqlalchemy import DECIMAL, TIMESTAMP, UUID, Column, ForeignKey, String, func
from Config.DatabaseConn import Base

class Inventario(Base):
  __tablename__ = "inventario"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  id_proveedor = Column(UUID(as_uuid=True), ForeignKey("proveedor.id"))
  nombre = Column(String, nullable=False)
  categoria = Column(String, nullable=False)
  cantidad = Column(DECIMAL)
  costo_unitario = Column(DECIMAL)
  created_at = Column(TIMESTAMP, server_default=func.now())
  update_at = Column(TIMESTAMP, server_default=func.now())

class InventarioCreate(BaseModel):
  id_proveedor: uuid.UUID
  nombre: str
  categoria: str
  cantidad: float
  costo_unitario: float

class InventarioRead(InventarioCreate):
  id: uuid.UUID
  created_at: datetime
  update_at: datetime
  model_config = ConfigDict(from_attributes=True)