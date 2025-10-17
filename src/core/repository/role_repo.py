from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core.model.role import RoleEnum, RoleModel

class RoleRepository:
    @staticmethod
    async def create_role(role_data: dict, session: AsyncSession) -> RoleModel:
        new_role = RoleModel(
            name=role_data["name"]
        )
        session.add(new_role)
        await session.commit()
        return new_role

    @staticmethod
    async def get_role_by_name(name: str, session: AsyncSession) -> RoleModel | None:
        result = await session.execute(select(RoleModel).where(RoleModel.name == name))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_roles(session: AsyncSession) -> list[RoleModel]:
        result = await session.execute(select(RoleModel).where(RoleModel.name != "ADMIN"))
        return result.scalars().all()

    @staticmethod
    async def init_roles(session: AsyncSession):
        if await RoleRepository.get_all_roles(session):
            return  # Roles already initialized
        roles = RoleEnum.__members__.keys()
        for role_name in roles:
            await RoleRepository.create_role({"name": role_name}, session)