from src.client import Client

client = Client()
image_path = "images/test_img.png"
try:
    client.post_image(image_path, (200,200))
except Exception as e:
    print("Failed to connect to server")