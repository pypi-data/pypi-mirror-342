# ServexTools

Herramientas para Servextex: utilidades para manejo de datos, logs, fechas, sockets y replicación MongoDB.

[![PyPI version](https://badge.fury.io/py/servextools.svg)](https://pypi.org/project/servextools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Instalación

```sh
pip install servextools
```

## Uso básico

```python
from ServexTools import Tools
from decimal import Decimal

# Formatear un valor decimal
dato = Tools.FormatearValor(Decimal('123.45'))
print(dato)

# Manejo de fechas
fecha = Tools.StrToDate("19/04/2025")
print(fecha)

# Escribir un log
from ServexTools import EscribirLog
EscribirLog.EscribirLog("Mensaje de prueba")

# Conexión a MongoDB (requiere configuración previa)
# from ServexTools import conexion
# collection, client = conexion.Get("mi_coleccion")
```

## Módulos principales

- **Tools.py**: Funciones generales (formateo, fechas, utilidades varias).
- **Enumerable.py**: Enumeraciones útiles.
- **EscribirLog.py**: Sistema de logs y consola.
- **GetTime.py**: Manejo de fechas y horas.
- **socket_manager.py**: Gestión de websockets (requiere Flask y Flask-SocketIO).
- **ReplicaDb.py**: Replicación y utilidades para MongoDB.
- **Table.py**: Utilidades para manejo y formateo de tablas de datos.

## Dependencias principales

- flask, pymongo, pytz, PyJWT, httpx, eventlet, flask-socketio, tqdm, bson

## Licencia

MIT - Ver archivo [LICENSE](LICENSE)
