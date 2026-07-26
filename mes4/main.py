from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mi primera API")

@app.get("/") # La ruta del URL donde se ejecuta: http://127.0.0.1:8000/
def hola_mundo():
    return {"mensaje":"hola mundo!"}

@app.get("/alumnos") # La ruta del URL donde se ejecuta: http://127.0.0.1:8000/alumnos
def listar_alumnos():
    # Por ahora, devolvemos datos de ejemplo
    return [
        {"id": 1, "nombre": "Carlos", "edad": 22},
        {"id": 2, "nombre": "Laura", "edad": 25}
    ]
@app.get("/saludo/{nombre}") # La ruta del URL donde se ejecuta: http://127.0.0.1:8000/saludo/nombre (dependerá del varlor de 'nombre')
def saludo_personalizado(nombre: str):
    return {"mensaje": f"¡Hola, {nombre}! ¡Bienvenido a FastAPI!"}

@app.get("/suma/{a}/{b}") # La ruta del URL donde se ejecuta: http://127.0.0.1:8000/suma/a/b (dependerá de los varlores de 'a' y 'b')
def suma(a: int,b: int):
    return {"operacion":"suma","a":a,"b":b,"resultado":a+b,"mensaje":f"La suma entre {a} y {b} es: {a+b}."}

@app.get("/buscar")
def buscar_alumnos(nombre: str = None,edad_minima: int = 0):

    alumnos = [
        {"id": 1, "nombre": "Carlos", "edad": 22},
        {"id": 2, "nombre": "Laura", "edad": 25},
        {"id": 3, "nombre": "Pedro", "edad": 18}
    ]

    if nombre:
        alumnos = [a for a in alumnos if nombre.lower() in a["nombre"].lower()]
    if edad_minima > 0:
        alumnos = [a for a in alumnos if a["edad"] >= edad_minima]

    return {"resultados":alumnos}

class AlumnoCreate(BaseModel):
    nombre: str
    edad: int

@app.post("/alumnos")
def crear_alumno(alumno: AlumnoCreate):
    nuevo_alumno = {
        "id": 100,  # Simulado
        "nombre": alumno.nombre,
        "edad": alumno.edad
    }
    return {"mensaje":"Alumno creado","alumno":nuevo_alumno}

