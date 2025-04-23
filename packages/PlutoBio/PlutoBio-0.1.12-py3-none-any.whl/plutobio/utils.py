import hashlib
import base64
import uuid
import os
from . import settings
import pandas as pd
from contextlib import contextmanager
import shutil


def to_class(new_object, response, all_attr=True):
    for key, value in response.items():
        if hasattr(new_object, key) or all_attr:
            setattr(new_object, key, value)
    return new_object


def is_valid_uuid(s):
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False


def calculate_md5_base64(file_path):
    with open(file_path, "rb") as f:
        # Calculate MD5 hash of the file
        md5_hash = hashlib.md5(f.read()).digest()

        # Convert the binary hash to Base64 format
        return base64.b64encode(md5_hash).decode("utf-8")


def get_content(file_path_or_str: str) -> str:
    """
    Retrieves content either from a file or directly from the input string.

    Parameters:
    - file_path_or_str (str): A string that can either be a path to a file or the actual content.

    Returns:
    - str: If file_path_or_str is a file path, returns the content of the file.
           Otherwise, returns file_path_or_str itself.
    """
    if os.path.isfile(file_path_or_str):
        with open(file_path_or_str, "r") as file:
            methods = file.read()
    else:
        methods = file_path_or_str

    return methods


@contextmanager
def dataframe_to_csv(dataframe, file_path):
    temp_file_path = os.path.join(settings.DEFAULT_TMP_PATH, file_path)

    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

    if isinstance(dataframe, pd.DataFrame):
        dataframe.to_csv(temp_file_path, index=False)
        yield temp_file_path
    else:
        shutil.copy(dataframe, temp_file_path)
        yield temp_file_path

    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
