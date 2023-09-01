from flask import Flask, request
from processor import ImageProcessor
from utils.process_helpers import encode_image, decode_image
from utils.checksum_gen import get_hashlib_checksum

app = Flask(__name__)

@app.route('/')
def index():
    return 'Image Processing App!'

@app.route('/process', methods=['POST'])
def process():
    print("Processing image...")
    # Get the image and size from the request
    image = request.json['image']
    size = request.json['size']
    checksum = request.json['checksum']

    # Decode the image
    try:
        decoded_img = decode_image(image)
    except Exception as e:
        return "Invalid image", 400
    decoded_img_checksum = get_hashlib_checksum(decoded_img)

    # Check if the image is valid
    if decoded_img_checksum != checksum:
        return "Invalid image", 400

    # Create the image processor
    processor = ImageProcessor(decoded_img, size)
    # Get the processed image
    processed_image = processor.get_processed_image()

    # Return the processed image
    return {
        "processed_image": encode_image(processed_image),
        "roi_image": encode_image(processor.get_img_roi()),
        "checksum": get_hashlib_checksum(processed_image)
    }

if __name__ == '__main__':
    app.run(debug=True, port=8000)