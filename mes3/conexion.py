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

    cursor = conexion.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📌 Versión: {version[0]}")
        
    # Cerrar la conexión
    cursor.close()
    conexion.close()
    print("🔒 Conexión cerrada correctamente")

    return True

def main():
    conectar()
    
if __name__ == "__main__":
    main()
