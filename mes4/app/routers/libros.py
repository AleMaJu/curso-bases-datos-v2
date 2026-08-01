from fastapi import APIRouter, HTTPException
from app.db import conectar
from app.models import Libro, LibroCreate

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.get("/",response_model=list[Libro])
def listar_libros():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM libros;")
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail="No hay ningún libro.")
            return [
                {
                    "id": l[0],
                    "titulo": l[1],
                    "autor": l[2],
                    "genero": l[3],
                    "anio_publicacion": l[4],
                    "ejemplares_disponibles": l[5]
                }
                for l in resultado
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al listar libros: {str(e)}")

@router.post("/{libro_id}",response_model=Libro, status_code=201)
def crear_libro(libro: LibroCreate):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO libros(titulo,autor,anio_publicacion,ejemplares_disponibles) VALUES(%s,%s,%s,%s,%s) RETURNING id;",(libro.titulo,libro.autor,libro.anio_publicacion,libro.ejemplares_disponibles))
            libro_id = cursor.fetchone()[0]
            conexion.commit()
            return[
                {
                    "id": libro_id,
                    "titulo": libro.titulo,
                    "autor": libro.autor,
                    "año_publicacion": libro.anio_publicacion,
                    "ejemplares disponibles": libro.ejemplares_disponibles
                }
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al crear libro: {str(e)}")

@router.put("/{libro_id}")
def actualizar_libro(libro_id: int, libro: LibroCreate):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM libros WHERE id = %s;",(libro_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404,detail=f"Libro con id '{libro_id}' no existe.")
            cursor.execute("UPDATE libros SET titulo= %s,autor = %s,anio_publicacion = %s,ejemplares_disponible = %s WHERE id = %s;",(libro.titulo,libro.autor,libro.anio_publicacion,libro.ejemplares_disponibles,libro_id))
            conexion.commit()
            return {
                "id": libro_id,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "año_publicacion": libro.anio_publicacion,
                "ejemplares disponibles": libro.ejemplares_disponibles
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al actualizar el libro: {str(e)}")

@router.delete("/{libro_id}",status_code=204)
def eliminar_libro(libro_id: int):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM libros WHERE id = %s;",(libro_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404,detail=f"Libro con id '{libro_id}' no existe.")
            cursor.execute("DELETE FROM libros WHERE id = %s;",(libro_id,))
            conexion.commit()
            return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al eliminar libro: {str(e)}")

@router.get("/buscar/por-titulo",response_model=Libro)
def buscar_libro(titulo: str):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM libros WHERE titulo = %s;",(titulo.strip(),))
            libro = cursor.fetchone()
            if not libro:
                raise HTTPException(status_code=404,detail=f"Libro con título '{titulo.strip()}' no existe.")
            return {
                "id": libro[0],
                "titulo": libro[1],
                "autor": libro[2],
                "año_publicacion": libro[3],
                "ejemplares disponibles": libro[4]
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al buscar libro: {str(e)}")