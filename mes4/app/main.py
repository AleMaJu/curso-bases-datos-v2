from fastapi import FastAPI
from app.routers import alumnos,libros,prestamos,reportes
from app.exceptions import setup_exception_handlers

app = FastAPI(
    title="API de Gestión de Biblioteca",
    description="API para gestionar alumnos, libros, préstamos y reportes",
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
app.include_router(reportes.router)

@app.get("/", tags=["Inicio"])
def hola_mundo():
    """Endpoint de bienvenida."""
    return {"mensaje": "¡Bienvenido a la API de Biblioteca!"}

@app.get("/health", tags=["Inicio"])
def health_check():
    """Verificar que la API está funcionando."""
    return {"status": "ok", "mensaje": "API operativa"}