from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db_session
from core.repository.admin_repo import AdminRepository
from core.repository.role_repo import RoleRepository
from core.service.session_data import SessionData
from web.entities.user_read import UserRead
from core.service.config import verifier, cookie
from core.service.decorators import handle_errors


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.get("/user-list", dependencies=[Depends(cookie)],  response_class=JSONResponse)
@handle_errors(message="Error al obtener la lista de usuarios")
async def user_list(request: Request, response: Response, db_session: AsyncSession = Depends(get_db_session), session: SessionData = Depends(verifier)):
    users = await AdminRepository.get_all_users(db_session)
    user_list = [UserRead(user).model_dump() for user in users]
    return JSONResponse(content=jsonable_encoder({"users": user_list}), status_code=201)
    

@router.get("/role-list", dependencies=[Depends(cookie)],  response_class=JSONResponse)
@handle_errors(message="Error al obtener la lista de roles")
async def role_list(request: Request, response: Response, db_session: AsyncSession = Depends(get_db_session), session: SessionData = Depends(verifier)):
    roles = await RoleRepository.get_all_roles(db_session)
    role_list = [role.model_dump() for role in roles]
    return JSONResponse(content=jsonable_encoder({"roles": role_list}), status_code=200)


@router.post("/add-user", dependencies=[Depends(cookie)])
@handle_errors(message="Error al agregar el usuario")
async def add_user(request: Request, response: Response, db_session: AsyncSession = Depends(get_db_session), session: SessionData = Depends(verifier)):
    user_data = await request.json()
    user_model = await AdminRepository.add_user_by_admin(user_data, db_session)
    new_user: UserRead = user_model
    return JSONResponse(content=jsonable_encoder(new_user.model_dump()), status_code=201)