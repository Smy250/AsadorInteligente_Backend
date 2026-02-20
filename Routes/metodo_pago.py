from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.metodo_pago import MetodoPago, MetodoPagoCreate, MetodoPagoRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/metodos_pago/", response_model=MetodoPagoRead)
def crear_metodo_pago(metodo: MetodoPagoCreate, db: Session = Depends(get_db)):
    db_metodo = MetodoPago(**metodo.model_dump())
    db.add(db_metodo)
    db.commit()
    db.refresh(db_metodo)
    return db_metodo

@router.get("/metodos_pago/{metodo_id}", response_model=MetodoPagoRead)
def obtener_metodo_pago(metodo_id: str, db: Session = Depends(get_db)):
    metodo = db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()
    if not metodo:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return metodo

@router.get("/metodos_pago/", response_model=list[MetodoPagoRead])
def listar_metodos_pago(db: Session = Depends(get_db)):
    return db.query(MetodoPago).all()

@router.put("/metodos_pago/{metodo_id}", response_model=MetodoPagoRead)
def modificar_metodo_pago(metodo_id: str, metodo: MetodoPagoCreate, db: Session = Depends(get_db)):
    db_metodo = db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()
    if not db_metodo:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    for key, value in metodo.model_dump().items():
        setattr(db_metodo, key, value)
    db.commit()
    db.refresh(db_metodo)
    return db_metodo

@router.delete("/metodos_pago/{metodo_id}")
def eliminar_metodo_pago(metodo_id: str, db: Session = Depends(get_db)):
    db_metodo = db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()
    if not db_metodo:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    db.delete(db_metodo)
    db.commit()
    return {"ok": True}
