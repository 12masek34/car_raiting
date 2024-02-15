import logging
import os

from dotenv import (
    load_dotenv,
)


load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
HOST = os.getenv("POSTGRES_HOST")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
