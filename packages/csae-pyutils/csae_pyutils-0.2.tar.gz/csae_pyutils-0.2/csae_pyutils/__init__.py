import os
import json

import requests
import pandas as pd
from io import BytesIO
import owncloud


def save_json(
    data: dict, file_path: str, encoding="utf-8", ensure_ascii=False, indent=True
) -> str:
    """Save dictionary to JSON file.
    Args:
        data (dict): Dictionary to save as JSON.
        file_path (str): Path where to save the JSON file.
        encoding (str, optional): File encoding. Defaults to "utf-8".
        ensure_ascii (bool, optional): If True, guarantee ASCII output. Defaults to False.
        indent (bool, optional): If True, pretty-print JSON with indentation. Defaults to True.
    Returns:
        str: The file path.
    Example:
        >>> data = {"key": "value"}
        >>> save_json(data, "output.json")
    """
    with open(file_path, "w", encoding=encoding) as fp:
        if indent:
            json.dump(data, fp, ensure_ascii=ensure_ascii, indent=indent)
        else:
            json.dump(data, fp, ensure_ascii=ensure_ascii, indent=indent)
    return file_path


def load_json(file_path_or_url: str, encoding="utf-8") -> dict:
    """Load data from a JSON file or URL.
    This function takes a file path or URL and returns the JSON data as a Python dictionary.
    The function automatically detects if the input is a URL (starts with 'http') or a local file path.
    Args:
        file_path_or_url (str): Path to local JSON file or URL pointing to JSON data
        encoding (str, optional): Character encoding to use when reading local file. Defaults to "utf-8"
    Returns:
        dict: Parsed JSON data as a Python dictionary
    Example:
        >>> data = load_json('data.json')  # Load from local file
        >>> data = load_json('https://api.example.com/data.json')  # Load from URL
    """

    if file_path_or_url.startswith("http"):
        data = requests.get(file_path_or_url).json()
    else:
        with open(file_path_or_url, "r", encoding=encoding) as fp:
            data = json.load(fp)
    return data


def gsheet_to_df(sheet_id: str) -> pd.DataFrame:
    """Converts a Google Sheet to a pandas DataFrame.
    This function takes a Google Sheet ID and returns the sheet's content as a pandas DataFrame.
    The sheet must be publicly accessible or have appropriate sharing settings.
    Args:
        sheet_id (str): The ID of the Google Sheet. This can be found in the sheet's URL between
            /d/ and /edit.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the sheet's data.
    Raises:
        requests.exceptions.RequestException: If there's an error fetching the sheet.
        pd.errors.EmptyDataError: If the sheet is empty or contains no valid data.
    Example:
        >>> sheet_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
        >>> df = gsheet_to_df(sheet_id)
    """

    GDRIVE_BASE_URL = "https://docs.google.com/spreadsheet/ccc?key="
    url = f"{GDRIVE_BASE_URL}{sheet_id}&output=csv"
    r = requests.get(url)
    print(r.status_code)
    data = r.content
    df = pd.read_csv(BytesIO(data))
    return df


def upload_files_to_owncloud(file_list: list, user: str, pw: str, folder="pfp-data"):
    """Uploads files to OEAW ownCloud instance.
    This function uploads a list of files to a specified folder in the OEAW ownCloud instance.
    It creates the destination folder if it doesn't exist.
    Args:
        file_list (list): List of file paths to upload
        user (str): ownCloud username
        pw (str): ownCloud password
        folder (str, optional): Destination folder name in ownCloud. Defaults to "pfp-data"
    Returns:
        result: Response from the last file upload operation
    Raises:
        Various ownCloud exceptions may be raised if connection or upload fails
    Example:
        >>> files = ['/path/to/file1.txt', '/path/to/file2.pdf']
        >>> result = upload_files_to_owncloud(
        ...     file_list=files,
        ...     user='your_username',
        ...     pw='your_password',
        ...     folder='my-uploads'
        ... )
    """

    collection = folder
    oc = owncloud.Client("https://oeawcloud.oeaw.ac.at")
    oc.login(user, pw)

    try:
        oc.mkdir(collection)
    except:  # noqa: E722
        pass

    files = file_list
    for x in files:
        _, tail = os.path.split(x)
        owncloud_name = f"{collection}/{tail}"
        print(f"uploading {tail} to {owncloud_name}")
        result = oc.put_file(owncloud_name, x)

    return result
