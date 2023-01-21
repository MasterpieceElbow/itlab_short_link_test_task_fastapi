import os 

from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
DOMAIN_ADDRESS = "https://97y3sv.deta.dev/"
LINK_NAME_LENGHT = 6
MIN_DAYS_TO_EXPIRE = 1
MAX_DAYS_TO_EXPIRE = 365
DEFAULT_DAYS_TO_EXPIRE = 90