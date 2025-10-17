from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from core.model.role import RoleEnum
from core.model.user import UserModel
from core.service.hash import hash_string, verify_string

class UserRepository:

    @staticmethod
    async def create_user(user_data: dict, session: AsyncSession) -> UserModel:
        if await UserRepository.get_user_by_email(user_data["email"], session):
            raise ValueError("Ya existe un usuario con ese correo electrónico.")

        hashed = hash_string(user_data["password"])
        print("---------USER----------\nUser data to create:", user_data, "\n-------------------")
        new_user = UserModel(
            name=user_data.get("name"), 
            last_name=user_data.get("last_name"), 
            email=user_data.get("email"), 
            birthdate=user_data.get("birthdate"),
            height=user_data.get("height"),
            weight=user_data.get("weight"),
            role_id=RoleEnum.USER.value,
            hashed_password=hashed
        )
        session.add(new_user)
        await session.commit()
        return new_user

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> UserModel | None:
        result = await session.execute(
            select(UserModel).options(selectinload(UserModel.role)).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def login_user(email: str, password: str, session: AsyncSession) -> UserModel:
        try:
            result = await session.execute(
                select(UserModel).options(selectinload(UserModel.role)).where(UserModel.email == email)
            )
            user = result.scalar_one_or_none()
            if not user or not verify_string(password, user.hashed_password):
                raise ValueError("Credenciales inválidas.")
            return user
        except Exception as e:
            raise ValueError("Credenciales inválidas.")

    