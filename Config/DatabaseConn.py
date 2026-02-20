# Importacion para variables de entorno del proyecto.
import os # Os, necesario para obtener las variables del archivo .env
from dotenv import load_dotenv # librería con la lógica clave de importación de .env
from sqlalchemy.orm import declarative_base, sessionmaker  # declarative_base: clase base para modelos ORM (SQLAlchemy 2.0) 
from sqlalchemy import create_engine  # Column: define create_engine: 

load_dotenv()

def getDictionary():
  return {
  "user" : os.getenv("user"),
  "password" : os.getenv("password"),
  "host" : os.getenv("host"),
  "port" : os.getenv("port"),
  "db": os.getenv("db")
  }

def getDatabaseConnection():
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("db")
    return f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

# URL de la base de datos
DATABASE_URL = getDatabaseConnection()
# Clase base para modelos ORM
Base = declarative_base()
# Crea el motor de la base de datos (conexión)
engine = create_engine(DATABASE_URL)
# Crea la fábrica de sesiones para la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()