import datetime
import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from core.model.role import RoleEnum
from core.repository.admin_repo import AdminRepository
from core.repository.role_repo import RoleRepository
from core.repository.user_repo import UserRepository

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    # Optionally, you can add initial data population here
    async with async_session() as session:
        await RoleRepository.init_roles(session)
        # Ensure we use the numeric role id (foreign key expects int), not the enum string value
        admin_role = await RoleRepository.get_role_by_name(RoleEnum.ADMIN.value, session)
        if not admin_role:
            raise RuntimeError("Admin role was not created or could not be found")

        user_data = {
            "name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "birthdate": datetime.date(1990, 1, 1),
            "height": 180,
            "weight": 75,
            "role_id": admin_role.id,
            "password": "admin123"
        }
        await AdminRepository.init_admin(user_data, session)