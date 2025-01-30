from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_KEY : str = '38333295000'
    APP_SECRET: str = 'fed2163e2e8dccb53ff914ce9e2f1258'
    BASE_URL: str = 'https://app.omie.com.br/api/v1/'

    DB_HOST : str = 'vitally-feasible-mongoose.data-1.use1.tembo.io'
    DB_PORT : int = 5432
    DB_USERNAME : str = 'postgres'
    DB_PASSWORD : str = 'oc7Op8zo0c3IqfS1'
    DB_NAME : str = 'postgres'
    class Config:
        env_file='.env'
        env_file_encondig='utf-8'
        extra='ignore'

