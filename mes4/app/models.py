from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

# ALUMNOS
class AlumnoCreate(BaseModel):
    """Modelo para crear un nuevo alumno."""
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del alumno (2-50 caracteres)")
    edad: int = Field(..., gt=0, lt=120, description="Edad del alumno (1-119 años)")

    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()
    
    # Validación personalizada para la edad
    @validator('edad')
    def edad_no_valida(cls, v):
        if v == 0:
            raise ValueError('La edad no puede ser 0')
        elif(v < 0):
            raise ValueError('La edad no puede ser negativa')
        return v


class Alumno(BaseModel):
    """Modelo para representar un alumno con ID."""
    id: int
    nombre: str
    edad: int

# LIBROS
class LibroCreate(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=200)
    autor: str = Field(..., min_length=2, max_length=100)
    genero: str = Field(..., min_length=2, max_length=50)
    anio_publicacion: int = Field(..., gt=1000, lt=2026)
    ejemplares_disponibles: int = Field(..., ge=0)

    @validator('titulo')
    def titulo_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El título no puede estar vacío')
        return v.strip()
    
    @validator('autor')
    def autor_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El autor no puede estar vacío')
        return v.strip()
    
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    anio_publicacion: int
    ejemplares_disponibles: int


# PRESTAMOS
class PrestamoCreate(BaseModel):
    socio_id: int = Field(..., gt=0)
    libro_id: int = Field(..., gt=0)

class Prestamo(BaseModel):
    id: int
    socio_id: int
    libro_id: int
    fecha_prestamo: date
    estado: str  # 'activo' o 'devuelto'
    socio_nombre: Optional[str] = None
    libro_titulo: Optional[str] = None