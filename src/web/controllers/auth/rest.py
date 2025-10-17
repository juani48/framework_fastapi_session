from typing import Optional
from core.service.session_data import SessionData
from core.service.session import create_cookie
from fastapi import Depends, Request, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from core.repository.user_repo import UserRepository
from core.service.validator import validate_login_json, validate_signin_json
from core.service.config import backend, cookie
from uuid import UUID
from core.database import get_db_session
from core.service.decorators import handle_errors

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
@handle_errors(message="Error en el registro")
async def register(request: Request, response: Response, session: AsyncSession = Depends(get_db_session)):
    json = await request.json()
    validate_signin_json(json)
    
    user = await UserRepository.create_user(user_data=json, session=session)
    await create_cookie(response, user)

    return 200

@router.post("/login")
@handle_errors(message="Error en el inicio de sesión")
async def login(request: Request, response: Response, session: AsyncSession = Depends(get_db_session)):
    json = await request.json()
    validate_login_json(json)

    email = json.get("email")
    password = json.get("password")
    user = await UserRepository.login_user(email, password, session)
    
    await create_cookie(response, user)
    return 200


@router.put("/logout")
@handle_errors(message="Error al cerrar sesión")
async def logout(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return 200

