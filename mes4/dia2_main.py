from fastapi import FastAPI,HTTPException
from db import conectar
import os
import psycopg2
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI(title="Mi segunda API") # URL: http://127.0.0.1:8000

load_dotenv()

class AlumnoCreate(BaseModel):
    nombre: str
    edad: int

class Alumno(BaseModel):
    id: int
    nombre: str
    edad: int

@app.get("/alumnos",response_model=list[Alumno],status_code=200)
def listar_alumnos():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos;")
        resultado = cursor.fetchall()
        return [{"id":a[0],"nombre":a[1],"edad":a[2]} for a in resultado]

@app.post("/alumnos",response_model=Alumno,status_code=201)
def crear_alumno(alumno: AlumnoCreate):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO alumnos(nombre,edad) VALUES(%s,%s) RETURNING id;",(alumno.nombre,alumno.edad))
            conexion.commit()
            nuevo_id = cursor.fetchone()[0]
            return {"id": nuevo_id,"nombre":alumno.nombre,"edad":alumno.edad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear alumno: {str(e)}")

@app.get("/alumnos/{alumno_id}",response_model=Alumno)
def buscar_alumno(alumno_id:int):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM alumnos WHERE id = %s;",(alumno_id,))
            alumno = cursor.fetchone()
            if not alumno:
                raise HTTPException(status_code=404,detail=f"Alumno con la id '{alumno_id}' no encontrado.")
            return {"id": alumno[0],"nombre":alumno[1],"edad":alumno[2]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar alumno: {str(e)}")
@app.delete("/alumnos/{alumno_id}",status_code=204)
def eliminar_alumno(alumno_id: int):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM alumnos WHERE id = %s;", (alumno_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Alumno con la id '{alumno_id}' no encontrado.")
            cursor.execute("DELETE FROM alumnos WHERE id = %s;",(alumno_id,))
            conexion.commit()
            return  # No devuelve contenido (status_code 204)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar alumno: {str(e)}")

@app.put("/alumnos/{alumno_id}",response_model=Alumno)
def actualizar_alumno(alumno_id: int, alumno:AlumnoCreate):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM alumnos WHERE id =%s;",(alumno_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404,detail=f"Alumno con la id '{alumno_id}' no encontrado.")
            cursor.execute("UPDATE alumnos SET nombre = %s, edad = %s WHERE id = %s;",(alumno.nombre,alumno.edad,alumno_id))
            conexion.commit()
            return {"id":alumno_id,"nombre":alumno.nombre,"edad":alumno.edad}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al actualizar alumno: {str(e)}")