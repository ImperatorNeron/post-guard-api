from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class DatabaseBaseSettings(BaseModel):
    driver: str
    user: str
    password: str
    host: str
    port: str
    db_name: str
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self):
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class DatabaseSettings(DatabaseBaseSettings):
    pass


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certificates" / "private.pem"
    public_key_path: Path = BASE_DIR / "certificates" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    api_version_prefix: str = "/api/v1"
    database: DatabaseSettings
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
