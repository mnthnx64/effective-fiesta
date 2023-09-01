import numpy as np
import cv2
import base64

class ROICoords():
    """# ROI Coordinates Class
    -----------------------------
    This is an abstract class that will be used to define the ROI trapezoid coordinates.

    Methods:
    - `get_coords()`: This method will return the coordinates of the trapezoid.
    """

    def __init__(self, image: np.ndarray) -> None:
        """## Constructor
        ----------------
        This is the constructor of the class.

        Arguments:
        - `image`: The image to extract the coordinates from.
        """
        # Genrate the coordinates of the trapezoid (cyclic order) 
        #! Can be changed to a more general approach
        shape = image.shape
        self._coords = np.array([
            [shape[1] * 0.25, shape[0] * 0.5],
            [shape[1] * 0.75, shape[0] * 0.5],
            [shape[1], shape[0]],
            [1, shape[0]]
        ], dtype=np.int32)


    def get_coords(self) -> np.ndarray:
        """## Get the coordinates
        ------------------------
        This method will return the coordinates of the trapezoid.

        Returns:
        - `np.ndarray`: The coordinates of the trapezoid.
        """
        return self._coords
    

def encode_image(image: np.ndarray) -> bytes:
    """## Encode the image
    ---------------------
    This method will encode the image to bytes.

    Arguments:
    - `image`: The image to encode.

    Returns:
    - `bytes`: The encoded image.
    """
    _, encoded_image = cv2.imencode('.png', image)
    return base64.b64encode(encoded_image).decode('utf-8')


def decode_image(encoded_image: bytes) -> np.ndarray:
    """## Decode the image
    ---------------------
    This method will decode the image from bytes.

    Arguments:
    - `encoded_image`: The image to decode.

    Returns:
    - `np.ndarray`: The decoded image.
    """
    nparr = np.frombuffer(base64.b64decode(encoded_image), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        

if __name__ == '__main__':
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    coords = ROICoords(img)
    print(coords.get_coords())