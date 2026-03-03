from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.metodo_pago import MetodoPago, MetodoPagoRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metodos_pago/{metodo_id}", response_model=MetodoPagoRead)
def obtener_metodo_pago(metodo_id: int, db: Session = Depends(get_db)):
    metodo = db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()
    if not metodo:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return metodo

@router.get("/metodos_pago/", response_model=list[MetodoPagoRead])
def listar_metodos_pago(db: Session = Depends(get_db)):
    return db.query(MetodoPago).limit(10)
