# Importaciones principales de FastAPI y SQLAlchemy
# Se importa Models para que funcione correctamente las relaciones, entre otros.
import Models
from fastapi import FastAPI

from Routes.proveedor import router as proveedor_router
from Routes.platillos import router as platillos_router
from Routes.receta_platillo import router as receta_platillo_router
from Routes.inventario import router as inventario_router
from Routes.metodo_pago import router as metodo_pago_router
from Routes.registro_de_pagos import router as registro_de_pagos_router
from Routes.gemini import router as gemini_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Asador Inteligente API",
    description="Sistema de gestión de inventario, recetas y facturación",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(registro_de_pagos_router, tags=[
    "Historial de Transacciones"])
app.include_router(proveedor_router, tags=["Gestión de Proveedores"])
app.include_router(inventario_router, tags=["Inventario y Stock"])
app.include_router(platillos_router, tags=["Menú de Platillos"])
app.include_router(metodo_pago_router, tags=["Configuración de Pagos"])
app.include_router(receta_platillo_router, tags=["Recetas y Escandallos"])
app.include_router(gemini_router, tags=["Consulta Gemini"])
