import logging
import os
from pathlib import (
    Path,
)

from dotenv import (
    load_dotenv,
)


load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

pictures_dir = Path("static","pictures")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
HOST = os.getenv("POSTGRES_HOST")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
GROUP_ID = os.getenv("GROUP_ID")
