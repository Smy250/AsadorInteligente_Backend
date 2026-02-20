import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from Config.DatabaseConn import getDictionary

def createDB() -> int | None:
  # Parámetros de conexión (ajusta según tu entorno)
  nombre_db = "AsadorInteligente"
  enVariables = getDictionary()

  # Conexión al servidor (no a una base específica)
  conn = psycopg2.connect(
      dbname="postgres",
      user=enVariables["user"],
      password=enVariables["password"],
      host=enVariables["host"],
      port=enVariables["port"]
  )
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cur = conn.cursor()

  # Crea la base de datos si no existe
  cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{nombre_db}'")
  existe = cur.fetchone()
  
  if existe:
      cur.close()
      conn.close()
      return 0
  
  cur.execute(f'CREATE DATABASE "{nombre_db}"')
  
  cur.close()
  conn.close()
  
  return 1