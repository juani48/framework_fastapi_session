import enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.model.user import UserModel


class RoleModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Inverse relationship to access users with this role
    users: List["UserModel"] | None = Relationship(back_populates="role")

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name
        }

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    CONFIGURATOR = "CONFIGURATOR"
    USER = "USER"
