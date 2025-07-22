from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from datetime import date

router = APIRouter()

@router.post("/eventos/", response_model=schemas.Evento, status_code=status.HTTP_201_CREATED)
def create_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    # Verificar si el creador existe
    creador = db.query(models.Usuario).filter(models.Usuario.id_usuario == evento.id_creador).first()
    if not creador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El creador especificado no existe"
        )
    
    # Verificar que la fecha de inicio no sea posterior a la fecha de fin
    if evento.fecha_inicio and evento.fecha_fin and evento.fecha_inicio > evento.fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin"
        )
    
    db_evento = models.Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@router.get("/eventos/", response_model=List[schemas.Evento])
def read_eventos(
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: date = None,
    fecha_fin: date = None,
    tipo_evento: str = None,
    id_creador: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Evento)
    
    if fecha_inicio:
        query = query.filter(models.Evento.fecha_inicio >= fecha_inicio)
    if fecha_fin:
        query = query.filter(models.Evento.fecha_fin <= fecha_fin)
    if tipo_evento:
        query = query.filter(models.Evento.tipo_evento == tipo_evento)
    if id_creador:
        query = query.filter(models.Evento.id_creador == id_creador)
    
    eventos = query.offset(skip).limit(limit).all()
    return eventos

@router.get("/eventos/{evento_id}", response_model=schemas.Evento)
def read_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id_evento == evento_id).first()
    if db_evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )
    return db_evento

@router.put("/eventos/{evento_id}", response_model=schemas.Evento)
def update_evento(evento_id: int, evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id_evento == evento_id).first()
    if db_evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )
    
    # Verificar si el creador existe
    creador = db.query(models.Usuario).filter(models.Usuario.id_usuario == evento.id_creador).first()
    if not creador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El creador especificado no existe"
        )
    
    # Verificar que la fecha de inicio no sea posterior a la fecha de fin
    if evento.fecha_inicio and evento.fecha_fin and evento.fecha_inicio > evento.fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin"
        )
    
    for key, value in evento.dict().items():
        setattr(db_evento, key, value)
    
    db.commit()
    db.refresh(db_evento)
    return db_evento

@router.delete("/eventos/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id_evento == evento_id).first()
    if db_evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )
    
    db.delete(db_evento)
    db.commit()
    return None 