from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import SessionLocal
from Models.registro_de_pagos import RegistroDePagos, RegistroDePagosCreate, RegistroDePagosRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro_pagos/", response_model=RegistroDePagosRead)
def crear_registro_pago(registro: RegistroDePagosCreate, db: Session = Depends(get_db)):
    db_registro = RegistroDePagos(**registro.model_dump())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

@router.get("/registro_pagos/{registro_id}", response_model=RegistroDePagosRead)
def obtener_registro_pago(registro_id: str, db: Session = Depends(get_db)):
    registro = db.query(RegistroDePagos).filter(RegistroDePagos.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro de pago no encontrado")
    return registro

@router.get("/registro_pagos/", response_model=list[RegistroDePagosRead])
def listar_registros_pago(db: Session = Depends(get_db)):
    return db.query(RegistroDePagos).all()

@router.put("/registro_pagos/{registro_id}", response_model=RegistroDePagosRead)
def modificar_registro_pago(registro_id: str, registro: RegistroDePagosCreate, db: Session = Depends(get_db)):
    db_registro = db.query(RegistroDePagos).filter(RegistroDePagos.id == registro_id).first()
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro de pago no encontrado")
    for key, value in registro.model_dump().items():
        setattr(db_registro, key, value)
    db.commit()
    db.refresh(db_registro)
    return db_registro

@router.delete("/registro_pagos/{registro_id}")
def eliminar_registro_pago(registro_id: str, db: Session = Depends(get_db)):
    db_registro = db.query(RegistroDePagos).filter(RegistroDePagos.id == registro_id).first()
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro de pago no encontrado")
    db.delete(db_registro)
    db.commit()
    return {"ok": True}
