from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.post("/tipologias/", response_model=schemas.Tipologia, status_code=status.HTTP_201_CREATED)
def create_tipologia(tipologia: schemas.TipologiaCreate, db: Session = Depends(get_db)):
    # Verificar si el nombre de la tipología ya existe
    db_tipologia = db.query(models.Tipologia).filter(models.Tipologia.nombre == tipologia.nombre).first()
    if db_tipologia:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de la tipología ya existe"
        )
    
    db_tipologia = models.Tipologia(**tipologia.dict())
    db.add(db_tipologia)
    db.commit()
    db.refresh(db_tipologia)
    return db_tipologia

@router.get("/tipologias/", response_model=List[schemas.Tipologia])
def read_tipologias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipologias = db.query(models.Tipologia).offset(skip).limit(limit).all()
    return tipologias

@router.get("/tipologias/{tipologia_id}", response_model=schemas.Tipologia)
def read_tipologia(tipologia_id: int, db: Session = Depends(get_db)):
    db_tipologia = db.query(models.Tipologia).filter(models.Tipologia.id_tipologia == tipologia_id).first()
    if db_tipologia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipología no encontrada"
        )
    return db_tipologia

@router.put("/tipologias/{tipologia_id}", response_model=schemas.Tipologia)
def update_tipologia(tipologia_id: int, tipologia: schemas.TipologiaCreate, db: Session = Depends(get_db)):
    db_tipologia = db.query(models.Tipologia).filter(models.Tipologia.id_tipologia == tipologia_id).first()
    if db_tipologia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipología no encontrada"
        )
    
    # Verificar si el nuevo nombre ya existe en otra tipología
    if tipologia.nombre != db_tipologia.nombre:
        existing_tipologia = db.query(models.Tipologia).filter(models.Tipologia.nombre == tipologia.nombre).first()
        if existing_tipologia:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la tipología ya existe"
            )
    
    for key, value in tipologia.dict().items():
        setattr(db_tipologia, key, value)
    
    db.commit()
    db.refresh(db_tipologia)
    return db_tipologia

@router.delete("/tipologias/{tipologia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipologia(tipologia_id: int, db: Session = Depends(get_db)):
    db_tipologia = db.query(models.Tipologia).filter(models.Tipologia.id_tipologia == tipologia_id).first()
    if db_tipologia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipología no encontrada"
        )
    
    # Verificar si hay productos asociados a la tipología
    productos = db.query(models.Producto).filter(models.Producto.id_tipologia == tipologia_id).first()
    if productos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la tipología porque tiene productos asociados"
        )
    
    db.delete(db_tipologia)
    db.commit()
    return None 