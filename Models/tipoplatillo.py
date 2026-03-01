from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Config.DatabaseConn import Base
# DTOs Pydantic
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column

class TipoPlatillo(Base):
    __tablename__ = "tipo_platillos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categoria: Mapped[str] = mapped_column(String, nullable=False)

class TipoPlatilloCreate(BaseModel):
    categoria: str

class TipoPlatilloRead(TipoPlatilloCreate):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)