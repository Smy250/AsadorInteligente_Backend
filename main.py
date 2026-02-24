# Importaciones principales de FastAPI y SQLAlchemy
import Models # Se importa Models para que funcione correctamente las relaciones, entre otros.
from fastapi import FastAPI

from Routes.proveedor import router as proveedor_router
from Routes.platillos import router as platillos_router
from Routes.receta_platillo import router as receta_platillo_router
from Routes.inventario import router as inventario_router
from Routes.metodo_pago import router as metodo_pago_router
from Routes.registro_de_pagos import router as registro_de_pagos_router

# Instancia principal de la aplicación FastAPI
app = FastAPI()
app.include_router(proveedor_router)
app.include_router(inventario_router)
app.include_router(platillos_router)
app.include_router(metodo_pago_router)
app.include_router(registro_de_pagos_router)
app.include_router(receta_platillo_router)
