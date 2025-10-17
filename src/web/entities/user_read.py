import datetime

from core.model.user import UserModel


class UserRead:
    name: str
    last_name: str
    email: str
    birthdate: datetime.date
    height: float
    weight: float

    
    def __init__(self, user: UserModel):
        self.name = user.name
        self.last_name = user.last_name
        self.email = user.email
        self.birthdate = user.birthdate
        self.height = user.height
        self.weight = user.weight

    def model_dump(self) -> dict:
        return {
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "birthdate": self.birthdate.isoformat(),
            "height": self.height,
            "weight": self.weight
        }