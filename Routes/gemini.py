from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import get_db
from Config.geminiConnection import chat as sesionGemini, consulta_agente_pro

router = APIRouter()

@router.post("/respuesta_ia/")
def obtener_metodo_pago(info: dict, db: Session = Depends(get_db)):
  res = consulta_agente_pro("", info['respuesta'], sesionGemini)
  return res