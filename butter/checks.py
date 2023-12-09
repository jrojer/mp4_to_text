from pathlib import Path
import os


def is_non_empty_dir(path):
    return is_dir(path) and len(os.listdir(path)) > 0


def is_file(path):
    return Path(path).is_file()


def is_dir(path):
    return Path(path).is_dir()


def dir_for_file_exists(path):
    return is_dir(Path(path).parent)


def check_that(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)
