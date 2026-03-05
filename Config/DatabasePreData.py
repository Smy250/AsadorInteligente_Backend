import json
import os

from Data.consults import get_ventas_totales, get_valor_total_inventario, get_top10_productos_mas_vendidos
from tensoflow.recomendations import entrenar_y_predecir

path_ = "./Data/MetricasAsadorInteligente.txt"

def checkDataInfo (up: int):
  inversion_total = get_ventas_totales()
  ventas_totales = get_valor_total_inventario()
  top_10 = get_top10_productos_mas_vendidos()
  #prediccion = entrenar_y_predecir()

  # Verificar que todas las funciones devuelvan datos válidos
  if any(v is None for v in [inversion_total, ventas_totales]):
      print("Advertencia: Datos insuficientes para generar el reporte.")
      return

  info_asadorInteligente = {
      "Inversión total": inversion_total,
      "Ventas totales": ventas_totales,
      "Top 10 productos": top_10 or list[any],
      "Resumen de análisis predictivo": list[str]
  }
  
  if os.path.exists(path=path_):
    infoDef(info_asadorInteligente,path_) if up == 1 else 0
  else:
    infoDef(info_asadorInteligente,path_)


def infoDef(info: dict[str,any], loc: str):
  info["Resumen de análisis predictivo"] = entrenar_y_predecir()
  with open(loc, "w", encoding="utf-8") as f:
    f.write(str(info))