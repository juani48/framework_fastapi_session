Nutricion Web - development notes

Redis for sessions
------------------

This project uses Redis as the session store. Set the `REDIS_URL` environment variable (for example in a `.env` file) before running the app. Example:

	REDIS_URL=redis://localhost:6379/0

To run Redis locally (Linux), you can install and start it with your package manager, or use Docker:

	# using apt (Debian/Ubuntu)
	sudo apt update && sudo apt install redis-server
	sudo systemctl enable --now redis-server

	# or using docker
	docker run -p 6379:6379 -d --name redis-local redis:7-alpine

No changes to `pyproject.toml` are required if you already have `redis[async]` in the dependencies (it is included).

Usage in this project
---------------------

The Redis backend in `src/web/config.py` reads `REDIS_URL` and stores session objects under keys `session:<uuid>` as JSON.

----

`async def render_index(request: Request, session: Optional[SessionData] = Depends(get_session)) ...` -> Retorna la sesion si existe
`async def render_admin_form_users(request: Request, session: SessionData = Depends(verifier)) ...` -> verifier normalmente es un objeto o función que usa la cookie validada para recuperar los datos de la sesión desde el backend. Entonces FastAPI hace esto internamente al llegar al endpoint: (1) Ejecuta la dependencia cookie: obtiene session_id (si existe), (2) Llama al verificador (verifier) con ese session_id, (3) El verificador va al backend y busca los datos asociados, (4) Crea un objeto SessionData con la información del usuario, (5) Pasa ese objeto como argumento session a la función principal.

Pasa ese objeto como argumento session a la función principal.
`@router.get("/panel", dependencies=[Depends(cookie)] ...` -> Leer la cookie enviada por el navegador y validarla (Revisa la firma criptográfica para asegurarse de que no fue modificada) otras palabras, Depends(cookie) actúa como un filtro de autenticación. Si la cookie no es válida, el endpoint ni siquiera se ejecuta.

`async def admin_panel( request: Request, session: SessionData = Depends(require_role(["admin"]))) ...` -> Esta función recibe la sesión ya verificada (por Depends(verifier)) y revisa que el usuario tenga un rol autorizado para acceder al endpoint.