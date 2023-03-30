from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "Благотворительный фонд поддержки котов"
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = "secret"
    first_superuser_email: Optional[EmailStr] = "alibek@gmail.com"
    first_superuser_password: Optional[str] = "12345678aA"

    class Config:
        env_file = ".env"


settings = Settings()
