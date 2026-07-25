import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    """Establece conexión con PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def insertar_alumno(nombre, edad):
    """
    Inserta un nuevo alumno en la tabla alumnos.
    
    Args:
        nombre (str): Nombre del alumno.
        edad (int): Edad del alumno.
    
    Returns:
        bool: True si se insertó correctamente, False en caso contrario.
    """
    try:
        with conectar() as conexion:
            with conexion.cursor() as cursor:
                # Consulta con parámetros (%s) - SEGURO contra SQL Injection
                cursor.execute(
                    "INSERT INTO alumnos (nombre, edad) VALUES (%s, %s);",
                    (nombre, edad)
                )
                conexion.commit()  # Guardar los cambios
                print(f"✅ Alumno '{nombre}' insertado correctamente.")
                return True
    except psycopg2.Error as e:
        print(f"❌ Error al insertar: {e}")
        return False

def main():
    """Función principal para probar inserciones."""
    
    insertar_alumno("Mario", 27)
    insertar_alumno("Sofia", 24)
    insertar_alumno("Luis", 31)
    insertar_alumno("Ana", 29)

if __name__ == "__main__":
    main()