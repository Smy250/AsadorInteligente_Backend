# Instrucciones:

## Instalar PostsgresSQL
Visita el siguiente enlace (de no tener PostgreSQL) `https://www.postgresql.org/download/`.
Descargarlo e instalarlo.

## Instalar dependencias
Ubicate en la raíz del proyecto y coloca en tu terminal lo siguiente: ``pip install -r requirements.txt``

## Creación de variables de entorno.
Necesitas tener definidas las siguientes variables de entorno para que funcione correctamente:
``{user, password, host, port, db}`` Indica tu usuario, contraseña, dirección ip, puerto y base de datos.

## Migrar la Base de datos
Luego de instalar las dependencias, para realizar la migración ingresa lo siguiente:
``alembic upgrade head`` para efectuar la migración.

## Ejecutar el proyecto
``fastapi dev main.py``