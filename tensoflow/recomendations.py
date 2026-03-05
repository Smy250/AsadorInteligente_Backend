import tensorflow as tf
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from Models.detalle_pagos import DetallePago
from Models.platillos import Platillo
import os

# Bloquear avisos innecesarios
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def entrenar_y_predecir(db: Session) -> str:
    # 1. Extraer datos agregados usando la sesión recibida
    datos = db.query(
        Platillo.nombre,
        func.sum(DetallePago.cantidad).label("total")
    ).join(DetallePago).group_by(Platillo.nombre).all()

    if not datos:
        return "No hay ventas registradas"

    nombres_list = [str(d[0]) for d in datos]
    ventas_list = [float(d[1]) for d in datos]

    # Convertir a Tensores de string y float
    nombres_tensor = tf.constant(nombres_list, dtype=tf.string)
    ventas_tensor = tf.constant(ventas_list, dtype=tf.float32)
    vocabulario = np.array(nombres_list)

    # 2. Construir el Modelo
    model = tf.keras.Sequential([
        tf.keras.layers.StringLookup(vocabulary=vocabulario, mask_token=None),
        tf.keras.layers.Embedding(len(vocabulario) + 1, 8),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    # 3. Entrenar (epochs ajustadas para balancear velocidad/precisión)
    model.fit(nombres_tensor, ventas_tensor, epochs=200, verbose=0)

    # 4. Predecir sobre los mismos datos
    predicciones = model.predict(nombres_tensor, verbose=0)

    # Buscamos el índice con el valor más alto
    indice_ganador = np.argmax(predicciones)

    return nombres_list[indice_ganador]
