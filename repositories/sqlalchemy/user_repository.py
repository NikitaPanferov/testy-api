from typing import Optional

from sqlalchemy import select

from models import User
from repositories.abc_repositories import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    async def create_user(
        self, email: str, name: str, hashed_password: bytes
    ) -> Optional[User]:
        async with self.db_session_factory() as session:
            async with session.begin():
                db_user = User(email=email, name=name, hashed_password=hashed_password)
                session.add(db_user)
                await session.commit()
                return db_user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.db_session_factory() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with self.db_session_factory() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()

    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(User).where(User.refresh_token == refresh_token)
            )
            return result.scalars().first()

    async def update_refresh_token(self, user_id: int, refresh_token: str) -> None:
        async with self.db_session_factory() as session:
            user = (
                (await session.execute(select(User).where(User.id == user_id)))
                .scalars()
                .first()
            )
            user.refresh_token = refresh_token
            session.add(user)
            await session.commit()
