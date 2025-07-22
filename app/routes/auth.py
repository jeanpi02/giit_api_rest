from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.post("/login", response_model=schemas.LoginResponse)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    usuario = db.query(models.Usuario).filter(models.Usuario.email == login_data.email).first()
    
    if not usuario:
        return schemas.LoginResponse(
            success=False,
            mensaje="Credenciales inválidas"
        )
    
    # Verificar contraseña
    if login_data.password != usuario.password:
        return schemas.LoginResponse(
            success=False,
            mensaje="Credenciales inválidas"
        )
    
    # Obtener el rol del usuario
    rol = db.query(models.Rol).filter(models.Rol.id_rol == usuario.id_rol).first()
    
    return schemas.LoginResponse(
        success=True,
        id_usuario=usuario.id_usuario,
        username=usuario.nombre,
        rol=rol.nombre_rol if rol else None,
        foto_perfil=usuario.foto_perfil,
        mensaje="Login exitoso"
    )