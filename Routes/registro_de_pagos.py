from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from Config.DatabaseConn import SessionLocal
from Models.detalle_pagos import DetallePago
from Models.registro_de_pagos import RegistroDePagos, RegistroDePagosCreate, RegistroDePagosRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registro_pagos/")
def crear_registro_pago(registro: RegistroDePagosCreate, db: Session = Depends(get_db)):
    # 1. Creamos el objeto principal
    db_registro = RegistroDePagos(
        id_metodo_pago=registro.id_metodo_pago,
        total_venta=registro.total_venta
    )

    # 2. Asignamos los detalles
    db_registro.detalles = [
        DetallePago(id_platillo=p.id_platillo, cantidad=p.cantidad)
        for p in registro.platillos
    ]

    db.add(db_registro)
    db.commit()
    
    # 3. Recargamos con las relaciones cargadas explícitamente
    # Esto asegura que 'detalles' esté lleno antes de enviarlo al response_model
    db_registro = db.query(RegistroDePagos)\
        .options(joinedload(RegistroDePagos.detalles))\
        .filter(RegistroDePagos.id == db_registro.id)\
        .first()

    return db_registro


@router.get("/registro_pagos/{registro_id}")
def obtener_registro_pago(registro_id: str, db: Session = Depends(get_db)):
    registro = db.query(RegistroDePagos).filter(RegistroDePagos.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro de pago no encontrado")
    return registro


@router.get("/registro_pagos/")
def listar_registros_pago(db: Session = Depends(get_db)):
    return db.query(RegistroDePagos).all()


@router.put("/registro_pagos/{registro_id}")
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
