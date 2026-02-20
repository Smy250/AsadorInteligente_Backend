from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.Inventario import InventarioCreate, InventarioRead, Inventario

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/inventario/", response_model=InventarioRead)
def crear_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = Inventario(**inventario.model_dump())
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

@router.get("/inventario/{inventario_id}", response_model=InventarioRead)
def obtener_inventario(inventario_id: str, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@router.get("/inventario/", response_model=list[InventarioRead])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@router.put("/inventario/{inventario_id}", response_model=InventarioRead)
def modificar_inventario(inventario_id: str, inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    for key, value in inventario.model_dump().items():
        setattr(db_inventario, key, value)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

@router.delete("/inventario/{inventario_id}")
def eliminar_inventario(inventario_id: str, db: Session = Depends(get_db)):
    db_inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    db.delete(db_inventario)
    db.commit()
    return {"ok": True}
