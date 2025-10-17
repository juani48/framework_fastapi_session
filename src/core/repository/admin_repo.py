import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from core.model.user import UserModel
from core.repository.user_repo import UserRepository
from core.service.hash import hash_string, generate_password

class AdminRepository:

    @staticmethod
    async def init_admin(user_data: dict, session: AsyncSession) -> UserModel:
        try:
            if await UserRepository.get_user_by_email(user_data["email"], session):
                return  # Admin already exists

            hashed = hash_string(user_data["password"])

            new_user = UserModel(
                name=user_data["name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                role_id=user_data["role_id"],
                hashed_password=hashed
            )
            session.add(new_user)
            await session.commit()
            return new_user
        except Exception as e:
            raise ValueError("Error al crear el usuario admin.")
        
    
    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[UserModel]:
        result = await session.execute(
            select(UserModel).options(selectinload(UserModel.role))
        )
        return result.scalars().all()
    
    @staticmethod
    async def delete_user(user_id: int, user_email: str, session: AsyncSession) -> None:
        if user_id:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
        else:
            result = await session.execute(
                select(UserModel).where(UserModel.email == user_email)
            )
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("Usuario no encontrado.")
        
        await session.delete(user)
        await session.commit()
    
    @staticmethod
    async def add_user_by_admin(user_data: dict, session: AsyncSession) -> UserModel:

        user = await UserRepository.get_user_by_email(user_data.get("email"), session)
        if user:
            raise ValueError("Ya existe un usuario con ese correo electrónico.")
        
        password = generate_password(length=len(user_data.get("email")))

        hashed = hash_string(password)

        new_user = UserModel(
            name=user_data.get("name"),
            last_name=user_data.get("last_name"),
            email=user_data.get("email"),
            role_id=int(user_data.get("role")),
            hashed_password=hashed,
        )
        session.add(new_user)
        await session.commit()
        return new_user
