"""
This file contains different functions that will be used to generate the checksum of the image.
"""

import hashlib
import numpy as np

def get_hashlib_checksum(image: np.ndarray) -> str:
    """## Get the hashlib checksum
    ------------------------------
    This method will return the hashlib checksum of the image.

    Arguments:
    - `image`: The image to get the checksum of.

    Returns:
    - `str`: The checksum of the image.
    """
    return hashlib.md5(image).hexdigest()

def get_numpy_checksum(image: np.ndarray) -> str:
    """## Get the numpy checksum
    ------------------------------
    This method will return the numpy checksum of the image.

    Arguments:
    - `image`: The image to get the checksum of.

    Returns:
    - `str`: The checksum of the image.
    """
    return str(np.sum(image))

