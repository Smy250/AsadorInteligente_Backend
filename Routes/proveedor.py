from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.proveedor import Proveedor, ProveedorCreate, ProveedorRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/proveedores/", response_model=ProveedorRead)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    db_proveedor = Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.get("/proveedores/{proveedor_id}", response_model=ProveedorRead)
def obtener_proveedor(proveedor_id: str, db: Session = Depends(get_db)):
    proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.get("/proveedores/", response_model=list[ProveedorRead])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(Proveedor).all()

@router.put("/proveedores/{proveedor_id}", response_model=ProveedorRead)
def modificar_proveedor(proveedor_id: str, proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for key, value in proveedor.model_dump().items():
        setattr(db_proveedor, key, value)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.delete("/proveedores/{proveedor_id}")
def eliminar_proveedor(proveedor_id: str, db: Session = Depends(get_db)):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(db_proveedor)
    db.commit()
    return {"ok": True}
