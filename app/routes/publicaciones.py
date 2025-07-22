from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from datetime import datetime

router = APIRouter()

@router.post("/publicaciones/", response_model=schemas.Publicacion, status_code=status.HTTP_201_CREATED)
def create_publicacion(publicacion: schemas.PublicacionCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva publicación. 
    El estado por defecto es 'pendiente' y debe ser aprobado por un administrador.
    """
    # Verificar si el autor principal existe
    autor = db.query(models.Usuario).filter(models.Usuario.id_usuario == publicacion.id_autor_principal).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El autor principal especificado no existe"
        )
    
    # Verificar si la línea de investigación existe
    if publicacion.id_linea:
        linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == publicacion.id_linea).first()
        if not linea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La línea de investigación especificada no existe"
            )
    
    # Crear la publicación con estado 'pendiente' por defecto
    db_publicacion = models.Publicacion(**publicacion.dict())
    db.add(db_publicacion)
    db.commit()
    db.refresh(db_publicacion)
    return db_publicacion

@router.get("/publicaciones/", response_model=List[schemas.PublicacionResponse])
def read_publicaciones(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[models.PublicacionEstado] = None,
    id_linea: Optional[int] = None,
    id_autor: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Publicacion)
    
    if estado:
        query = query.filter(models.Publicacion.estado == estado)
    if id_linea:
        query = query.filter(models.Publicacion.id_linea == id_linea)
    if id_autor:
        query = query.filter(models.Publicacion.id_autor_principal == id_autor)
    
    publicaciones = query.offset(skip).limit(limit).all()
    
    # Crear respuestas con información del aprobador
    publicaciones_response = []
    for pub in publicaciones:
        aprobador_nombre = None
        aprobador_apellido = None
        
        id_aprobador = getattr(pub, 'id_aprobador', None)
        if id_aprobador is not None:
            aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
            if aprobador:
                aprobador_nombre = aprobador.nombre
                aprobador_apellido = aprobador.apellido
        
        publicacion_dict = {
            'id_publicacion': getattr(pub, 'id_publicacion'),
            'titulo': getattr(pub, 'titulo'),
            'resumen': getattr(pub, 'resumen'),
            'autores': getattr(pub, 'autores'),
            'revista_conferencia': getattr(pub, 'revista_conferencia'),
            'fecha_publicacion': getattr(pub, 'fecha_publicacion'),
            'enlace': getattr(pub, 'enlace'),
            'id_linea': getattr(pub, 'id_linea'),
            'id_autor_principal': getattr(pub, 'id_autor_principal'),
            'estado': getattr(pub, 'estado'),
            'fecha_registro': getattr(pub, 'fecha_registro'),
            'fecha_aprobacion': getattr(pub, 'fecha_aprobacion'),
            'id_aprobador': id_aprobador,
            'aprobador_nombre': aprobador_nombre,
            'aprobador_apellido': aprobador_apellido,
            'autor_principal': pub.autor_principal,
            'linea': pub.linea
        }
        publicaciones_response.append(schemas.PublicacionResponse(**publicacion_dict))
    
    return publicaciones_response

@router.get("/publicaciones/{publicacion_id}", response_model=schemas.PublicacionResponse)
def read_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    db_publicacion = db.query(models.Publicacion).filter(models.Publicacion.id_publicacion == publicacion_id).first()
    if db_publicacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Obtener información del aprobador
    aprobador_nombre = None
    aprobador_apellido = None
    
    id_aprobador = getattr(db_publicacion, 'id_aprobador', None)
    if id_aprobador is not None:
        aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
        if aprobador:
            aprobador_nombre = aprobador.nombre
            aprobador_apellido = aprobador.apellido
    
    publicacion_dict = {
        'id_publicacion': getattr(db_publicacion, 'id_publicacion'),
        'titulo': getattr(db_publicacion, 'titulo'),
        'resumen': getattr(db_publicacion, 'resumen'),
        'autores': getattr(db_publicacion, 'autores'),
        'revista_conferencia': getattr(db_publicacion, 'revista_conferencia'),
        'fecha_publicacion': getattr(db_publicacion, 'fecha_publicacion'),
        'enlace': getattr(db_publicacion, 'enlace'),
        'id_linea': getattr(db_publicacion, 'id_linea'),
        'id_autor_principal': getattr(db_publicacion, 'id_autor_principal'),
        'estado': getattr(db_publicacion, 'estado'),
        'fecha_registro': getattr(db_publicacion, 'fecha_registro'),
        'fecha_aprobacion': getattr(db_publicacion, 'fecha_aprobacion'),
        'id_aprobador': id_aprobador,
        'aprobador_nombre': aprobador_nombre,
        'aprobador_apellido': aprobador_apellido,
        'autor_principal': db_publicacion.autor_principal,
        'linea': db_publicacion.linea
    }
    
    return schemas.PublicacionResponse(**publicacion_dict)

@router.put("/publicaciones/{publicacion_id}", response_model=schemas.Publicacion)
def update_publicacion(publicacion_id: int, publicacion: schemas.PublicacionCreate, db: Session = Depends(get_db)):
    db_publicacion = db.query(models.Publicacion).filter(models.Publicacion.id_publicacion == publicacion_id).first()
    if db_publicacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar si el autor principal existe
    autor = db.query(models.Usuario).filter(models.Usuario.id_usuario == publicacion.id_autor_principal).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El autor principal especificado no existe"
        )
    
    # Verificar si la línea de investigación existe
    if publicacion.id_linea:
        linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == publicacion.id_linea).first()
        if not linea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La línea de investigación especificada no existe"
            )
    
    for key, value in publicacion.dict().items():
        setattr(db_publicacion, key, value)
    
    db.commit()
    db.refresh(db_publicacion)
    return db_publicacion

@router.delete("/publicaciones/{publicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    db_publicacion = db.query(models.Publicacion).filter(models.Publicacion.id_publicacion == publicacion_id).first()
    if db_publicacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    db.delete(db_publicacion)
    db.commit()
    return None

@router.put("/publicaciones/{publicacion_id}/aprobar", response_model=schemas.Publicacion)
def aprobar_publicacion(publicacion_id: int, id_aprobador: int, db: Session = Depends(get_db)):
    db_publicacion = db.query(models.Publicacion).filter(models.Publicacion.id_publicacion == publicacion_id).first()
    if db_publicacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar si el aprobador existe
    aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
    if not aprobador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El aprobador especificado no existe"
        )
    
    setattr(db_publicacion, 'estado', models.PublicacionEstado.aprobada)
    setattr(db_publicacion, 'id_aprobador', id_aprobador)
    setattr(db_publicacion, 'fecha_aprobacion', datetime.utcnow())
    
    db.commit()
    db.refresh(db_publicacion)
    return db_publicacion

@router.put("/publicaciones/{publicacion_id}/rechazar", response_model=schemas.Publicacion)
def rechazar_publicacion(publicacion_id: int, id_aprobador: int, db: Session = Depends(get_db)):
    db_publicacion = db.query(models.Publicacion).filter(models.Publicacion.id_publicacion == publicacion_id).first()
    if db_publicacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar si el aprobador existe
    aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
    if not aprobador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El aprobador especificado no existe"
        )
    
    setattr(db_publicacion, 'estado', models.PublicacionEstado.rechazada)
    setattr(db_publicacion, 'id_aprobador', id_aprobador)
    setattr(db_publicacion, 'fecha_aprobacion', datetime.utcnow())
    
    db.commit()
    db.refresh(db_publicacion)
    return db_publicacion

@router.put("/publicaciones/{publicacion_id}/estado", response_model=schemas.PublicacionEstadoResponse)
def actualizar_estado_publicacion(
    publicacion_id: int, 
    estado_update: schemas.PublicacionEstadoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar el estado de una publicación.
    Permite cambiar el estado a cualquier valor válido (pendiente, aprobada, rechazada).
    Si se proporciona un id_aprobador, se registrará como aprobador y se establecerá la fecha de aprobación.
    """
    db_publicacion = db.query(models.Publicacion).filter(models.Publicacion.id_publicacion == publicacion_id).first()
    if db_publicacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    aprobador_nombre = None
    aprobador_apellido = None
    
    # Si se proporciona un aprobador, verificar que existe
    if estado_update.id_aprobador:
        aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == estado_update.id_aprobador).first()
        if not aprobador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El aprobador especificado no existe"
            )
        setattr(db_publicacion, 'id_aprobador', estado_update.id_aprobador)
        setattr(db_publicacion, 'fecha_aprobacion', datetime.utcnow())
        aprobador_nombre = aprobador.nombre
        aprobador_apellido = aprobador.apellido
    
    # Actualizar el estado
    setattr(db_publicacion, 'estado', estado_update.estado)
    
    db.commit()
    db.refresh(db_publicacion)
    
    # Crear mensaje según el estado
    mensaje = f"Estado actualizado a '{estado_update.estado}'"
    if aprobador_nombre is not None and aprobador_apellido is not None:
        mensaje += f" por {aprobador_nombre} {aprobador_apellido}"
    
    return schemas.PublicacionEstadoResponse(
        id_publicacion=getattr(db_publicacion, 'id_publicacion'),
        titulo=getattr(db_publicacion, 'titulo'),
        estado=getattr(db_publicacion, 'estado'),
        fecha_aprobacion=getattr(db_publicacion, 'fecha_aprobacion'),
        aprobador_nombre=str(aprobador_nombre) if aprobador_nombre is not None else None,
        aprobador_apellido=str(aprobador_apellido) if aprobador_apellido is not None else None,
        mensaje=mensaje
    ) 