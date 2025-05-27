from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from p1.app import models, schemas, crud
from p1.app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="p1/app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

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