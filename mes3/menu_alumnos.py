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

def leer_alumnos():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos;")
        resultado = cursor.fetchall()
        if not resultado:
            print("No hay ningún alumno en la base de datos.")
        for alumno in resultado:
            print(f"ID {alumno[0]}: {alumno[1]}. Edad: {alumno[2]}.")
def insertar_alumnos(lista_alumnos):
    with conectar() as conexion:
        if not lista_alumnos:
            print("Los argumentos que has enviado están vacíos.")
            return
        cursor = conexion.cursor()
        cursor.executemany("INSERT alumnos(nombre,edad) VALUES (%s,%s);",lista_alumnos)
        conexion.commit()
        print(f"Se han agregado {len(lista_alumnos)} alumno(s).")

def eliminar_alumno(id_alumno):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos WHERE id = %s;",(id_alumno,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"No existe el alumno con ID {id_alumno}.")
            return
        cursor.execute("DELETE FROM alumnos WHERE id = %s;",(id_alumno,))
        conexion.commit()
        print(f"Se ha eliminado alumno con ID {id_alumno}.")

def actualizar_alumno(id_alumno,campo,valor_nuevo):
    with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM alumnos WHERE id = %s;",(id_alumno,))
            resultado = cursor.fetchone()
            if not resultado:
                print(f"No existe el alumno con ID {id_alumno}.")
                return
            consulta = f"UPDATE alumnos SET {campo} = %s WHERE id = %s;"
            cursor.execute(consulta,(valor_nuevo,id_alumno))
            conexion.commit()
            print(f"Se ha actualizado el campo '{campo}' del alumno con ID {id_alumno}.")

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
                print("Error: Debe ser un valor entero.")
def pedir_float(mensaje):
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
                print("Error: Debe ser un valor decimal (ej: 14.99).")
def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("No puede estar vacío.")
            continue
        return texto

def mostrar_menu():
    print("\n" + "="*40)
    print("   GESTIÓN DE ALUMNOS")
    print("="*40)
    print("1. Listar alumnos")
    print("2. Insertar alumno")
    print("3. Actualizar alumno")
    print("4. Eliminar alumno")
    print("5. Salir")
    print("="*40)

def main():
    """Función principal del programa."""
    while True:
        mostrar_menu()
        opcion = pedir_entero("Elige una opción (1-5): ")
        match(opcion):
            case 1:
                leer_alumnos()
            case 2:
                alumnos = []
                cantidad =pedir_entero("¿Cuántos alumnos quieres agregar? ")
                for i in range(cantidad):
                    print(f"\nAlumno {i+1}:")
                    nombre = pedir_texto("Nombre: ")
                    edad = pedir_entero("Edad: ")
                    alumnos.append((nombre,edad))
                insertar_alumnos(alumnos)
            case 3:
                id_alumno = pedir_entero("ID del alumno a actualizar: ")
                print("Campos disponibles: nombre, edad")
                campo = pedir_texto("Campo a actualizar: ")
                if campo == "edad":
                    valor_nuevo = pedir_entero("Nueva edad:")
                    actualizar_alumno(id_alumno,campo,valor_nuevo)
                else:
                    valor_nuevo = pedir_texto("Nuevo nombre: ")
                    actualizar_alumno(id_alumno,campo,valor_nuevo)
            case 4:
                id_alumno = pedir_entero("ID del alumno a eliminar: ")
                confirmar = input(f"¿Eliminar alumno con ID {id_alumno}? (s/n): ").strip().lower()
                if confirmar == 's':
                    eliminar_alumno(id_alumno)
                else:
                    print("Eliminación cancelada.")
            case 5:
                print("¡Hasta luego!")
                break
            case _:
                print("Opción no válida. Elige 1-5.")

if __name__ == "__main__":
    main()