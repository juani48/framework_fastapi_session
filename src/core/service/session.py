from fastapi import Response
from uuid import uuid4
from core.model.user import UserModel
from core.service.session_data import SessionData
from core.service.config import backend, cookie

async def create_cookie(response: Response, user: UserModel) -> None:
    session_id = uuid4()
    session_data = SessionData(name=user.name, email=user.email, role=user.role.name)
    await backend.create(session_id, session_data) # Guarda la sesión en Redis
    cookie.attach_to_response(response, session_id) # Adjunta la cookie al response
    return