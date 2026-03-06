import json
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from Models.Inventario import Inventario
from Models.detalle_pagos import DetallePago
from Models.metodo_pago import MetodoPago
from Models.platillos import Platillo
from Models.registro_de_pagos import RegistroDePagos
from Config.DatabaseConn import SessionLocal, get_db

def get_ventas_totales():
  db: Session = SessionLocal()
  
  resultado = (
    db.query(
      func.sum(Platillo.precio * DetallePago.cantidad).label("ventas_totales")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .join(RegistroDePagos, RegistroDePagos.id == DetallePago.id_pago)
    .scalar()  # Con esta query se extrae el valor único
  )
  suma_total = float(resultado) if resultado else 0.0
  
  if(suma_total == 0.0):
    return None
  
  return {"ventas_totales": suma_total}

def get_valor_total_inventario(
):
  db: Session = SessionLocal()
  # Obtener el total general
  valor_total = db.query(
    func.sum(Inventario.precio_compra)
  ).scalar()
  
  if valor_total == 0:
    return None
  
  return {"inversion_total":valor_total}

def get_top10_productos_mas_vendidos():
  db: Session = SessionLocal()
  
  resultado = (
    db.query(
      Platillo.nombre.label("nombre_platillo"),
      func.sum(DetallePago.cantidad).label("cantidad_total_vendida"),
      func.sum(Platillo.precio * DetallePago.cantidad).label("ventas_acumuladas")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .group_by(Platillo.id, Platillo.nombre)
    .order_by(desc("cantidad_total_vendida"))
    .limit(10)
    .all()
  )
  
  if resultado == 0:
    return None
  
  ventas_dict = [row._asdict() for row in resultado]
  return ventas_dict

def get_info_inventario():
  db: Session = SessionLocal()
  
  resultado = (
  db.query(
    Inventario.nombre_insumo,
    Inventario.categoria,
    Inventario.cantidad,
    Inventario.precio_compra
  )
  .all()
  )
  
  inventario_lista_plana = []
  for row in resultado:
    inventario_lista_plana.append([
      row.nombre_insumo,
      row.categoria,
      float(row.cantidad) if row.cantidad else 0.0,
      float(row.precio_compra) if row.precio_compra else 0.0
    ])
  
  return inventario_lista_plana
