# Image Processor - Keyo

## Description
This repo contains:
- A simple image processor that can be used to extract an roi from an image and wrap it to a specific perspective.
    - It internally uses checksum to validate the integrity of the image.
    - For now the ROI is dynamically hardcoded (can be changed to be passed as an argument).
- Script to compare the quality of 2 images, in `compare_images.py`.

## Setup
To setup the environment, run the following command:
```
conda env create -f environment.yml
```
or
```
mamba env create -f environment.yml
```

## Usage
Place your desired images in the `images` folder.
--------
Run the server with the following command:
```
python src/server.py
```

Run the client with the following command:
```
python main.py
```

Run the comparison script with the following command:
```
python compare_images.py
```

## Structure
```
.
├── README.md
├── environment.yml
├── main.py
├── compare_images.py
├── src
│   ├── client.py
│   ├── image_processor.py
│   ├── server.py
│   └── utils
│       ├── compare_images.py
│       └── image_utils.py
├── images
│   ├── test_img.png
```

Authors: Manthan Satish, Ilir Osmanaj