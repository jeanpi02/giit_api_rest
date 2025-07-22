from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# Enums
class UsuarioEstado(str, Enum):
    activo = "activo"
    inactivo = "inactivo"
    pendiente = "pendiente"

class LineaInvestigacionEstado(str, Enum):
    activa = "activa"
    inactiva = "inactiva"

class PublicacionEstado(str, Enum):
    pendiente = "pendiente"
    aprobada = "aprobada"
    rechazada = "rechazada"

class ProductoEstadoDesarrollo(str, Enum):
    idea = "idea"
    desarrollo = "desarrollo"
    pruebas = "pruebas"
    completado = "completado"

class ProductoEstado(str, Enum):
    pendiente = "pendiente"
    aprobado = "aprobado"
    rechazado = "rechazado"

class SemilleroEstado(str, Enum):
    activo = "activo"
    inactivo = "inactivo"
    en_proceso = "en_proceso"

# Base Schemas
class RolBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    institucion: Optional[str] = None
    especialidad: Optional[str] = None
    foto_perfil: Optional[str] = None

class LineaInvestigacionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_logo: Optional[str] = None
    id_responsable: Optional[int] = None

class PublicacionBase(BaseModel):
    titulo: str
    resumen: Optional[str] = None
    autores: str
    revista_conferencia: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    enlace: Optional[str] = None
    id_linea: Optional[int] = None

class EventoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_evento: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    enlace: Optional[str] = None
    foto_evento: Optional[str] = None
    id_creador: int

class TipologiaBase(BaseModel):
    nombre: str

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    id_tipologia: int
    id_linea: Optional[int] = None
    fecha_creacion: Optional[date] = None
    enlace: Optional[str] = None
    repositorio: Optional[str] = None
    imagen_referencia: Optional[str] = None

class SemilleroBase(BaseModel):
    nombre: str
    mision: Optional[str] = None
    correo: Optional[str] = None
    nombre_lider: Optional[str] = None
    id_linea: Optional[int] = None

# Create Schemas
class RolCreate(RolBase):
    pass

class UsuarioCreate(UsuarioBase):
    password: str
    id_rol: int
    estado: Optional[UsuarioEstado] = UsuarioEstado.pendiente

class LineaInvestigacionCreate(LineaInvestigacionBase):
    pass

class PublicacionCreate(PublicacionBase):
    id_autor_principal: int

class EventoCreate(EventoBase):
    pass

class TipologiaCreate(TipologiaBase):
    pass

class ProductoCreate(ProductoBase):
    id_responsable: int
    estado_desarrollo: ProductoEstadoDesarrollo

class SemilleroCreate(SemilleroBase):
    pass

# Response Schemas
class Rol(RolBase):
    id_rol: int

    class Config:
        from_attributes = True

class Usuario(UsuarioBase):
    id_usuario: int
    id_rol: int
    password: str
    estado: UsuarioEstado
    fecha_registro: datetime
    ultimo_acceso: Optional[datetime] = None
    rol: Rol

    class Config:
        from_attributes = True

class LineaInvestigacion(LineaInvestigacionBase):
    id_linea: int
    fecha_creacion: datetime
    estado: LineaInvestigacionEstado
    responsable: Optional[Usuario] = None

    class Config:
        from_attributes = True

class Publicacion(PublicacionBase):
    id_publicacion: int
    id_autor_principal: int
    estado: PublicacionEstado
    fecha_registro: datetime
    fecha_aprobacion: Optional[datetime] = None
    id_aprobador: Optional[int] = None
    autor_principal: Usuario
    linea: Optional[LineaInvestigacion] = None

    class Config:
        from_attributes = True

# Schema mejorado para respuestas GET de publicaciones
class PublicacionResponse(PublicacionBase):
    id_publicacion: int
    id_autor_principal: int
    estado: PublicacionEstado
    fecha_registro: datetime
    fecha_aprobacion: Optional[datetime] = None
    id_aprobador: Optional[int] = None
    aprobador_nombre: Optional[str] = None
    aprobador_apellido: Optional[str] = None
    autor_principal: Usuario
    linea: Optional[LineaInvestigacion] = None

    class Config:
        from_attributes = True

class Evento(EventoBase):
    id_evento: int
    id_creador: int
    fecha_registro: datetime
    creador: Usuario

    class Config:
        from_attributes = True

class Tipologia(TipologiaBase):
    id_tipologia: int

    class Config:
        from_attributes = True

class Producto(ProductoBase):
    id_producto: int
    id_responsable: int
    estado_desarrollo: ProductoEstadoDesarrollo
    estado_aprobacion: ProductoEstado
    fecha_registro: datetime
    fecha_aprobacion: Optional[datetime] = None
    id_aprobador: Optional[int] = None
    responsable: Usuario
    tipologia: Tipologia
    linea: Optional[LineaInvestigacion] = None

    class Config:
        from_attributes = True

# Schema mejorado para respuestas GET de productos
class ProductoResponse(ProductoBase):
    id_producto: int
    id_responsable: int
    estado_desarrollo: ProductoEstadoDesarrollo
    estado_aprobacion: ProductoEstado
    fecha_registro: datetime
    fecha_aprobacion: Optional[datetime] = None
    id_aprobador: Optional[int] = None
    aprobador_nombre: Optional[str] = None
    aprobador_apellido: Optional[str] = None
    responsable: Usuario
    tipologia: Tipologia
    linea: Optional[LineaInvestigacion] = None

    class Config:
        from_attributes = True

class Semillero(SemilleroBase):
    id_semillero: int
    estado: SemilleroEstado
    linea: Optional[LineaInvestigacion] = None

    class Config:
        from_attributes = True

# Carrusel Schemas
class CarruselFotoBase(BaseModel):
    url: str
    orden: int

class CarruselFotoCreate(CarruselFotoBase):
    pass

class CarruselFoto(CarruselFotoBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    success: bool
    id_usuario: Optional[int] = None
    username: Optional[str] = None
    rol: Optional[str] = None
    foto_perfil: Optional[str] = None
    mensaje: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Schema para actualizar estado de publicaciones
class PublicacionEstadoUpdate(BaseModel):
    estado: PublicacionEstado
    id_aprobador: Optional[int] = None

# Schema para respuesta de actualización de estado
class PublicacionEstadoResponse(BaseModel):
    id_publicacion: int
    titulo: str
    estado: PublicacionEstado
    fecha_aprobacion: Optional[datetime] = None
    aprobador_nombre: Optional[str] = None
    aprobador_apellido: Optional[str] = None
    mensaje: str

    class Config:
        from_attributes = True

# Schema para actualizar estado de productos
class ProductoEstadoUpdate(BaseModel):
    estado: ProductoEstado
    id_aprobador: Optional[int] = None

# Schema para respuesta de actualización de estado de productos
class ProductoEstadoResponse(BaseModel):
    id_producto: int
    nombre: str
    estado: ProductoEstado
    fecha_aprobacion: Optional[datetime] = None
    aprobador_nombre: Optional[str] = None
    aprobador_apellido: Optional[str] = None
    mensaje: str

    class Config:
        from_attributes = True 