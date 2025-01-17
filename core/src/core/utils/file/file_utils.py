import os
import shutil
from pathlib import Path
from typing import Union

from hyperstyle.src.python.review.common.file_system import Extension

from core.utils.file.extension_utils import AnalysisExtension


def clean_file(path: str):
    if os.path.isfile(path):
        with open(path, 'r+') as f:
            f.truncate(0)


# File should contain the full path and its extension.
# Create all parents if necessary
def create_file(file_path: Union[str, Path], content: str):
    create_directory(get_parent_folder(file_path))

    with open(file_path, 'w+') as f:
        f.writelines(content)
        yield Path(file_path)


def create_directory(path: Union[str, Path], exist_ok: bool = True, clear: bool = False) -> Path:
    if os.path.exists(path) and clear:
        remove_directory(path)

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=exist_ok)
    return Path(path)


def get_parent_folder(path: Union[Path, str], to_add_slash: bool = False) -> Path:
    path = remove_slash(str(path))
    parent_folder = '/'.join(path.split('/')[:-1])
    if to_add_slash:
        parent_folder = add_slash(parent_folder)
    return Path(parent_folder)


def remove_directory(directory: Union[str, Path]) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)


def add_slash(path: str) -> str:
    if not path.endswith('/'):
        path += '/'
    return path


def remove_slash(path: str) -> str:
    return path.rstrip('/')


# For getting name of the last folder or file
# For example, returns 'folder' for both 'path/data/folder' and 'path/data/folder/'
def get_name_from_path(path: Union[Path, str], with_extension: bool = True) -> str:
    head, tail = os.path.split(path)
    # Tail can be empty if '/' is at the end of the path
    file_name = tail or os.path.basename(head)
    if not with_extension:
        file_name = os.path.splitext(file_name)[0]
    elif AnalysisExtension.get_extension_from_file(file_name) == Extension.EMPTY:
        raise ValueError('Cannot get file name with extension, because the passed path does not contain it')
    return file_name
