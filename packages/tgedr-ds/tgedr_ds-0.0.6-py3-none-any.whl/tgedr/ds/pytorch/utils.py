"""
Module Name: 
Description: code utils for use in data science context
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
import torch

DEVICE_CPU = torch.device("cpu")
DEVICE_MPS = torch.device("mps")


def get_device():
    """gets current processing device, tries to get GPU/MPS first

    Args:
        arg (type): description

    Returns:
        torch.device: device

    Raises:
        ...

    """
    if torch.backends.mps.is_available():
        print(f"[get_device] mps device count: {torch.mps.device_count()}")
        result = DEVICE_MPS
    else:
        print("[get_device] MPS device not found!")
        result = DEVICE_CPU
    return result
