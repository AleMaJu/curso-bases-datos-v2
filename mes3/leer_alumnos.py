import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    conexion = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )
    return conexion

def main():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos;")
        alumnos = cursor.fetchall()
        for alumno in alumnos:
            print(f"ID {alumno[0]}: {alumno[1]}. Edad: {alumno[2]}.")

if __name__ == "__main__":
    main()
