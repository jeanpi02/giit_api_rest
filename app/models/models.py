from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base
import enum

class UsuarioEstado(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    pendiente = "pendiente"

class LineaInvestigacionEstado(str, enum.Enum):
    activa = "activa"
    inactiva = "inactiva"

class PublicacionEstado(str, enum.Enum):
    pendiente = "pendiente"
    aprobada = "aprobada"
    rechazada = "rechazada"

class ProductoEstadoDesarrollo(str, enum.Enum):
    idea = "idea"
    desarrollo = "desarrollo"
    pruebas = "pruebas"
    completado = "completado"

class ProductoEstado(str, enum.Enum):
    pendiente = "pendiente"
    aprobado = "aprobado"
    rechazado = "rechazado"

class SemilleroEstado(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    en_proceso = "en_proceso"

class Rol(Base):
    __tablename__ = "Roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)

    usuarios = relationship("Usuario", back_populates="rol")

class Usuario(Base):
    __tablename__ = "Usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("Roles.id_rol"), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    telefono = Column(String(20))
    institucion = Column(String(100))
    especialidad = Column(String(100))
    foto_perfil = Column(String(255))
    estado = Column(Enum(UsuarioEstado), default=UsuarioEstado.pendiente)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime)

    rol = relationship("Rol", back_populates="usuarios")
    lineas_investigacion = relationship("LineaInvestigacion", back_populates="responsable")
    publicaciones_autor = relationship("Publicacion", 
                                     foreign_keys="Publicacion.id_autor_principal",
                                     back_populates="autor_principal")
    publicaciones_aprobador = relationship("Publicacion",
                                         foreign_keys="Publicacion.id_aprobador",
                                         back_populates="aprobador")
    productos_aprobador = relationship("Producto",
                                     foreign_keys="Producto.id_aprobador",
                                     back_populates="aprobador")
    eventos = relationship("Evento", back_populates="creador")
    productos = relationship("Producto", foreign_keys="Producto.id_responsable", back_populates="responsable")

class LineaInvestigacion(Base):
    __tablename__ = "LineasInvestigacion"

    id_linea = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    imagen_logo = Column(String(255))
    id_responsable = Column(Integer, ForeignKey("Usuarios.id_usuario"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(Enum(LineaInvestigacionEstado), default=LineaInvestigacionEstado.activa)

    responsable = relationship("Usuario", back_populates="lineas_investigacion")
    publicaciones = relationship("Publicacion", back_populates="linea")
    productos = relationship("Producto", back_populates="linea")

class Publicacion(Base):
    __tablename__ = "Publicaciones"

    id_publicacion = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    resumen = Column(Text)
    autores = Column(Text, nullable=False)
    revista_conferencia = Column(String(255))
    fecha_publicacion = Column(Date)
    enlace = Column(String(255))
    id_linea = Column(Integer, ForeignKey("LineasInvestigacion.id_linea"))
    id_autor_principal = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    estado = Column(Enum(PublicacionEstado), default=PublicacionEstado.pendiente)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_aprobacion = Column(DateTime)
    id_aprobador = Column(Integer, ForeignKey("Usuarios.id_usuario"))

    linea = relationship("LineaInvestigacion", back_populates="publicaciones")
    autor_principal = relationship("Usuario", foreign_keys=[id_autor_principal], back_populates="publicaciones_autor")
    aprobador = relationship("Usuario", foreign_keys=[id_aprobador], back_populates="publicaciones_aprobador")

class Evento(Base):
    __tablename__ = "Eventos"

    id_evento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    tipo_evento = Column(String(100))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    lugar = Column(String(255))
    organizador = Column(String(255))
    enlace = Column(String(255))
    foto_evento = Column(String(255))
    id_creador = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    creador = relationship("Usuario", back_populates="eventos")

class Tipologia(Base):
    __tablename__ = "Tipologias"

    id_tipologia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    productos = relationship("Producto", back_populates="tipologia")

class Producto(Base):
    __tablename__ = "Productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    id_tipologia = Column(Integer, ForeignKey("Tipologias.id_tipologia"), nullable=False)
    id_linea = Column(Integer, ForeignKey("LineasInvestigacion.id_linea"))
    id_responsable = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    fecha_creacion = Column(Date)
    estado_desarrollo = Column(Enum(ProductoEstadoDesarrollo), default=ProductoEstadoDesarrollo.idea)
    estado_aprobacion = Column(Enum(ProductoEstado), default=ProductoEstado.pendiente)
    fecha_aprobacion = Column(DateTime)
    id_aprobador = Column(Integer, ForeignKey("Usuarios.id_usuario"))
    enlace = Column(String(255))
    repositorio = Column(String(255))
    imagen_referencia = Column(String(255))
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    tipologia = relationship("Tipologia", back_populates="productos")
    linea = relationship("LineaInvestigacion", back_populates="productos")
    responsable = relationship("Usuario", foreign_keys=[id_responsable], back_populates="productos")
    aprobador = relationship("Usuario", foreign_keys=[id_aprobador], back_populates="productos_aprobador")

class CarruselFoto(Base):
    __tablename__ = "CarruselFotos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    orden = Column(Integer, nullable=False, unique=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow) 