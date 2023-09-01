"""
Script to compare the quality of two images.
It uses:
1. Sharpness (calculated using Laplacian)
2. SNR (calculated using MSE)
"""

import base64
import cv2
from math import log10, sqrt
import numpy as np

# Read the images
img1 = cv2.imread("images/test_img.png")
img2 = cv2.GaussianBlur(img1, (5, 5), 0)

# Define sharpness function
def measure_sharpness(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpness = np.mean(np.abs(laplacian))
    return sharpness

# Convert images to grayscale    
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Denoise if necessary
# gray1 = cv2.fastNlMeansDenoising(gray1)
# gray2 = cv2.fastNlMeansDenoising(gray2)

# Compute sharpness score
sharpness1 = measure_sharpness(gray1)
sharpness2 = measure_sharpness(gray2)

# Compare sharpness scores
print("Sharpness1: ", sharpness1)
print("Sharpness2: ", sharpness2)
print("Sharpness1 > Sharpness2: ", sharpness1 > sharpness2)

# Compute SNR 
def compute_snr(image):
    mse = np.mean((image) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

# Compute SNR scores
snr1 = compute_snr(gray1)
snr2 = compute_snr(gray2)
print("SNR1: ", snr1)
print("SNR2: ", snr2)
print("SNR1 > SNR2: ", snr1 > snr2)

"""
Output:
Sharpness1:  9.204294250081317
Sharpness2:  3.5850981537334548
Sharpness1 > Sharpness2:  True
SNR1:  27.700641672207244
SNR2:  27.68754713162341
SNR1 > SNR2:  True
"""