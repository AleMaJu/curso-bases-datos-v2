from fastapi import APIRouter, HTTPException
from app.db import conectar
from app.models import Alumno, AlumnoCreate

# Crear un router con prefijo y etiqueta
router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

@router.get("/", response_model=list[Alumno], status_code=200)
def listar_alumnos():
    """Lista todos los alumnos."""
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, edad FROM alumnos;")
        resultado = cursor.fetchall()
        return [{"id": a[0], "nombre": a[1], "edad": a[2]} for a in resultado]

@router.get("/{alumno_id}", response_model=Alumno, status_code=200)
def buscar_alumno(alumno_id: int):
    """Obtiene un alumno por su ID."""
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, edad FROM alumnos WHERE id = %s;", (alumno_id,))
            alumno = cursor.fetchone()
            if not alumno:
                raise HTTPException(status_code=404, detail=f"Alumno con ID {alumno_id} no encontrado.")
            return {"id": alumno[0], "nombre": alumno[1], "edad": alumno[2]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar alumno: {str(e)}")

@router.post("/", response_model=Alumno, status_code=201)
def crear_alumno(alumno: AlumnoCreate):
    """Crea un nuevo alumno."""
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO alumnos(nombre, edad) VALUES(%s, %s) RETURNING id;",
                (alumno.nombre, alumno.edad)
            )
            nuevo_id = cursor.fetchone()[0]
            conexion.commit()
            return {"id": nuevo_id, "nombre": alumno.nombre, "edad": alumno.edad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear alumno: {str(e)}")

@router.put("/{alumno_id}", response_model=Alumno, status_code=200)
def actualizar_alumno(alumno_id: int, alumno: AlumnoCreate):
    """Actualiza un alumno existente."""
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM alumnos WHERE id = %s;", (alumno_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Alumno con ID {alumno_id} no encontrado.")
            
            cursor.execute(
                "UPDATE alumnos SET nombre = %s, edad = %s WHERE id = %s;",
                (alumno.nombre, alumno.edad, alumno_id)
            )
            conexion.commit()
            return {"id": alumno_id, "nombre": alumno.nombre, "edad": alumno.edad}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar alumno: {str(e)}")

@router.delete("/{alumno_id}", status_code=204)
def eliminar_alumno(alumno_id: int):
    """Elimina un alumno por su ID."""
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM alumnos WHERE id = %s;", (alumno_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Alumno con ID {alumno_id} no encontrado.")
            
            cursor.execute("DELETE FROM alumnos WHERE id = %s;", (alumno_id,))
            conexion.commit()
            return  # No devuelve contenido (status_code 204)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar alumno: {str(e)}")

# Endpoint adicional para búsqueda por nombre
@router.get("/buscar/por-nombre", response_model=list[Alumno], status_code=200)
def buscar_por_nombre(nombre: str):
    """Busca alumnos cuyo nombre contenga el texto."""
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre, edad FROM alumnos WHERE nombre ILIKE %s;",
                (f"%{nombre}%",)
            )
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"Alumno(s) con el nombre '{nombre}' no existe.")
            return [{"id": a[0], "nombre": a[1], "edad": a[2]} for a in resultado]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar alumnos: {str(e)}")