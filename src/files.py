import os

import yaml


def rename(filepath: str, filename: str) -> str:
    """Renames file in filepath to filename.

    Args:
        filepath (str): original filepath
        filename (str): filename to be set

    Returns:
        str: new filepath
    """
    path = filepath.split("/")
    old_filename = path[-1]
    new_filepath = filepath.replace(old_filename, filename)
    os.rename(filepath, new_filepath)

    return new_filepath


def create_folder(folder: str):
    """Creates folder if it does not exist

    Args:
        folder (str): path to folder
    """
    if not os.path.exists(folder):
        os.makedirs(folder)


def exists(filepath: str) -> bool:
    """Checks if folder or file exists in filepath

    Args:
        filepath (str): path to file or folder

    Returns:
        bool: True if file/folder existes, False otherwise
    """
    return os.path.exists(filepath)


def save_configs(filepath: str, configs: dict):
    """Saves config dictionary to yaml file

    Args:
        filepath (str): path to resulting yaml file
        configs (dict): config parameters to be saved
    """
    with open(filepath, "w") as file:
        yaml.dump(configs, file)
