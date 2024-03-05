from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgre_pwd: str
    postgre_usr: str
    postgre_host: str
    postgre_port: str
    database_name: str
    jwt_secret_key: str
    jwt_algo: str
    jwt_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
