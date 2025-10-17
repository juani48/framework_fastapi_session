from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.database import init_db
from web.controllers.auth import render as auth_render
from web.controllers.auth import rest as auth_rest
from web.controllers import default
from web.controllers.admin import render as admin_render
from web.controllers.admin import rest as admin_rest
from core.service.config import backend, cookie, verifier

__all__ = ["create_app", "app"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app(debug: bool = False) -> FastAPI:
    # Crea y configura la aplicación FastAPI
    app = FastAPI(debug=debug, lifespan=lifespan)

    # Montar archivos estáticos
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    # Registrar los routers
    app.include_router(default.router)
    app.include_router(auth_render.router)
    app.include_router(auth_rest.router)
    app.include_router(admin_render.router)
    app.include_router(admin_rest.router)

    return app

# Exportar una app por defecto para que uvicorn pueda localizarla con `src.web:app`
app = create_app()

templates = Jinja2Templates(directory="src/web/templates")

# Error HTTP general (404, 403, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(
        "error.html",
        { 
            "request": request, 
            "title": "Acceso Denegado", 
            "message": "No posee permisos suficientes para acceder a este recurso." ,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        "error.html",
        { 
            "request": request, 
            "title": "Error interno del servidor", 
            "message": "Ocurrió un error inesperado en el servidor.",
            "status_code": 500
        }
    )
