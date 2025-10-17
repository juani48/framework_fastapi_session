from pydantic import BaseModel

from core.model.role import RoleEnum

class SessionData(BaseModel):
    name: str
    email: str
    role: str