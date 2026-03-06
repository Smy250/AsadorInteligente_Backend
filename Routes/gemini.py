import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from Models.Inventario import Inventario
from Models.detalle_pagos import DetallePago
from Models.metodo_pago import MetodoPago
from Models.platillos import Platillo
from Models.registro_de_pagos import RegistroDePagos
from Config.DatabasePreData import path_
from Config.DatabaseConn import get_db
from Config.geminiConnection import chat as sesionGemini, consulta_agente_pro
from Data.consults import get_valor_total_inventario, get_ventas_totales, get_top10_productos_mas_vendidos
from tensoflow.recomendations import entrenar_y_predecir

router = APIRouter()

#Gemini obtiene todas las estadisticas para asesorar al usuario.
@router.post("/respuesta_ia/")
def obtener_ventas_totales_ia(info: dict):
  try:
    with open(path_, "r", encoding="utf-8") as f:
      contenido = f.read().strip()
    
    if not contenido:
      print("El archivo está vacío o no contiene datos válidos.")
      return None

    # Intentar parsear el contenido como JSON
    #info_asadorInteligente = json.loads(contenido)
    consulta_gemini = consulta_agente_pro(contenido, info['respuesta'], sesionGemini)
    return consulta_gemini

  except json.JSONDecodeError:
    return "El archivo no contiene un JSON válido."
  except FileNotFoundError:
    return f"Archivo {path_} no encontrado."
  except Exception as e:
    return f"Error al leer el archivo: {e}"

#Obtener ventas totales con tablas.
@router.get("/ventas_totales/")
def obtener_ventas_totales(db: Session = Depends(get_db), skip: int = 0, 
  limit: int = 50,):
  resultado = (
    db.query(
      Platillo.nombre.label("nombre_platillo"),
      DetallePago.cantidad.label("cantidad_vendida"),
      MetodoPago.nombre.label("metodo_pago"),
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .join(RegistroDePagos, RegistroDePagos.id == DetallePago.id_pago)
    .offset(skip)
    .limit(limit)
    .all()
  )
  
  ventas_dict = [row._asdict() for row in resultado]
  return ventas_dict

#Se obtienen las ventas totales en crudo numericamente.
@router.get("/ventas_totales_raw/")
def obtener_ventas_totales(db: Session = Depends(get_db),):
  resultado = (
    db.query(
      func.sum(Platillo.precio * DetallePago.cantidad).label("ventas_totales")
    )
    .join(DetallePago, DetallePago.id_platillo == Platillo.id)
    .join(RegistroDePagos, RegistroDePagos.id == DetallePago.id_pago)
    .scalar()  # Con esta query se extrae el valor único
  )
  suma_total = float(resultado) if resultado else 0.0 
  
  return {"ventas_totales":suma_total} 


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
      func.sum(DetallePago.cantidad).label("cantidad_total_vendida"),
      func.sum(Platillo.precio * DetallePago.cantidad).label("ventas_acumuladas")
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
  
  #resumen_json = json.dumps(inventario_lista_plana, ensure_ascii=False, indent=2)
  return inventario_lista_plana


"""
Retorna valor total del inventario.
"""
@router.get("/inventario/inventario-valor-total/")
def obtener_valor_total_inventario(
  db: Session = Depends(get_db)
):
  # Obtener el total general
  valor_total = db.query(
    func.sum(Inventario.precio_compra)
  ).scalar()
  
  return {"inversion_total":valor_total}


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

