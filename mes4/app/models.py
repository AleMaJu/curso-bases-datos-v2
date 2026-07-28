from pydantic import BaseModel, Field, validator

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