from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import roles, usuarios, lineas_investigacion, publicaciones, eventos, tipologias, productos, auth, carrusel
from app.database.database import init_db, engine
from app.models import models

# Crear las tablas y datos por defecto
models.Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="GIIT API",
    description="API REST para el sistema de gestión de investigación",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir routers con tags
app.include_router(auth.router, tags=["Autenticación"])
app.include_router(roles.router, tags=["Roles"])
app.include_router(usuarios.router, tags=["Usuarios"])
app.include_router(lineas_investigacion.router, tags=["Líneas de Investigación"])
app.include_router(publicaciones.router, tags=["Publicaciones"])
app.include_router(eventos.router, tags=["Eventos"])
app.include_router(tipologias.router, tags=["Tipologías"])
app.include_router(productos.router, tags=["Productos"])
app.include_router(carrusel.router, tags=["Carrusel"])

@app.get("/", tags=["General"])
async def root():
    return {"message": "Bienvenido a la API de GIIT"}
