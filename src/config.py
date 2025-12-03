from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str = ""
    white_list_users: list[int] = []
    update_interval: int = 10

    postgres_host: str = ""
    postgres_port: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
