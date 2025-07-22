from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:passgiit23@localhost/giit_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from app.models import models
    
    Base.metadata.create_all(bind=engine)
    
    # Crear una sesión para insertar datos por defecto
    db = SessionLocal()
    
    try:
        # Verificar si ya existen roles
        if not db.query(models.Rol).first():
            # Crear roles por defecto
            roles = [
                models.Rol(
                    nombre_rol="administrador",
                    descripcion="Usuario con acceso total al sistema"
                ),
                models.Rol(
                    nombre_rol="investigador",
                    descripcion="Usuario que participa en proyectos y publicaciones"
                )
            ]
            db.add_all(roles)
            db.commit()
            
            # Crear usuarios por defecto
            admin_rol = db.query(models.Rol).filter(models.Rol.nombre_rol == "administrador").first()
            investigador_rol = db.query(models.Rol).filter(models.Rol.nombre_rol == "investigador").first()
            
            if admin_rol and investigador_rol:
                usuarios = [
                    models.Usuario(
                        id_rol=admin_rol.id_rol,
                        nombre="Admin",
                        apellido="Principal",
                        email="admin@example.com",
                        password="admin123",
                        telefono="1234567890",
                        institucion="Universidad Nacional",
                        especialidad="Sistemas",
                        estado=models.UsuarioEstado.activo
                    ),
                    models.Usuario(
                        id_rol=investigador_rol.id_rol,
                        nombre="Jhon",
                        apellido="Doe",
                        email="investigador@example.com",
                        password="inv123",
                        telefono="0987654321",
                        institucion="Universidad Nacional",
                        especialidad="Ingeniería de Software",
                        estado=models.UsuarioEstado.activo
                    )
                ]
                db.add_all(usuarios)
                db.commit()
            
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 