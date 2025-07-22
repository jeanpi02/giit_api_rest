from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.post("/roles/", response_model=schemas.Rol, status_code=status.HTTP_201_CREATED)
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    # Verificar si el nombre del rol ya existe
    db_rol = db.query(models.Rol).filter(models.Rol.nombre_rol == rol.nombre_rol).first()
    if db_rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre del rol ya existe"
        )
    
    db_rol = models.Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.get("/roles/", response_model=List[schemas.Rol])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(models.Rol).offset(skip).limit(limit).all()
    return roles

@router.get("/roles/{rol_id}", response_model=schemas.Rol)
def read_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()
    if db_rol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return db_rol

@router.put("/roles/{rol_id}", response_model=schemas.Rol)
def update_rol(rol_id: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()
    if db_rol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Verificar si el nuevo nombre ya existe en otro rol
    if rol.nombre_rol != db_rol.nombre_rol:
        existing_rol = db.query(models.Rol).filter(models.Rol.nombre_rol == rol.nombre_rol).first()
        if existing_rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del rol ya existe"
            )
    
    for key, value in rol.dict().items():
        setattr(db_rol, key, value)
    
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.delete("/roles/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()
    if db_rol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Verificar si hay usuarios asociados al rol
    usuarios = db.query(models.Usuario).filter(models.Usuario.id_rol == rol_id).first()
    if usuarios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el rol porque tiene usuarios asociados"
        )
    
    db.delete(db_rol)
    db.commit()
    return None 