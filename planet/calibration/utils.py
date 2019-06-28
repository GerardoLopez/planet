
import os.path as osp

def file_exists(filename: str):
    """
    Private method to check if a file exist in the local filesystem.

    Parameters
    ----------
    filename: str
        The full path of a filename

    Returns
    -------
    True: Boolean
        If the file exists in the local file system
    False: Boolean
        If the file does not exist in the local file system
    """
    if osp.exists(filename) is True:
        return True
    else:
        return False
