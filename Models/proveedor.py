from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped

class Proveedor(Base):
    __tablename__ = "proveedores"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String)
    contacto: Mapped[str] = Column(String)
    created_at: Mapped[TIMESTAMP] = Column(TIMESTAMP, server_default=func.now())
    update_at: Mapped[TIMESTAMP] = Column(TIMESTAMP, server_default=func.now())

class ProveedorCreate(BaseModel):
    nombre: str
    contacto: str

class ProveedorRead(ProveedorCreate):
    id: uuid.UUID
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)
