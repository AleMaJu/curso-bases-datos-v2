from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def setup_exception_handlers(app):

    # Manejar errores de validación de Pydantic (422)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errores = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"]) # error["loc"] = ("body", "direccion", "codigo_postal") -> ej: field = "body.direccion.codigo_postal"
            msg = error["msg"]
            errores.append(f"{field}: {msg}")
        return JSONResponse(
            status_code=422, # El error 422 aparece cuando los datos son válidos, pero no cumplen con la condición del sistema o si faltan más datos Ej: edad = 0 -> está bien, pero debe ser mayor a 0.
            content={
                "detail": "Error de validación en los datos enviados",
                "errors": errores
                }
        )

    # Manejar errores HTTP generales
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    # Manejar errores inesperados (500)
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Error interno del servidor",
                "error": str(exc)
            }
        )
