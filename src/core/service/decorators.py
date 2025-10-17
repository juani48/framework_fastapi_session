from functools import wraps
from fastapi import Response

from core.model.role import RoleEnum


def handle_errors( message):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except ValueError as ve:
                return Response(content=message + ": " + str(ve), status_code=400)
            except Exception as e:
                return Response(content="Error interno del servidor.", status_code=500)
        return wrapper
    return decorator

def exception_handler(message: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as ve:
                return Response(content=message + ": " + str(ve), status_code=400)
            except Exception as e:
                return Response(content="Error interno del servidor.", status_code=500)
        return wrapper
    return decorator