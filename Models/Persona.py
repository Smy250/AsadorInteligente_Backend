from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict
from Config.DatabaseConn import Base

class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=True)
    apellido = Column(String, nullable=True)
    direccion = Column(String, nullable=True)

# DTO (Data Transfer Object) para crear una Persona (entrada de datos)
class PersonaCreate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    direccion: str | None = None

# DTO para leer una Persona (salida de datos)
class PersonaRead(PersonaCreate):
    id: int  # Incluye el ID al leer

    model_config = ConfigDict(from_attributes=True) # Permite convertir automáticamente desde objetos ORM

