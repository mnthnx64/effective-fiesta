"""
A simple script to use the client to talk to the server
"""

from src.client import Client

# Initialize the client
client = Client()

# Give the image path and the size of the image here
image_path = "images/test_img.png"
ouput_size = (200, 200)

# Send the image to the server
try:
    client.post_image(image_path, ouput_size)
except Exception as e:
    # If the server is not running or in case of any other exception, this will be printed
    print("Failed to connect to server")