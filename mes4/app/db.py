import psycopg2
from app.config import settings

def conectar():
    """Establece conexión con PostgreSQL y retorna la conexión."""
    try:
        conexion = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        print("✅ Conexión a PostgreSQL establecida")
        return conexion
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        raise
