import logging

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    mongo_user: str = Field(alias="MONGO_USER", default="admin")
    mongo_password: str = Field(alias="MONGO_PASSWORD", default="password123")
    mongo_host: str = Field(alias="MONGO_HOST", default="localhost")
    mongo_port: int = Field(alias="MONGO_PORT", default=27017)
    mongo_db_name: str = Field(alias="DB_NAME", default="sampleDB")

    bot_token: str = Field(alias="BOT_TOKEN", default="7257132856:AAEP_EPKxmonCpMgkVEjUlggMJkc1alMSDI")


settings = Settings()

console = logging.StreamHandler()
filename = logging.FileHandler("logs/get_data.log")

logging.basicConfig(
    handlers=(console, filename),
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
