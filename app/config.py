from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool = True
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = {"env_file": ".env"}

settings = Settings()