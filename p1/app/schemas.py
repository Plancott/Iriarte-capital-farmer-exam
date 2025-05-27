from pydantic import BaseModel
from datetime import datetime
from pydantic import ConfigDict

class CotizacionCreate(BaseModel):
    nombre_cliente: str
    email: str
    tipo_servicio: str
    descripcion: str

class CotizacionResponse(CotizacionCreate):
    numero: str
    precio: float
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)