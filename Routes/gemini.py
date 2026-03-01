from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import get_db
from Config.geminiConnection import chat as sesionGemini, consulta_agente_pro

router = APIRouter()

@router.post("/respuesta_ia/")
def obtener_metodo_pago(respuesta: str, db: Session = Depends(get_db)):
  res = consulta_agente_pro("", respuesta, sesionGemini)
  return res