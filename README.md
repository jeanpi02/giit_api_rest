# GIIT API REST

API REST para el sistema de gestión de investigación del GIIT.

## Rutas de Publicaciones

### Actualizar Estado de Publicación

**PUT** `/publicaciones/{publicacion_id}/estado`

Actualiza el estado de una publicación específica.

**Parámetros de ruta:**
- `publicacion_id` (int): ID de la publicación a actualizar

**Cuerpo de la petición:**
```json
{
  "estado": "aprobada",
  "id_aprobador": 1
}
```

**Estados disponibles:**
- `pendiente`: Estado inicial de las publicaciones
- `aprobada`: Publicación aprobada por un administrador
- `rechazada`: Publicación rechazada por un administrador

**Ejemplo de uso:**
```bash
curl -X PUT "http://localhost:8000/publicaciones/1/estado" \
     -H "Content-Type: application/json" \
     -d '{
       "estado": "aprobada",
       "id_aprobador": 1
     }'
```

**Respuesta exitosa:**
```json
{
  "id_publicacion": 1,
  "titulo": "Título de la publicación",
  "estado": "aprobada",
  "fecha_aprobacion": "2024-01-12T15:30:00",
  "aprobador_nombre": "María",
  "aprobador_apellido": "García",
  "mensaje": "Estado actualizado a 'aprobada' por María García"
}
```

**Notas:**
- El campo `id_aprobador` es opcional
- Si se proporciona `id_aprobador`, se registrará automáticamente la fecha de aprobación
- Si no se proporciona `id_aprobador`, solo se actualizará el estado sin registrar aprobador

## Rutas de Productos

### Actualizar Estado de Aprobación de Producto

**PUT** `/productos/{producto_id}/estado-aprobacion`

Actualiza el estado de aprobación de un producto específico.

**Parámetros de ruta:**
- `producto_id` (int): ID del producto a actualizar

**Cuerpo de la petición:**
```json
{
  "estado": "aprobado",
  "id_aprobador": 1
}
```

**Estados disponibles:**
- `pendiente`: Estado inicial de los productos
- `aprobado`: Producto aprobado por un administrador
- `rechazado`: Producto rechazado por un administrador

**Ejemplo de uso:**
```bash
curl -X PUT "http://localhost:8000/productos/1/estado-aprobacion" \
     -H "Content-Type: application/json" \
     -d '{
       "estado": "aprobado",
       "id_aprobador": 1
     }'
```

**Respuesta exitosa:**
```json
{
  "id_producto": 1,
  "nombre": "Nombre del producto",
  "estado": "aprobado",
  "fecha_aprobacion": "2024-01-12T15:30:00",
  "aprobador_nombre": "María",
  "aprobador_apellido": "García",
  "mensaje": "Estado de aprobación actualizado a 'aprobado' por María García"
}
```

### Aprobar Producto

**PUT** `/productos/{producto_id}/aprobar`

Aprueba un producto específico.

**Parámetros:**
- `producto_id` (int): ID del producto a aprobar
- `id_aprobador` (int): ID del usuario que aprueba

### Rechazar Producto

**PUT** `/productos/{producto_id}/rechazar`

Rechaza un producto específico.

**Parámetros:**
- `producto_id` (int): ID del producto a rechazar
- `id_aprobador` (int): ID del usuario que rechaza

### Obtener Productos con Información de Aprobador

**GET** `/productos/`

Obtiene la lista de productos con información del aprobador.

**Parámetros de consulta:**
- `estado_aprobacion` (opcional): Filtrar por estado de aprobación
- `estado_desarrollo` (opcional): Filtrar por estado de desarrollo
- `id_linea` (opcional): Filtrar por línea de investigación
- `id_tipologia` (opcional): Filtrar por tipología
- `id_responsable` (opcional): Filtrar por responsable

**Respuesta incluye:**
- `aprobador_nombre`: Nombre del aprobador (si existe)
- `aprobador_apellido`: Apellido del aprobador (si existe)
- `fecha_aprobacion`: Fecha de aprobación (si existe)
- `estado_aprobacion`: Estado de aprobación actual

### Crear Producto

**POST** `/productos/`

Crea un nuevo producto.

**Cuerpo de la petición:**
```json
{
  "nombre": "Nombre del producto",
  "descripcion": "Descripción del producto",
  "id_tipologia": 1,
  "id_linea": 1,
  "id_responsable": 1,
  "estado_desarrollo": "idea",
  "fecha_creacion": "2024-01-15",
  "enlace": "https://ejemplo.com",
  "repositorio": "https://github.com/ejemplo",
  "imagen_referencia": "https://ejemplo.com/imagen.jpg"
}
```

**Estados de desarrollo disponibles:**
- `idea`: Estado inicial, solo idea
- `desarrollo`: En proceso de desarrollo
- `pruebas`: En fase de pruebas
- `completado`: Producto terminado

**Ejemplo de uso:**
```bash
curl -X POST "http://localhost:8000/productos/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Sistema de Gestión",
       "descripcion": "Sistema web para gestión de inventarios",
       "id_tipologia": 1,
       "id_responsable": 1,
       "estado_desarrollo": "desarrollo"
     }'
```

## Requisitos

- Python 3.8+
- PostgreSQL
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd giit-api-rest
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
DATABASE_URL=postgresql://postgres:postgres@localhost/giit_db
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Crear la base de datos en PostgreSQL:
```sql
CREATE DATABASE giit_db;
```

## Ejecución

1. Iniciar el servidor de desarrollo:
```bash
uvicorn main:app --reload
```

2. Acceder a la documentación de la API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del Proyecto

```
giit-api-rest/
├── app/
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Esquemas Pydantic
│   ├── routes/         # Rutas de la API
│   ├── core/           # Configuraciones centrales
│   └── database/       # Configuración de la base de datos
├── .env               # Variables de entorno
├── requirements.txt   # Dependencias del proyecto
└── main.py           # Punto de entrada de la aplicación
```

## Características

- Autenticación y autorización de usuarios
- Gestión de roles y permisos
- CRUD completo para todas las entidades
- Validación de datos con Pydantic
- Documentación automática con Swagger y ReDoc
- Integración con PostgreSQL
- Manejo de relaciones entre entidades
- Paginación y filtrado de resultados

## Endpoints Principales

- `/api/v1/usuarios/` - Gestión de usuarios
- `/api/v1/roles/` - Gestión de roles
- `/api/v1/lineas-investigacion/` - Gestión de líneas de investigación
- `/api/v1/publicaciones/` - Gestión de publicaciones
- `/api/v1/eventos/` - Gestión de eventos
- `/api/v1/tipologias/` - Gestión de tipologías
- `/api/v1/productos/` - Gestión de productos
- `/api/v1/semilleros/` - Gestión de semilleros

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 