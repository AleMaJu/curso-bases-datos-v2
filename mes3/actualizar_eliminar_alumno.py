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

def actualizar_alumno(id,campo,valor_nuevo):
    with conectar() as conexion:
        cursor = conexion.cursor()
        campos_validos = {
                'nombre': 'nombre',
                'edad': 'edad'
            }
        if campo not in campos_validos:
            print(f"El campo '{campo}' no existe.")
            return
        cursor.execute("SELECT * FROM alumnos WHERE id = %s;",(id,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"El alumno con la ID {id} no existe.")
            return
        consulta = f"UPDATE alumnos SET {campo} = %s WHERE id = %s;"
        cursor.execute(consulta,(valor_nuevo,id))
        conexion.commit()
        print(f"Alumno con ID {id} se ha actualizado el campo '{campo}'.")

def eliminar_alumno(id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos WHERE id = %s;",(id,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"El alumno con la ID {id} no existe.")
            return
        cursor.execute("DELETE FROM alumnos WHERE id = %s;",(id,))
        conexion.commit()
        print(f"El alumno con la ID {id} ha sido eliminado.")

if __name__ == "__main__":
    # Actualizar la edad del alumno con ID 1
    actualizar_alumno(1, "edad", 22)
    
    # Eliminar al alumno con ID 2
    eliminar_alumno(2)
