from fastapi import APIRouter,HTTPException
from app.db import conectar

router = APIRouter(prefix="/reportes",tags=["Reportes"])

@router.get("/prestamos-por-socio")
def prestamos_por_socio():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT s.nombre, COUNT(*) AS total_prestamos, COUNT(CASE WHEN p.estado = 'activo' THEN 1 END) AS prestamos_activos FROM socios s LEFT JOIN prestamos_biblioteca p ON s.id = p.socio_id GROUP BY s.nombre ORDER BY total_prestamos DESC;")
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"No se ha realizado ningún préstamo aún.")
            return [
                {
                    "socio_nombre": r[0],
                    "total_prestamos": r[1],
                    "prestamos_activos": r[2]
                }
                for r in resultado
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al listar préstamos por socio: {str(e)}")

@router.get("/libros-mas-prestados")
def libros_mas_prestados():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT l.titulo AS titulo, COUNT(*) AS ejemplares_prestados FROM prestamos_biblioteca p LEFT JOIN libros l ON l.id = p.libro_id GROUP BY l.titulo ORDER BY ejemplares_prestados DESC LIMIT 5;")
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"No se ha realizado ningún préstamo aún.")
            return [
                {
                    "titulo": r[0],
                    "ejemplares_prestados": r[1]
                }
                for r in resultado
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al listar los libros mas prestados: {str(e)}")

@router.get("/socios-activos")
def socios_activos():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(CASE WHEN activo = TRUE THEN 1 END) AS activos, COUNT(CASE WHEN activo = FALSE THEN 1 END) AS inactivos FROM socios;")
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"No existe ningún socio aún.")
            return {
                "socios_activos": resultado[0],
                "socios_inactivos": resultado[1]
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el reporte: {str(e)}")

@router.get("/prestamos-mensuales")
def prestamos_mensuales():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT EXTRACT(YEAR FROM fecha_prestamo) AS anio,EXTRACT(MONTH FROM fecha_prestamo) AS mes, COUNT(id) AS num_prestamos FROM prestamos_biblioteca WHERE fecha_prestamo >= CURRENT_DATE - INTERVAL '6 months' GROUP BY anio,mes ORDER BY anio,mes;")
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"No se ha realizado ningún prestamo aún.")
            return [
                {
                    "año": r[0],
                    "mes": r[1],
                    "num_prestamos": r[2]
                }
                for r in resultado
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al obtener reporte: {str(e)}")

@router.get("/libros-sin-stock")
def libros_sin_stock():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id,titulo,autor,ejemplares_disponibles FROM libros WHERE ejemplares_disponibles = 0;")
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"No existen libros aún.")
            return [
                {
                    "libro_id": r[0],
                    "titulo": r[1],
                    "autor": r[2],
                    "ejemplares_disponibles": r[3]
                }
                for r in resultado
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener reporte: {str(e)}")

@router.get("/prestamos-retrasados")
def prestamos_retrasados():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT p.id, s.nombre,l.titulo,CURRENT_DATE - p.fecha_prestamo AS dias_prestado FROM prestamos_biblioteca p JOIN socios s ON s.id = p.socio_id JOIN libros l ON l.id = p.libro_id WHERE p.estado = 'activo' AND CURRENT_DATE - p.fecha_prestamo > 7;")
            resultado = cursor.fetchall()
            if not resultado:
                raise HTTPException(status_code=404,detail=f"No se ha realizado ningún prestamo aún.")
            return [
                {
                    "id": r[0],
                    "nombre_socio": r[1],
                    "titulo_libro": r[2],
                    "dias_prestado": r[3]
                }
                for r in resultado
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al obtener reporte: {str(e)}")