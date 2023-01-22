import os 

from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/shorturl")
DOMAIN_ADDRESS = os.getenv("DOMAIN_ADDRESS", "http://127.0.0.1:8000/")
LINK_NAME_LENGHT = 6
MIN_DAYS_TO_EXPIRE = 1
MAX_DAYS_TO_EXPIRE = 365
DEFAULT_DAYS_TO_EXPIRE = 90