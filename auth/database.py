from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer, Column, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from models.models import roles

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id =Column('id', Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    username = Column('username', String, nullable=False)
    registered_at = Column('registered_at', TIMESTAMP, default=datetime.utcnow)
    role_id = Column('role_id', Integer, ForeignKey(roles.c.id))
    hashed_password: str = Column(
        String(length=1024), nullable=False
    )
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(
        Boolean, default=False, nullable=False
    )
    is_verified: bool = Column(
        Boolean, default=False, nullable=False
    )

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)