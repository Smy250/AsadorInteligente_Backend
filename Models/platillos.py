from decimal import Decimal

from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Platillo(Base):
    __tablename__ = "platillos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String)
    precio = Column(DECIMAL, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now())

class PlatilloCreate(BaseModel):
    nombre: str
    precio: Decimal

class PlatilloRead(PlatilloCreate):
    id: uuid.UUID
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)
