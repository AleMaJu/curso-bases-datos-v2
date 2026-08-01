from fastapi import FastAPI
from app.routers import alumnos,libros,prestamos
from app.exceptions import setup_exception_handlers

app = FastAPI(
    title="Mi API con Estructura Profesional",
    description="API para gestionar alumnos con FastAPI y PostgreSQL",
    version="1.0.0",
    contact={
        "name": "AleMaJu",
        "email": "macedojulca@gmail.com"
    }
)

# Configurar manejadores de errores globales
setup_exception_handlers(app)

# Incluir los routers
app.include_router(alumnos.router)
app.include_router(libros.router)
app.include_router(prestamos.router)

@app.get("/", tags=["Inicio"])
def hola_mundo():
    """Endpoint de bienvenida."""
    return {"mensaje": "Bienvenido a mi API!"}

@app.get("/health", tags=["Inicio"])
def health_check():
    """Verificar que la API está funcionando."""
    return {"status": "ok", "mensaje": "API operativa"}