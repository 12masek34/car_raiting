from aiogram.enums.parse_mode import (
    ParseMode,
)
from aiogram.types import (
    BufferedInputFile,
    InputMediaDocument,
    InputMediaPhoto,
)
from asyncpg import (
    Record,
)

from config import (
    pictures_dir,
)


def get_pictures(file_name: str) -> BufferedInputFile:
    with open(pictures_dir / file_name, "rb") as f:
        photo_front = f.read()

    return BufferedInputFile(photo_front, file_name)


def get_summary(pics: set, docs: set, summary: Record) -> list:
    restriction = "*есть*" if summary["restriction"] else "нет"
    keys = summary["number_of_keys"]
    tire = summary["tire"]
    drive_type = summary["drive_type"]

    caption = (
        f"Принимайте лялю\!\n\nОграничения \- {restriction}\n"
        f"Ключей \- {keys}\nШины \- {tire}\n Привод \- {drive_type}\n"
    )

    files = []
    if pics:
        first = pics.pop()
    elif docs:
        first = docs.pop()
    else:
        first = None

    if first:
        first = InputMediaPhoto(media=first, caption=caption, parse_mode=ParseMode.MARKDOWN_V2)
        files.append(first)
        files.extend([InputMediaPhoto(media=pic) for pic in pics])
        files.extend([InputMediaDocument(media=doc) for doc in docs])

    if files:
        files = chunk_list(files, 9)
    else:
        files = [files]

    files.reverse()

    return files


def chunk_list(input_list: list, chunk_size: int) -> list:
    chunked_list = []
    for i in range(0, len(input_list), chunk_size):
        chunked_list.append(input_list[i:i + chunk_size])

    return chunked_list
