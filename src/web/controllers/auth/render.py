from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="src/web/templates")

@router.get("/registrarse", response_class=Jinja2Templates)
async def render_signin(request: Request):
    return templates.TemplateResponse("user/signin.html", {"request": request})

@router.get("/iniciar-sesion", response_class=Jinja2Templates)
async def render_login(request: Request):
    return templates.TemplateResponse("user/login.html", {"request": request})