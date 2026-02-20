from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.platillos import Platillo, PlatilloCreate, PlatilloRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/platillos/", response_model=PlatilloRead)
def crear_platillo(platillo: PlatilloCreate, db: Session = Depends(get_db)):
    db_platillo = Platillo(**platillo.model_dump())
    db.add(db_platillo)
    db.commit()
    db.refresh(db_platillo)
    return db_platillo

@router.get("/platillos/{platillo_id}", response_model=PlatilloRead)
def obtener_platillo(platillo_id: str, db: Session = Depends(get_db)):
    platillo = db.query(Platillo).filter(Platillo.id == platillo_id).first()
    if not platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return platillo

@router.get("/platillos/", response_model=list[PlatilloRead])
def listar_platillos(db: Session = Depends(get_db)):
    return db.query(Platillo).all()

@router.put("/platillos/{platillo_id}", response_model=PlatilloRead)
def modificar_platillo(platillo_id: str, platillo: PlatilloCreate, db: Session = Depends(get_db)):
    db_platillo = db.query(Platillo).filter(Platillo.id == platillo_id).first()
    if not db_platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    for key, value in platillo.model_dump().items():
        setattr(db_platillo, key, value)
    db.commit()
    db.refresh(db_platillo)
    return db_platillo

@router.delete("/platillos/{platillo_id}")
def eliminar_platillo(platillo_id: str, db: Session = Depends(get_db)):
    db_platillo = db.query(Platillo).filter(Platillo.id == platillo_id).first()
    if not db_platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    db.delete(db_platillo)
    db.commit()
    return {"ok": True}
