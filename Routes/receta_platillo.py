from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.receta_platillo import RecetaPlatillo, RecetaPlatilloCreate, RecetaPlatilloRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/receta_platillo/", response_model=RecetaPlatilloRead)
def crear_receta_platillo(receta: RecetaPlatilloCreate, db: Session = Depends(get_db)):
    db_receta = RecetaPlatillo(**receta.model_dump())
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta

@router.get("/receta_platillo/{id_platillo}/{id_insumo}", response_model=RecetaPlatilloRead)
def obtener_receta_platillo(id_platillo: str, id_insumo: str, db: Session = Depends(get_db)):
    receta = db.query(RecetaPlatillo).filter(RecetaPlatillo.id_platillo == id_platillo, RecetaPlatillo.id_insumo == id_insumo).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta de platillo no encontrada")
    return receta

@router.get("/receta_platillo/", response_model=list[RecetaPlatilloRead])
def listar_recetas_platillo(db: Session = Depends(get_db)):
    return db.query(RecetaPlatillo).all()

@router.put("/receta_platillo/{id_platillo}/{id_insumo}", response_model=RecetaPlatilloRead)
def modificar_receta_platillo(id_platillo: str, id_insumo: str, receta: RecetaPlatilloCreate, db: Session = Depends(get_db)):
    db_receta = db.query(RecetaPlatillo).filter(RecetaPlatillo.id_platillo == id_platillo, RecetaPlatillo.id_insumo == id_insumo).first()
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta de platillo no encontrada")
    for key, value in receta.model_dump().items():
        setattr(db_receta, key, value)
    db.commit()
    db.refresh(db_receta)
    return db_receta

@router.delete("/receta_platillo/{id_platillo}/{id_insumo}")
def eliminar_receta_platillo(id_platillo: str, id_insumo: str, db: Session = Depends(get_db)):
    db_receta = db.query(RecetaPlatillo).filter(RecetaPlatillo.id_platillo == id_platillo, RecetaPlatillo.id_insumo == id_insumo).first()
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta de platillo no encontrada")
    db.delete(db_receta)
    db.commit()
    return {"ok": True}
