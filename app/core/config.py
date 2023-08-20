from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков'
    description: str = (
        'Сервис для сбора пожертвований на различные проекты для котиков'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'p@$$w0rd'

    class Config:
        env_file = '.env'


settings = Settings()
