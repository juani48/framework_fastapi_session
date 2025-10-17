from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core.model.role import RoleEnum
from core.service.config import verifier, cookie
from core.service.session_data import SessionData
from core.service.depends import require_role


router = APIRouter(
    prefix="/administrador",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="src/web/templates")

@router.get("/panel", dependencies=[Depends(cookie)], response_class=HTMLResponse)
async def render_admin_dashboard(request: Request, session: SessionData = Depends(require_role([RoleEnum.ADMIN]))):
    return templates.TemplateResponse(
        "admin/dashboard.html", 
        {
            "request": request,
            "session": session
        }
    )

@router.get("/agregar-usuario", dependencies=[Depends(cookie)], response_class=HTMLResponse)
async def render_admin_form_users(request: Request, session: SessionData = Depends(require_role([RoleEnum.ADMIN]))):
    return templates.TemplateResponse(
        "admin/user_form.html",
        {
            "request": request,
            "session": session
        }
    )