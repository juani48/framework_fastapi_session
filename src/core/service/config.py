from os import getenv
from core.service.session_data import SessionData
from dotenv import load_dotenv
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException
import redis.asyncio as redis
from uuid import UUID
from typing import Optional
import json


load_dotenv()

# Configurar Redis
redis_url = getenv("REDIS_URL")
redis_client: redis.Redis = redis.from_url(redis_url)


class RedisBackend:
    def __init__(self, client: redis.Redis, prefix: str = "session:") -> None:
        self.client = client
        self.prefix = prefix

    async def create(self, session_id: UUID, data: SessionData) -> None:
        key = f"{self.prefix}{session_id}"
        # pydantic BaseModel -> dict -> json
        await self.client.set(key, json.dumps(data.model_dump()), ex=None)

    async def read(self, session_id: UUID) -> Optional[SessionData]:
        key = f"{self.prefix}{session_id}"
        raw = await self.client.get(key)
        if raw is None:
            return None
        try:
            payload = json.loads(raw)
            return SessionData(**payload)
        except Exception:
            return None

    async def delete(self, session_id: UUID) -> None:
        key = f"{self.prefix}{session_id}"
        await self.client.delete(key)


# Crear backend Redis
backend = RedisBackend(redis_client)

# Configuración de la cookie
cookie_params = CookieParameters(
    httponly=True,
    secure=True,  
    samesite="lax"
    )

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=getenv("API_KEY"),
    cookie_params=cookie_params,
)
class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: RedisBackend,
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True

verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)