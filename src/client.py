from typing import Tuple
from src.utils.checksum_gen import get_numpy_checksum, get_hashlib_checksum
from src.utils.process_helpers import encode_image, decode_image

import cv2
import numpy as np
import requests
import base64
import sys
sys.path.append('..')

class Client():
    """# Client
    Client class for the image processing service

    Methods:
    - `post_image()`: This method will post the image to the server and retrive the data sent by the server.
    """

    def __init__(self,):
        """## Constructor
        This is the constructor of the class.
        """
        self._url = 'http://localhost:8000/process'
        self._headers = {'Content-Type': 'application/json'}
        self._image = None
        self._size = None
        self._checksum = None


    def post_image(self, image_path: str, size: Tuple) -> np.ndarray:
        """## Post the image
        This method will post the image to the server and retrive the data sent by the server.

        Arguments:
        - `image_path`: The path image to process.
        - `size`: The size of the output image.

        Returns:
        - `np.ndarray`: The processed image.
        """
        self._image = cv2.imread(image_path)
        self._size = size
        self._checksum = self._get_checksum(self._image)


        # Create the request body
        body = {
            'image': encode_image(self._image),
            'size': size,
            'checksum': self._checksum
        }

        # Send the request
        response = requests.post(self._url, json=body, headers=self._headers)
        response = response.json()

        image = decode_image(response['processed_image'])
        decode_image_checksum = get_hashlib_checksum(image)

        # Check if the image is valid
        if decode_image_checksum != response['checksum']:
            raise Exception("Invalid image")

        roi_image = decode_image(response['roi_image'])
        
        cv2.imshow("Processed Image", image)   
        cv2.imshow("Original Image", self._image) 
        cv2.imshow("ROI Image", roi_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        

    def _get_checksum(self, image: np.ndarray) -> str:
        """## Get the checksum
        This method will return the checksum of the image.

        Arguments:
        - `image`: The image to get the checksum from.

        Returns:
        - `str`: The checksum of the image.
        """
        return get_hashlib_checksum(image)
