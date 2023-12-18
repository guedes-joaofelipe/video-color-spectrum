import os


def rename(filepath: str, filename: str) -> str:
    """ Renames file in filepath to filename.

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
    """ Creates folder if it does not exist

    Args:
        folder (str): path to folder
    """
    if not os.path.exists(folder):
        os.makedirs(folder)