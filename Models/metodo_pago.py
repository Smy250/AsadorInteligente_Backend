from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Config.DatabaseConn import Base, engine
from pydantic import BaseModel, ConfigDict # DTOs Pydantic

class MetodoPago(Base):
    __tablename__ = "metodo_pago"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String)

class MetodoPagoCreate(BaseModel):
    nombre: str

class MetodoPagoRead(MetodoPagoCreate):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
