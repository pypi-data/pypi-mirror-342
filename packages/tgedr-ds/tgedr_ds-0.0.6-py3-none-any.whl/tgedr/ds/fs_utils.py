"""
Module Name: 
Description: code utils to handle file system operations
Author:
Date:
Version:

Dependencies:
- ...

Environment Variables:
- ...

Usage:
    >>> from tgedr.ds.pytorch.utils import get_device
    >>> DEVICE = get_device()
    >>> print(DEVICE.type)
    mps

"""


# pylint: disable=consider-using-with
def read_text_file(filename):
    """reads text file content

    Args:
        filename (str): the file to read
        encoding (str): the text encoding
    Returns:
        torch.device: device

    Raises:
        ...

    """
    file = open(filename, "r", encoding="utf-8")
    return file.read()
