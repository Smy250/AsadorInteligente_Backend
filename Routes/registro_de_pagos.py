import uuid

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from Config.DatabaseConn import SessionLocal
from Models.detalle_pagos import DetallePago
from Models.registro_de_pagos import PlatilloEnRegistroDePago, RegistroDePagos, RegistroDePagosCreate, RegistroDePagosRead
from Models.platillos import Platillo
from tensoflow.recomendations import entrenar_y_predecir

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registro_pagos/", response_model=RegistroDePagosRead)
def crear_registro_pago(datos: RegistroDePagosCreate, db: Session = Depends(get_db)):
    # Obtener los platillos desde la base de datos
    ids_platillos = [p.id_platillo for p in datos.platillos]
    platillos_db = db.execute(
        select(Platillo.id, Platillo.precio).where(
            Platillo.id.in_(ids_platillos))
    ).all()

    precios_map = {p.id: p.precio for p in platillos_db}

    # Validar que todos los platillos existan
    for item in datos.platillos:
        if item.id_platillo not in precios_map:
            raise HTTPException(
                status_code=404, detail=f"Platillo con id {item.id_platillo} no encontrado")

    # Calcular total_venta
    total_venta = sum(
        precios_map[item.id_platillo] * item.cantidad
        for item in datos.platillos
    )

    # Crear el registro de pago
    registro_pago = RegistroDePagos(
        id_metodo_pago=datos.id_metodo_pago,
        total_venta=total_venta
    )
    db.add(registro_pago)
    db.flush()

    # Crear los detalles de pago
    for item in datos.platillos:
        detalle = DetallePago(
            id_pago=registro_pago.id,
            id_platillo=item.id_platillo,
            cantidad=item.cantidad
        )
        db.add(detalle)

    db.commit()

    # Retornar el modelo de lectura
    return RegistroDePagosRead(
        id=registro_pago.id,
        id_metodo_pago=registro_pago.id_metodo_pago,
        total_venta=registro_pago.total_venta,
        created_at=registro_pago.created_at,
        platillos=datos.platillos
    )


@router.get("/registro_pagos/{id_pago}", response_model=RegistroDePagosRead)
def obtener_registro_pago(id_pago: uuid.UUID, db: Session = Depends(get_db)):
    registro_pago = db.query(RegistroDePagos).options(
        selectinload(RegistroDePagos.pago).selectinload(DetallePago.platillo)
    ).filter(RegistroDePagos.id == id_pago).first()

    if not registro_pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    platillos_detalle = [
        PlatilloEnRegistroDePago(
            id_platillo=detalle.id_platillo,
            cantidad=detalle.cantidad,
            nombre=detalle.platillo.nombre
        )
        for detalle in registro_pago.pago
    ]

    return RegistroDePagosRead(
        id=registro_pago.id,
        id_metodo_pago=registro_pago.id_metodo_pago,
        total_venta=registro_pago.total_venta,
        created_at=registro_pago.created_at,
        platillos=platillos_detalle
    )


@router.get("/registro_pagos/")
def listar_registros_pago(db: Session = Depends(get_db)):
    registros = db.query(RegistroDePagos).options(
        selectinload(RegistroDePagos.pago).selectinload(DetallePago.platillo)
    ).all()

    respuesta = []

    for registro in registros:
        platillos_detalle = [
            PlatilloEnRegistroDePago(
                id_platillo=detalle.id_platillo,
                cantidad=detalle.cantidad,
                nombre=detalle.platillo.nombre
            )
            for detalle in registro.pago
        ]

        respuesta.append(
            RegistroDePagosRead(
                id=registro.id,
                id_metodo_pago=registro.id_metodo_pago,
                total_venta=registro.total_venta,
                created_at=registro.created_at,
                platillos=platillos_detalle
            )
        )

    return respuesta


@router.put("/registro_pagos/{registro_id}")
def modificar_registro_pago(registro_id: str, registro: RegistroDePagosCreate, db: Session = Depends(get_db)):
    db_registro = db.query(RegistroDePagos).filter(
        RegistroDePagos.id == registro_id).first()
    if not db_registro:
        raise HTTPException(
            status_code=404, detail="Registro de pago no encontrado")
    for key, value in registro.model_dump().items():
        setattr(db_registro, key, value)
    db.commit()
    db.refresh(db_registro)
    return db_registro


@router.delete("/registro_pagos/{registro_id}")
def eliminar_registro_pago(registro_id: str, db: Session = Depends(get_db)):
    db_registro = db.query(RegistroDePagos).filter(
        RegistroDePagos.id == registro_id).first()
    if not db_registro:
        raise HTTPException(
            status_code=404, detail="Registro de pago no encontrado")
    db.delete(db_registro)
    db.commit()
    return {"ok": True}


@router.get("/recomendacion_ia_tenso-flow/")
def obtener_recomendacion_popularidad(db: Session = Depends(get_db)):
    try:
        # Ahora sí, la función espera 'db' y se la pasamos
        producto_estrella = entrenar_y_predecir(db)

        # Validar si devolvió el mensaje de "vacío"
        if producto_estrella == "No hay ventas registradas":
            return {
                "recomendacion": None,
                "mensaje": producto_estrella
            }

        return {
            "recomendacion": producto_estrella,
            "mensaje": f"¡{producto_estrella} es lo que más está saliendo! Seguro le encantará al cliente."
        }
    except Exception as e:
        # Esto te ayudará a ver errores reales en el log si algo falla
        print(f"Error en IA: {e}")
        raise HTTPException(status_code=500, detail=str(e))
