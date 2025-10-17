from typing import Optional
from fastapi.responses import HTMLResponse
from core.service.session_data import SessionData
from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from core.service.config import verifier, cookie
from core.service.depends import get_session

router = APIRouter(
    prefix="",
    tags=["default"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="src/web/templates")

@router.get("/", response_class=HTMLResponse)
async def render_index(request: Request, session: Optional[SessionData] = Depends(get_session)):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "session": session
        }
    )
