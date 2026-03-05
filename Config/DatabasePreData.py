import json
import os

from Data.consults import get_info_inventario, get_ventas_totales, get_valor_total_inventario, get_top10_productos_mas_vendidos
from tensoflow.recomendations import entrenar_y_predecir

path_ = "./Data/MetricasAsadorInteligente.txt"

def checkDataInfo (up: int):
  inversion_total = get_valor_total_inventario()
  inversion_prod = get_info_inventario() 
  ventas_totales = get_ventas_totales()
  top_10 = get_top10_productos_mas_vendidos()

  # Verificar que todas las funciones devuelvan datos válidos
  if any(v is None for v in [inversion_total, ventas_totales]):
      print("Advertencia: Datos insuficientes para generar el reporte.")
      return

  info_asadorInteligente = {
    "Inventario":f"{inversion_prod}\n",
    "Inversión total del inventario": f"{inversion_total}\n",
    "Ventas totales": f"{ventas_totales}\n",
    "Top 10 productos": f"{top_10}\n" or f"{list[any]}\n",
    "Resumen de análisis predictivo": f"{list[str]}\n"
  }
  
  if os.path.exists(path=path_):
    infoDef(info_asadorInteligente,path_) if up == 1 else 0
  else:
    infoDef(info_asadorInteligente,path_)


def infoDef(info: any, loc: str):
  info["Resumen de análisis predictivo"] = f"{entrenar_y_predecir()}\n"
  with open(loc, "w", encoding="utf-8") as f:
    f.write(str(info))