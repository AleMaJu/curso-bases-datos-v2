from fastapi import APIRouter,HTTPException
from app.db import conectar
from app.models import Prestamo, PrestamoCreate
from datetime import date

router = APIRouter(prefix="/prestamos",tags=["Préstamos"])

@router.get("/",response_model=list[Prestamo])
def listar_prestamos():
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("""SELECT p.id, p.socio_id, p.libro_id, p.fecha_prestamo, p.estado, s.nombre AS socio_nombre, l.titulo AS libro_titulo FROM prestamos_biblioteca p JOIN socios s ON p.socio_id = s.id JOIN libros l ON p.libro_id = l.id ORDER BY p.fecha_prestamo DESC;""")
            prestamos = cursor.fetchall()
            if not prestamos:
                raise HTTPException(status_code=404,detail=f"No hay ningún préstamo.")
            return [
                {
                    "id": p[0],
                    "socio_id": p[1],
                    "libro_id": p[2],
                    "fecha_prestamo": p[3],
                    "estado": p[4],
                    "socio_nombre": p[5],
                    "libro_titulo": p[6]
                }
                for p in prestamos
            ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al listar préstamos: {str(e)}")

@router.post("/{prestamo_id}",status_code=201,response_model=PrestamoCreate)
def crear_prestamo(prestamo: PrestamoCreate):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()

            cursor.execute("SELECT id FROM socios WHERE id = %s;",(prestamo.socio_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Socio con id {prestamo.socio_id} no encontrado.")
            
            cursor.execute("SELECT ejemplares_disponibles FROM libros WHERE id = %s;", (prestamo.libro_id,))
            libro = cursor.fetchone()
            if not libro:
                raise HTTPException(status_code=404, detail=f"Libro con id {prestamo.libro_id} no encontrado.")
            if libro[0] <= 0:
                raise HTTPException(status_code=400, detail="No hay ejemplares disponibles de este libro.")

            fecha_prestamo = date.today()
            cursor.execute("INSERT INTO prestamos_biblioteca(socio_id,libro_id,fecha_prestamo,estado) VALUES(%s,%s,%s,'activo') RETURNING id;",(prestamo.socio_id,prestamo.libro_id,fecha_prestamo))
            prestamo_id = cursor.fetchone()[0]

            # Reducir ejemplares disponibles
            cursor.execute("UPDATE libros SET ejemplares_disponibles = ejemplares_disponibles - 1 WHERE id = %s;",(prestamo.libro_id,))
            conexion.commit()
            return {
                "id": prestamo_id,
                "socio_id": prestamo.socio_id,
                "libro_id": prestamo.libro_id,
                "fecha_prestamo": fecha_prestamo,
                "estado": "activo"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al crear préstamo: {str(e)}")

@router.put("/{prestamo_id}/devolver",response_model=PrestamoCreate,status_code=200)
def devolver_libro(prestamo_id: int):
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            
            # Verificar que el préstamo existe y está activo
            cursor.execute(
                "SELECT libro_id, estado FROM prestamos_biblioteca WHERE id = %s;",(prestamo_id,))
            prestamo = cursor.fetchone()
            if not prestamo:
                raise HTTPException(status_code=404, detail=f"Préstamo con ID {prestamo_id} no encontrado.")
            if prestamo[1] == 'devuelto':
                raise HTTPException(status_code=400, detail="Este préstamo ya fue devuelto.")
            
            # Marcar como devuelto
            cursor.execute("UPDATE prestamos_biblioteca SET estado = 'devuelto' WHERE id = %s;",(prestamo_id,))
            
            # Aumentar ejemplares disponibles
            cursor.execute("UPDATE libros SET ejemplares_disponibles = ejemplares_disponibles + 1 WHERE id = %s;",(prestamo[0],))
            conexion.commit()
            
            return {"mensaje": f"Préstamo {prestamo_id} devuelto correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al devolver libro: {str(e)}")
