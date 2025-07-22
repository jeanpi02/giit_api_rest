# GIIT API REST

API REST para el sistema de gestión de investigación del Grupo de Investigación en Innovación y Tecnología (GIIT).

Este proyecto proporciona una API robusta para la gestión de usuarios, roles, publicaciones, productos, eventos, líneas de investigación, tipologías y semilleros, integrando autenticación, autorización y operaciones CRUD completas sobre una base de datos PostgreSQL.

## Configuración de Variables de Entorno

El proyecto utiliza un archivo `.env` para gestionar las credenciales y parámetros de conexión a la base de datos. Debes crear un archivo `.env` en la raíz del proyecto con el siguiente formato:

```
DB_HOST=tu_host
DB_PORT=tu_puerto
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

Puedes usar el archivo `.env.example` como plantilla.

## Instalación y Ejecución

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd GIIT-api-rest
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
# En Linux/Mac
source .venv/bin/activate
# En Windows
.venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura el archivo `.env` como se indicó arriba.

5. Crea la base de datos en PostgreSQL:
```sql
CREATE DATABASE giit_db;
```

6. Inicia el servidor de desarrollo:
```bash
uvicorn main:app --reload
```

7. Accede a la documentación interactiva:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del Proyecto

```
GIIT-api-rest/
├── app/
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Esquemas Pydantic
│   ├── routes/         # Rutas de la API
│   ├── core/           # Configuraciones centrales
│   └── database/       # Configuración de la base de datos
├── .env               # Variables de entorno (no subir al repo)
├── .env.example       # Plantilla de variables de entorno
├── requirements.txt   # Dependencias del proyecto
└── main.py           # Punto de entrada de la aplicación
```

## Características Principales

- Autenticación y autorización de usuarios
- Gestión de roles y permisos
- CRUD completo para todas las entidades principales
- Validación de datos con Pydantic
- Documentación automática con Swagger y ReDoc
- Integración con PostgreSQL
- Manejo de relaciones entre entidades
- Paginación y filtrado de resultados

## Endpoints Destacados

- `/usuarios/` - Gestión de usuarios
- `/roles/` - Gestión de roles
- `/lineas_investigacion/` - Gestión de líneas de investigación
- `/publicaciones/` - Gestión de publicaciones
- `/eventos/` - Gestión de eventos
- `/tipologias/` - Gestión de tipologías
- `/productos/` - Gestión de productos

## Contribución

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFeature`)
3. Commit tus cambios (`git commit -m 'Agrega NuevaFeature'`)
4. Push a la rama (`git push origin feature/NuevaFeature`)
5. Abre un Pull Request
