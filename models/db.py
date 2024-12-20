from typing_extensions import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from configs.config import Settings


class DatabaseHelper:
    def __init__(self, url: Optional[str] = None, echo: Optional[bool] = None) -> None:
        settings = Settings()

        if not url:
            url = settings.db.url

        if not echo:
            echo = settings.db.echo

        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )


db = DatabaseHelper()
