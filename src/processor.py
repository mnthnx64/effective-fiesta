from typing import Tuple
from utils.process_helpers import ROICoords

import cv2
import numpy as np
import base64


class ImageProcessor():
    """# Image processor
    This class will handle all the processing tasks from obtaining the image to extracting the data from the image.

    Arguments:
        - `encoded_image`: The encoded image data.
        - `output_size`: The size of the output image after processing.

    ## Public Methods
    - `get_image_info()`: This method will return the image information.
    - `get_original_image()`: This method will return the original image.
    - `get_processed_image()`: This method will return the processed image.
    - `get_img_roi()`: This method will return the ROI drawn on the image.
    """

    def __init__(self, image: bytes, output_size: Tuple) -> None:
        """## Constructor
        This is the constructor of the class.
        """
        self._original_image = image
        self._output_size = output_size
        self._roi = self._get_roi()
        self._processed_image = self._process_image()
    
    
    def _get_roi(self) -> ROICoords:
        """## Gets the roi (trapezoid) from the image.

        This can be converted into internal function that calls a model to extract the trapezoid roi

        Returns:
        - `ROICoords`: The trapezoid ROI.
        """
        return ROICoords(self._original_image)


    def _process_image(self) -> np.ndarray:
        """## Process the image
        This method will process the image and extract the data from it.

        Requires:
        - `self.image`: The image to process.
        - `self.coords`: The coordinates of the trapezoid ROI.

        Returns:
        - `np.ndarray`: The processed image.
        """

        image = self._original_image.copy()
        coords = self._roi.get_coords()

        # Draw the trapezoid coordinates on the image
        for coord in coords:
            cv2.circle(image, (coord[0], coord[1]), 5, (0, 0, 255), 8)


        # Connect the dots 
        cv2.polylines(image, np.array([coords]), True, (0, 0, 255), 8)
        """
        This can be used as well
        length = len(coords)
        for i in range(length):
            cv2.line(image, (coords[i][0], coords[i][1]), (coords[(i+1)%length][0], coords[(i+1)%length][1]), (0, 0, 255), 8)
        """

        # Wrap the trapezoid to a new image
        # Calculate the affine transformation
        x, y = self._output_size
        pts1 = np.float32(coords)
        pts2 = np.float32([[0,0],[x,0],[x,y],[0,y]])

        # Wrap it into perspective
        M = cv2.getPerspectiveTransform(pts1, pts2)
        wrapped_image = cv2.warpPerspective(self._original_image.copy(), M, self._output_size)
        self._roi_on_image = image

        return wrapped_image
    
    
    def get_image_info(self) -> dict:
        """## Get the image information
        This method will return the image information.

        Returns:
        - `dict`: The image information.
        """
        return {
            'shape': self._original_image.shape,
            'dtype': str(self._original_image.dtype)
        }
    

    def get_original_image(self) -> np.ndarray:
        """## Get the original image
        This method will return the original image.

        Returns:
        - `np.ndarray`: The original image.
        """
        return self._original_image
    

    def get_processed_image(self) -> np.ndarray:
        """## Get the processed image
        This method will return the processed image.

        Returns:
        - `np.ndarray`: The processed image.
        """
        return self._processed_image
    
    def get_img_roi(self) -> np.ndarray:
        """## Get the image with the ROI drawn on it
        This method will return the image with the ROI drawn on it.

        Returns:
        - `np.ndarray`: The image with the ROI drawn on it.
        """
        return self._roi_on_image



if __name__ == '__main__':
    img = cv2.imread('images/DP.jpg')
    _, data = cv2.imencode('.jpg',img)
    encoded_img = base64.b64encode(data)
    processor = ImageProcessor(encoded_img, (200, 200))
    print(processor.get_image_info())
    cv2.imshow("Original Image with roi", processor.get_img_roi())
    cv2.imshow("Processed Image", processor.get_processed_image())
    cv2.waitKey(0)
    cv2.destroyAllWindows()