from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.model.role import RoleModel


class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str

    role_id: Optional[int] = Field(default=None, foreign_key="rolemodel.id")
    # Relationship to access the RoleModel instance directly
    role: "RoleModel" = Relationship(back_populates="users")

    birthdate: date
    height: float  # in cm
    weight: float  # in kg
    