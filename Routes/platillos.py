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

@router.get("/platillos/{platillo_id}", response_model=PlatilloRead)
def obtener_platillo(platillo_id: str, db: Session = Depends(get_db)):
    platillo = db.query(Platillo).filter(Platillo.id == platillo_id).first()
    if not platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return platillo

@router.get("/platillos/", response_model=list[PlatilloRead])
def listar_platillos(db: Session = Depends(get_db)):
    return db.query(Platillo).all()
