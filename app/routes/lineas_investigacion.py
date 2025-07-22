from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.post("/lineas-investigacion/", response_model=schemas.LineaInvestigacion, status_code=status.HTTP_201_CREATED)
def create_linea_investigacion(linea: schemas.LineaInvestigacionCreate, db: Session = Depends(get_db)):
    # Verificar si el responsable existe
    if linea.id_responsable:
        responsable = db.query(models.Usuario).filter(models.Usuario.id_usuario == linea.id_responsable).first()
        if not responsable:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El responsable especificado no existe"
            )
    
    db_linea = models.LineaInvestigacion(**linea.dict())
    db.add(db_linea)
    db.commit()
    db.refresh(db_linea)
    return db_linea

@router.get("/lineas-investigacion/", response_model=List[schemas.LineaInvestigacion])
def read_lineas_investigacion(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[models.LineaInvestigacionEstado] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.LineaInvestigacion)
    if estado:
        query = query.filter(models.LineaInvestigacion.estado == estado)
    lineas = query.offset(skip).limit(limit).all()
    return lineas

@router.get("/lineas-investigacion/{linea_id}", response_model=schemas.LineaInvestigacion)
def read_linea_investigacion(linea_id: int, db: Session = Depends(get_db)):
    db_linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == linea_id).first()
    if db_linea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Línea de investigación no encontrada"
        )
    return db_linea

@router.put("/lineas-investigacion/{linea_id}", response_model=schemas.LineaInvestigacion)
def update_linea_investigacion(linea_id: int, linea: schemas.LineaInvestigacionCreate, db: Session = Depends(get_db)):
    db_linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == linea_id).first()
    if db_linea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Línea de investigación no encontrada"
        )
    
    # Verificar si el nuevo responsable existe
    if linea.id_responsable:
        responsable = db.query(models.Usuario).filter(models.Usuario.id_usuario == linea.id_responsable).first()
        if not responsable:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El responsable especificado no existe"
            )
    
    # Obtener los datos de la línea
    linea_data = linea.dict()
    
    # Si imagen_logo es "string", mantener la imagen actual
    if linea_data.get('imagen_logo') == "string":
        linea_data.pop('imagen_logo')
    
    for key, value in linea_data.items():
        setattr(db_linea, key, value)
    
    db.commit()
    db.refresh(db_linea)
    return db_linea

@router.delete("/lineas-investigacion/{linea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_linea_investigacion(linea_id: int, db: Session = Depends(get_db)):
    db_linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == linea_id).first()
    if db_linea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Línea de investigación no encontrada"
        )
    
    # Verificar si hay publicaciones, productos o semilleros asociados
    publicaciones = db.query(models.Publicacion).filter(models.Publicacion.id_linea == linea_id).first()
    productos = db.query(models.Producto).filter(models.Producto.id_linea == linea_id).first()
    # semilleros = db.query(models.Semillero).filter(models.Semillero.id_linea == linea_id).first()
    
    if publicaciones or productos: # Removed semilleros check
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la línea de investigación porque tiene publicaciones o productos asociados" # Updated detail
        )
    
    db.delete(db_linea)
    db.commit()
    return None 