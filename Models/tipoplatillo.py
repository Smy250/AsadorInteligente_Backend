from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict

class TipoPlatillo(Base):
    __tablename__ = "tipo_platillo"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categoria = Column(String, nullable=False)

class TipoPlatilloCreate(BaseModel):
    categoria: str

class TipoPlatilloRead(TipoPlatilloCreate):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)