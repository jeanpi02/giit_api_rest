from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from datetime import datetime

router = APIRouter()

@router.post("/productos/", response_model=schemas.Producto, status_code=status.HTTP_201_CREATED)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    # Verificar si la tipología existe
    tipologia = db.query(models.Tipologia).filter(models.Tipologia.id_tipologia == producto.id_tipologia).first()
    if not tipologia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La tipología especificada no existe"
        )
    
    # Verificar si la línea de investigación existe
    if producto.id_linea:
        linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == producto.id_linea).first()
        if not linea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La línea de investigación especificada no existe"
            )
    
    # Verificar si el responsable existe
    responsable = db.query(models.Usuario).filter(models.Usuario.id_usuario == producto.id_responsable).first()
    if not responsable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El responsable especificado no existe"
        )
    
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/productos/", response_model=List[schemas.ProductoResponse])
def read_productos(
    skip: int = 0,
    limit: int = 100,
    estado_desarrollo: Optional[models.ProductoEstadoDesarrollo] = None,
    estado_aprobacion: Optional[models.ProductoEstado] = None,
    id_linea: Optional[int] = None,
    id_tipologia: Optional[int] = None,
    id_responsable: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Producto)
    
    if estado_desarrollo:
        query = query.filter(models.Producto.estado_desarrollo == estado_desarrollo)
    if estado_aprobacion:
        query = query.filter(models.Producto.estado_aprobacion == estado_aprobacion)
    if id_linea:
        query = query.filter(models.Producto.id_linea == id_linea)
    if id_tipologia:
        query = query.filter(models.Producto.id_tipologia == id_tipologia)
    if id_responsable:
        query = query.filter(models.Producto.id_responsable == id_responsable)
    
    productos = query.offset(skip).limit(limit).all()
    
    # Crear respuestas con información del aprobador
    productos_response = []
    for prod in productos:
        aprobador_nombre = None
        aprobador_apellido = None
        
        id_aprobador = getattr(prod, 'id_aprobador', None)
        if id_aprobador is not None:
            aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
            if aprobador:
                aprobador_nombre = aprobador.nombre
                aprobador_apellido = aprobador.apellido
        
        producto_dict = {
            'id_producto': getattr(prod, 'id_producto'),
            'nombre': getattr(prod, 'nombre'),
            'descripcion': getattr(prod, 'descripcion'),
            'id_tipologia': getattr(prod, 'id_tipologia'),
            'id_linea': getattr(prod, 'id_linea'),
            'fecha_creacion': getattr(prod, 'fecha_creacion'),
            'enlace': getattr(prod, 'enlace'),
            'repositorio': getattr(prod, 'repositorio'),
            'imagen_referencia': getattr(prod, 'imagen_referencia'),
            'id_responsable': getattr(prod, 'id_responsable'),
            'estado_desarrollo': getattr(prod, 'estado_desarrollo'),
            'estado_aprobacion': getattr(prod, 'estado_aprobacion'),
            'fecha_registro': getattr(prod, 'fecha_registro'),
            'fecha_aprobacion': getattr(prod, 'fecha_aprobacion'),
            'id_aprobador': id_aprobador,
            'aprobador_nombre': aprobador_nombre,
            'aprobador_apellido': aprobador_apellido,
            'responsable': prod.responsable,
            'tipologia': prod.tipologia,
            'linea': prod.linea
        }
        productos_response.append(schemas.ProductoResponse(**producto_dict))
    
    return productos_response

@router.get("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Obtener información del aprobador
    aprobador_nombre = None
    aprobador_apellido = None
    
    id_aprobador = getattr(db_producto, 'id_aprobador', None)
    if id_aprobador is not None:
        aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
        if aprobador:
            aprobador_nombre = aprobador.nombre
            aprobador_apellido = aprobador.apellido
    
    producto_dict = {
        'id_producto': getattr(db_producto, 'id_producto'),
        'nombre': getattr(db_producto, 'nombre'),
        'descripcion': getattr(db_producto, 'descripcion'),
        'id_tipologia': getattr(db_producto, 'id_tipologia'),
        'id_linea': getattr(db_producto, 'id_linea'),
        'fecha_creacion': getattr(db_producto, 'fecha_creacion'),
        'enlace': getattr(db_producto, 'enlace'),
        'repositorio': getattr(db_producto, 'repositorio'),
        'imagen_referencia': getattr(db_producto, 'imagen_referencia'),
        'id_responsable': getattr(db_producto, 'id_responsable'),
        'estado_desarrollo': getattr(db_producto, 'estado_desarrollo'),
        'estado_aprobacion': getattr(db_producto, 'estado_aprobacion'),
        'fecha_registro': getattr(db_producto, 'fecha_registro'),
        'fecha_aprobacion': getattr(db_producto, 'fecha_aprobacion'),
        'id_aprobador': id_aprobador,
        'aprobador_nombre': aprobador_nombre,
        'aprobador_apellido': aprobador_apellido,
        'responsable': db_producto.responsable,
        'tipologia': db_producto.tipologia,
        'linea': db_producto.linea
    }
    
    return schemas.ProductoResponse(**producto_dict)

@router.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Verificar si la tipología existe
    tipologia = db.query(models.Tipologia).filter(models.Tipologia.id_tipologia == producto.id_tipologia).first()
    if not tipologia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La tipología especificada no existe"
        )
    
    # Verificar si la línea de investigación existe
    if producto.id_linea:
        linea = db.query(models.LineaInvestigacion).filter(models.LineaInvestigacion.id_linea == producto.id_linea).first()
        if not linea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La línea de investigación especificada no existe"
            )
    
    # Verificar si el responsable existe
    responsable = db.query(models.Usuario).filter(models.Usuario.id_usuario == producto.id_responsable).first()
    if not responsable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El responsable especificado no existe"
        )
    
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    db.delete(db_producto)
    db.commit()
    return None

@router.put("/productos/{producto_id}/estado", response_model=schemas.Producto)
def update_estado_producto(
    producto_id: int,
    estado: models.ProductoEstadoDesarrollo,
    db: Session = Depends(get_db)
):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    setattr(db_producto, 'estado_desarrollo', estado)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/productos/{producto_id}/aprobar", response_model=schemas.Producto)
def aprobar_producto(producto_id: int, id_aprobador: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Verificar si el aprobador existe
    aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
    if not aprobador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El aprobador especificado no existe"
        )
    
    setattr(db_producto, 'estado_aprobacion', models.ProductoEstado.aprobado)
    setattr(db_producto, 'id_aprobador', id_aprobador)
    setattr(db_producto, 'fecha_aprobacion', datetime.utcnow())
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/productos/{producto_id}/rechazar", response_model=schemas.Producto)
def rechazar_producto(producto_id: int, id_aprobador: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Verificar si el aprobador existe
    aprobador = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_aprobador).first()
    if not aprobador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El aprobador especificado no existe"
        )
    
    setattr(db_producto, 'estado_aprobacion', models.ProductoEstado.rechazado)
    setattr(db_producto, 'id_aprobador', id_aprobador)
    setattr(db_producto, 'fecha_aprobacion', datetime.utcnow())
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/productos/{producto_id}/estado-aprobacion", response_model=schemas.ProductoEstadoResponse)
def actualizar_estado_aprobacion_producto(
    producto_id: int, 
    estado_update: schemas.ProductoEstadoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar el estado de aprobación de un producto.
    Permite cambiar el estado a cualquier valor válido (pendiente, aprobado, rechazado).
    Si se proporciona un id_aprobador, se registrará como aprobador y se establecerá la fecha de aprobación.
    """
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
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
        setattr(db_producto, 'id_aprobador', estado_update.id_aprobador)
        setattr(db_producto, 'fecha_aprobacion', datetime.utcnow())
        aprobador_nombre = aprobador.nombre
        aprobador_apellido = aprobador.apellido
    
    # Actualizar el estado
    setattr(db_producto, 'estado_aprobacion', estado_update.estado)
    
    db.commit()
    db.refresh(db_producto)
    
    # Crear mensaje según el estado
    mensaje = f"Estado de aprobación actualizado a '{estado_update.estado}'"
    if aprobador_nombre is not None and aprobador_apellido is not None:
        mensaje += f" por {aprobador_nombre} {aprobador_apellido}"
    
    return schemas.ProductoEstadoResponse(
        id_producto=getattr(db_producto, 'id_producto'),
        nombre=getattr(db_producto, 'nombre'),
        estado=getattr(db_producto, 'estado_aprobacion'),
        fecha_aprobacion=getattr(db_producto, 'fecha_aprobacion'),
        aprobador_nombre=str(aprobador_nombre) if aprobador_nombre is not None else None,
        aprobador_apellido=str(aprobador_apellido) if aprobador_apellido is not None else None,
        mensaje=mensaje
    ) 