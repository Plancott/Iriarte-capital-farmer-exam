from sqlalchemy.orm import Session
from p1.app import models, schemas
from datetime import datetime
from uuid import uuid4

# Precios base para los servicios
precios = {
    "Constitución de empresa": 1500.0,
    "Defensa laboral": 2000.0,
    "Consultoría tributaria": 800.0
}
# Función para generar un número de cotización único
def generar_numero_cotizacion():
    return f"COT-2025-{str(uuid4())[:4].upper()}"

# Función para crear una cotización en la base de datos
def crear_cotizacion(db: Session, data: schemas.CotizacionCreate):
    numero = generar_numero_cotizacion()
    precio = precios.get(data.tipo_servicio, 0.0)

    cotizacion = models.Cotizacion(
        numero=numero,
        nombre_cliente=data.nombre_cliente,
        email=data.email,
        tipo_servicio=data.tipo_servicio,
        precio=precio,
        descripcion=data.descripcion
    )
    db.add(cotizacion)
    db.commit()
    db.refresh(cotizacion)
    return cotizacion