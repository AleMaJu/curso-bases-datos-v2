from fastapi import FastAPI

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