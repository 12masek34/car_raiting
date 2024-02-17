from aiogram.types import (
    BufferedInputFile,
)

from config import (
    pictures_dir,
)


def get_pictures(file_name: str) -> BufferedInputFile:
    with open(pictures_dir / file_name, "rb") as f:
        photo_front = f.read()

    return BufferedInputFile(photo_front, file_name)
