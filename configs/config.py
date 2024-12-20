from misc.singleton import singleton
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSettings):
    url: str = "postgresql+asyncpg://postgres:changeme@localhost:5432/"
    echo: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "DB_"
        extra = "ignore"


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        env_prefix = "JWT_"
        extra = "ignore"


@singleton
class Settings(BaseModel):
    jwt: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()
