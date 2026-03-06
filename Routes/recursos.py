from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Models.recursos import RecursosRead, Recursos, RecursosCreate
from Config.DatabaseConn import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recursos/", response_model=RecursosRead)
def crear_recurso(recurso: RecursosCreate, db: Session = Depends(get_db)):
    db_recursos = Recursos(**recurso.model_dump())
    db.add(db_recursos)
    db.commit()
    db.refresh(db_recursos)
    return db_recursos

@router.get("/recursos/{recursos_id}", response_model=RecursosRead)
def obtener_recurso(recurso_id: str, db: Session = Depends(get_db)):
    recurso = db.query(Recursos).filter(Recursos.id == recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return recurso

@router.get("/recursos/", response_model=list[RecursosRead])
def listar_recursos(db: Session = Depends(get_db)):
    return db.query(Recursos).all()

@router.put("/recursos/{recurso_id}", response_model=RecursosRead)
def modificar_recurso(id_recurso: str, id_insumo: str, receta: RecursosCreate, db: Session = Depends(get_db)):
    recurso = db.query(Recursos).filter(Recursos.id == id_recurso, Recursos.id_insumo == id_insumo).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    for key, value in receta.model_dump().items():
        setattr(recurso, key, value)
    db.commit()
    db.refresh(recurso)
    return recurso

@router.delete("/recursos/{recurso_id}")
def eliminar_recurso(id_recurso: str, id_insumo: str, db: Session = Depends(get_db)):
    recurso = db.query(Recursos).filter(Recursos.id == id_recurso, Recursos.id_insumo == id_insumo).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrada")
    db.delete(recurso)
    db.commit()
    return {"ok": True}