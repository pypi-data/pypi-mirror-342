# ServexTools

Herramientas avanzadas para Servextex: utilidades para manejo de datos, logs, fechas, sockets y replicación MongoDB.

[![PyPI version](https://badge.fury.io/py/servextools.svg)](https://pypi.org/project/servextools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Tabla de Contenidos
- [Instalación](#instalación)
- [Módulos y Funcionalidades](#módulos-y-funcionalidades)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Dependencias](#dependencias)
- [Licencia](#licencia)

---

## Instalación

```sh
pip install servextools
```

---

## Módulos y Funcionalidades

### Tools.py
Funciones generales y utilidades:
- **FormatearValor(valor):** Convierte valores Decimal a float.
- **StrToDate(dato):** Convierte string a fecha.
- **Mensaje / MensajeV2:** Genera respuestas estándar para APIs.
- **Encriptar:** Encripta datos con JWT.
- **AgregarActualizarCampo / EliminarArea / CambiarNombreColeccion:** Utilidades para colecciones MongoDB.
- **WriteFile, EscribirLog:** Manejo de archivos y logs.

### EscribirLog.py
- **EscribirLog(texto, tipo):** Escribe logs de error y éxito.
- **EscribirConsola, EscribirProcesos, EscribirUpdate:** Logs especializados para consola y procesos.

### GetTime.py
- Utilidades para manejo avanzado de fechas y horas.

### Enumerable.py
- Enumeraciones útiles para tu aplicación.

### Table.py
- **CrearTabla, CrearTablaReport:** Generación de tablas HTML dinámicas a partir de datos.
- **Formatos:** Formatea columnas según tipo (fecha, moneda, etc).

### ReplicaDb.py
- Utilidades para replicación y manejo avanzado de bases de datos MongoDB.

### socket_manager.py
- Gestión de WebSockets usando Flask-SocketIO para aplicaciones en tiempo real.

### conexion.py
- **Get, GetDB, ProcesarDatos:** Abstracciones para conexión y operaciones con MongoDB.
- **TypeConnection:** Obtiene parámetros de conexión seguros.

---

## Ejemplos de Uso

### Formateo y utilidades generales
```python
from ServexTools import Tools
from decimal import Decimal

# Formatear un valor decimal
dato = Tools.FormatearValor(Decimal('123.45'))
print(dato)

# Manejo de fechas
fecha = Tools.StrToDate("19/04/2025")
print(fecha)

# Encriptar datos
jwt_token = Tools.Encriptar("mi_dato", "mi_clave_secreta")
print(jwt_token)
```

### Manejo de logs
```python
from ServexTools import EscribirLog
EscribirLog.EscribirLog("Mensaje de prueba", tipo="Exito")
```

### Conexión y operaciones MongoDB
```python
from ServexTools import conexion

# Obtener colección y cliente
collection, client = conexion.Get("mi_coleccion")

# Insertar un documento
doc = {"nombre": "Juan", "edad": 30}
collection.insert_one(doc)
```

### Generación de tablas HTML
```python
from ServexTools import Table

datos = [
    {"Nombre": "Juan", "Edad": 30},
    {"Nombre": "Ana", "Edad": 25}
]
columnas = ("Nombre", "Edad")
html = Table.CrearTabla(datos, NombreColumnas=columnas)
print(html)
```

---

## Dependencias
- flask
- pymongo
- pytz
- PyJWT
- httpx
- eventlet
- flask-socketio
- tqdm

---

## Licencia
MIT - Ver archivo [LICENSE](LICENSE)
