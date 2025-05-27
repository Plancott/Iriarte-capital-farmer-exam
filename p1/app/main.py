from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from p1.app import models, schemas, crud
from p1.app.database import engine, SessionLocal
from p1.app.ia_utils import analizar_con_ia

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="p1/app/templates")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#End point del formulario
@app.get("/", response_class=HTMLResponse)
def formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})


#End point para generar la cotización
@app.post("/generar", response_class=JSONResponse)
def generar(
    nombre_cliente: str = Form(...),
    email: str = Form(...),
    tipo_servicio: str = Form(...),
    descripcion: str = Form(...),
    db: Session = Depends(get_db)
):
    data = schemas.CotizacionCreate(
        nombre_cliente=nombre_cliente,
        email=email,
        tipo_servicio=tipo_servicio,
        descripcion=descripcion
    )
    cotizacion = crud.crear_cotizacion(db, data)
    return cotizacion

#End point para generar la cotización con IA
@app.post("/generar-ia", response_class=JSONResponse)
def generar(
    nombre_cliente: str = Form(...),
    email: str = Form(...),
    tipo_servicio: str = Form(...),
    descripcion: str = Form(...),
    db: Session = Depends(get_db)
):
    # Precios base
    precios = {
        "Constitución de empresa": 1500,
        "Defensa laboral": 2000,
        "Consultoría tributaria": 800
    }
    precio_base = precios.get(tipo_servicio, 0)

    # Llamar a IA para análisis
    resultado_ia = analizar_con_ia(descripcion, tipo_servicio)
    ajuste = resultado_ia.get("ajuste_precio", 0)

    # Crear cotización en la BD
    data = schemas.CotizacionCreate(
        nombre_cliente=nombre_cliente,
        email=email,
        tipo_servicio=tipo_servicio,
        descripcion=descripcion,
    )
    cotizacion = crud.crear_cotizacion(db, data)
    return {
        "cotizacion": {
            "id": cotizacion.id,
            "numero": cotizacion.numero,
            "nombre_cliente": cotizacion.nombre_cliente,
            "email": cotizacion.email,
            "tipo_servicio": cotizacion.tipo_servicio,
            "descripcion": cotizacion.descripcion,
            "precio_base": precio_base,
            "ajuste_por_ia": precio_base*(ajuste+1),
            "precio_final": cotizacion.precio,
            "fecha": cotizacion.fecha.strftime("%Y-%m-%d")
        },
        "analisis_ia": resultado_ia
    }

