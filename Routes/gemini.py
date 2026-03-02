import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from Models.Inventario import Inventario
from Models.detalle_pagos import DetallePago
from Models.metodo_pago import MetodoPago
from Models.platillos import Platillo
from Models.registro_de_pagos import RegistroDePagos
from Config.DatabaseConn import get_db
from Config.geminiConnection import chat as sesionGemini, consulta_agente_pro

router = APIRouter()

#Gemini obtiene las ventas totales y responde con un analisis.
@router.post("/respuesta_ia/ventas_totales/")
def obtener_ventas_totales_ia(info: dict, db: Session = Depends(get_db), skip: int = 0, 
  limit: int = 100,):
  resultado = (
    db.query(
      Platillo.nombre.label("nombre_platillo"),
      DetallePago.cantidad.label("cantidad_vendida"),
      MetodoPago.nombre.label("metodo_pago"),
      (Platillo.precio * DetallePago.cantidad).label("precio_total")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .join(RegistroDePagos, RegistroDePagos.id == DetallePago.id_pago)
    .join(MetodoPago, MetodoPago.id == RegistroDePagos.id_metodo_pago)
    .offset(skip)
    .limit(limit)
    .all()
  )
  ventas_dict = [row._asdict() for row in resultado]
  
  lineas = []
  for venta in ventas_dict:
    linea = f"Platillo: {venta['nombre_platillo']}, Cantidad: {venta['cantidad_vendida']}, Método: {venta['metodo_pago']}, Total: ${venta['precio_total']:.2f}"
    lineas.append(linea)
  clave_para_analisis = "\n".join(lineas)
  
  consulta_gemini = consulta_agente_pro(clave_para_analisis, info['respuesta'], sesionGemini)
  return consulta_gemini

#Obtener las ventas totales.
@router.get("/ventas_totales/")
def obtener_ventas_totales(db: Session = Depends(get_db), skip: int = 0, 
  limit: int = 100,):
  resultado = (
    db.query(
      Platillo.nombre.label("nombre_platillo"),
      DetallePago.cantidad.label("cantidad_vendida"),
      MetodoPago.nombre.label("metodo_pago"),
      (Platillo.precio * DetallePago.cantidad).label("precio_total")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .join(RegistroDePagos, RegistroDePagos.id == DetallePago.id_pago)
    .join(MetodoPago, MetodoPago.id == RegistroDePagos.id_metodo_pago)
    .offset(skip)
    .limit(limit)
    .all()
  )
  
  ventas_dict = [row._asdict() for row in resultado]
  return ventas_dict

"""
Retorna los productos más vendidos (top N) con:
- Nombre del platillo
- Cantidad total vendida (sumada de todas las ventas)
"""
@router.post("/respuesta_ia/productos-top3")
def obtener_top3_productos_mas_vendidos_ia(
  info: dict,
  limite: int = 3,
  db: Session = Depends(get_db)
):
  resultado = (
    db.query(
      Platillo.nombre.label("nombre_platillo"),
      func.sum(DetallePago.cantidad).label("cantidad_total_vendida")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .group_by(Platillo.id, Platillo.nombre)
    .order_by(desc("cantidad_total_vendida"))
    .limit(limite)
    .all()
  )
  
  ventas_dict = [row._asdict() for row in resultado]
  
  lineas = []
  for venta in ventas_dict:
    linea = f"Nombre del Platillo: {venta['nombre_platillo']}, Cantidad Vendidas Totales: {venta['cantidad_total_vendida']}"
    lineas.append(linea)
  
  clave_para_analisis = "\n".join(lineas)
  
  consulta_gemini = consulta_agente_pro(clave_para_analisis, info['respuesta'], sesionGemini)
  return consulta_gemini

"""
Retorna los productos más vendidos (top 3) con los parametros:
- Nombre del platillo
- Cantidad total vendida (sumada de todas las ventas)
"""
@router.get("/ventas/productos-top3")
def obtener_top3_productos_mas_vendidos(
  limite: int = 3,
  db: Session = Depends(get_db)
):
  
  
  resultado = (
    db.query(
      Platillo.nombre.label("nombre_platillo"),
      func.sum(DetallePago.cantidad).label("cantidad_total_vendida")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .group_by(Platillo.id, Platillo.nombre)
    .order_by(desc("cantidad_total_vendida"))
    .limit(limite)
    .all()
  )
  
  ventas_dict = [row._asdict() for row in resultado]
  return ventas_dict

@router.get("/inventario/inversion-total-raw/")
def obtener_inventario_total_raw(
  db: Session = Depends(get_db)
):
  resultado = (
    db.query(
      Inventario.nombre_insumo,
      Inventario.categoria,
      Inventario.cantidad,
      Inventario.precio_compra
    ).all()
  )
  
  # Convertir a lista de diccionarios la variable resultado.
  inventario_list = []
  for row in resultado:
    inventario_list.append({
      "nombre_insumo": row.nombre_insumo,
      "categoria": row.categoria,
      "cantidad": float(row.cantidad) if row.cantidad else 0.0,
      "precio_compra": float(row.precio_compra) if row.precio_compra else 0.0
    })
  
  resumen_json = json.dumps(inventario_list, ensure_ascii=False, indent=2)
  return resumen_json


"""
Retorna inventario en formato lista plana:
[[nombre_insumo, categoria, cantidad, precio_compra], ...]
"""
@router.get("/inventario/inversion-total-lista/")
def obtener_inventario_total_lista(
  db: Session = Depends(get_db)
):
  resultado = (
    db.query(
      Inventario.nombre_insumo,
      Inventario.categoria,
      Inventario.cantidad,
      Inventario.precio_compra
    )
    .all()
  )
  
  # Lista de listas (sin nombres de campo)
  inventario_lista_plana = []
  for row in resultado:
    inventario_lista_plana.append([
      row.nombre_insumo,
      row.categoria,
      float(row.cantidad) if row.cantidad else 0.0,
      float(row.precio_compra) if row.precio_compra else 0.0
    ])
  
  resumen_json = json.dumps(inventario_lista_plana, ensure_ascii=False, indent=2)
  return resumen_json


"""
Retorna valor total del inventario y totales por categoría
"""
@router.post("/inventario/inventario-valor-total/")
def obtener_valor_total_inventario(
  db: Session = Depends(get_db)
):
  # Obtener el total general
  valor_total = db.query(
    func.sum(Inventario.cantidad * Inventario.precio_compra)
  ).scalar()
  
  # Obtener por categoría
  por_categoria = (
      db.query(
        Inventario.categoria,
        func.sum(Inventario.cantidad * Inventario.precio_compra).label("valor")
      )
      .group_by(Inventario.categoria)
      .all()
  )
  
  resumen = {
      "valor_total_inventario": float(valor_total) if valor_total else 0.0,
      "por_categoria": [
        {"categoria": cat, "valor": float(val)}
        for cat, val in por_categoria
      ]
  }
  
  resumen_json = json.dumps(resumen, ensure_ascii=False, indent=2)
  return resumen_json


"""
Retorna valor total del inventario y totales por categoría
"""
@router.get("/respuesta_ia/inventario-valor-total/")
def obtener_valor_total_inventario(
  info: dict,
  db: Session = Depends(get_db)
):
  # Obtener el total general
  valor_total = db.query(
    func.sum(Inventario.cantidad * Inventario.precio_compra)
  ).scalar()
  
  # Obtener por categoría
  por_categoria = (
    db.query(
      Inventario.categoria,
      func.sum(Inventario.cantidad * Inventario.precio_compra).label("valor")
    )
    .group_by(Inventario.categoria)
    .all()
  )
  
  resumen = {
    "valor_total_inventario": float(valor_total) if valor_total else 0.0,
    "por_categoria": [
      {"categoria": cat, "valor": float(val)}
      for cat, val in por_categoria
    ]
  }
  resumen_json = json.dumps(resumen, ensure_ascii=False, indent=2)
  
  consulta_gemini = consulta_agente_pro(resumen_json, info['respuesta'], sesionGemini)
  return consulta_gemini

