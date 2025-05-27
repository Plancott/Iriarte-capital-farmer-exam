from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


#Modelo de datos para las cotizaciones
class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True)
    nombre_cliente = Column(String)
    email = Column(String)
    tipo_servicio = Column(String)
    precio = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)
    descripcion = Column(String)