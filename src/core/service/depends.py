from typing import Optional
from fastapi import Depends, HTTPException, Request
from fastapi_sessions.frontends.session_frontend import FrontendError
from core.model.role import RoleEnum
from core.service.config import backend, cookie, verifier
from core.service.session_data import SessionData

async def get_session(request: Request) -> Optional[SessionData]:
    try:
        session_id = cookie(request)
        if isinstance(session_id, FrontendError):
            return None
        return await backend.read(session_id)
    except Exception:
        return None
    
def require_role(roles: list[RoleEnum]):
    print("---------ROLE----------\nRequired roles:", roles, "\n-------------------")
    async def role_checker(session: SessionData = Depends(verifier)) -> SessionData:
        if session is None or session.role not in [role.value for role in roles]:
            raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este recurso.")
        return session
    return role_checker