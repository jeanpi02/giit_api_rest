from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/carrusel", tags=["Carrusel"])

@router.post("/", response_model=schemas.CarruselFoto, status_code=status.HTTP_201_CREATED)
def crear_foto_carrusel(foto: schemas.CarruselFotoCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva foto para el carrusel
    """
    # Verificar si ya existe una foto con ese orden
    foto_existente = db.query(models.CarruselFoto).filter(models.CarruselFoto.orden == foto.orden).first()
    if foto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una foto con el orden {foto.orden}"
        )
    
    db_foto = models.CarruselFoto(**foto.dict())
    db.add(db_foto)
    db.commit()
    db.refresh(db_foto)
    return db_foto

@router.get("/", response_model=List[schemas.CarruselFoto])
def obtener_fotos_carrusel(db: Session = Depends(get_db)):
    """
    Obtener todas las fotos del carrusel ordenadas por el campo orden
    """
    fotos = db.query(models.CarruselFoto).order_by(models.CarruselFoto.orden).all()
    return fotos

@router.get("/{foto_id}", response_model=schemas.CarruselFoto)
def obtener_foto_carrusel(foto_id: int, db: Session = Depends(get_db)):
    """
    Obtener una foto específica del carrusel por ID
    """
    foto = db.query(models.CarruselFoto).filter(models.CarruselFoto.id == foto_id).first()
    if not foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto no encontrada"
        )
    return foto

@router.put("/{foto_id}", response_model=schemas.CarruselFoto)
def actualizar_foto_carrusel(foto_id: int, foto: schemas.CarruselFotoCreate, db: Session = Depends(get_db)):
    """
    Actualizar una foto del carrusel
    """
    db_foto = db.query(models.CarruselFoto).filter(models.CarruselFoto.id == foto_id).first()
    if not db_foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto no encontrada"
        )
    
    # Verificar si el nuevo orden ya existe en otra foto
    if foto.orden != db_foto.orden:
        foto_existente = db.query(models.CarruselFoto).filter(
            models.CarruselFoto.orden == foto.orden,
            models.CarruselFoto.id != foto_id
        ).first()
        if foto_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una foto con el orden {foto.orden}"
            )
    
    for key, value in foto.dict().items():
        setattr(db_foto, key, value)
    
    db.commit()
    db.refresh(db_foto)
    return db_foto

@router.delete("/{foto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_foto_carrusel(foto_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una foto del carrusel
    """
    db_foto = db.query(models.CarruselFoto).filter(models.CarruselFoto.id == foto_id).first()
    if not db_foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto no encontrada"
        )
    
    db.delete(db_foto)
    db.commit()
    return None

@router.put("/{foto_id}/orden/{nuevo_orden}")
def cambiar_orden_foto(foto_id: int, nuevo_orden: int, db: Session = Depends(get_db)):
    """
    Cambiar el orden de una foto específica
    """
    db_foto = db.query(models.CarruselFoto).filter(models.CarruselFoto.id == foto_id).first()
    if not db_foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto no encontrada"
        )
    
    # Verificar si el nuevo orden ya existe
    foto_existente = db.query(models.CarruselFoto).filter(
        models.CarruselFoto.orden == nuevo_orden,
        models.CarruselFoto.id != foto_id
    ).first()
    if foto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una foto con el orden {nuevo_orden}"
        )
    
    setattr(db_foto, 'orden', nuevo_orden)
    db.commit()
    db.refresh(db_foto)
    return {"message": f"Orden de la foto {foto_id} cambiado a {nuevo_orden}"} 