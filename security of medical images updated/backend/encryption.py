import numpy as np
import cv2
import os
from key_generation import generate_keys
import matplotlib.pyplot as plt

# DNA Encoding Rules
DNA_RULES = {
    "00": "A", "01": "T", "10": "C", "11": "G",
    "A": "00", "T": "01", "C": "10", "G": "11"
}

def binary_to_dna(binary_data):
    """Convert binary string to DNA sequence"""
    return "".join(DNA_RULES[binary_data[i:i+2]] for i in range(0, len(binary_data), 2))

def encrypt_image(image_path):
    """Encrypt image using hybrid chaotic encryption + DNA encoding"""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    image = cv2.resize(image, (128, 128))
    logistic_keys, henon_keys, lorenz_keys = generate_keys(image.shape)
    hybrid_keys = logistic_keys ^ henon_keys ^ lorenz_keys
    
    encrypted_image = (image.astype(np.uint16) + hybrid_keys.astype(np.uint16)) % 256
    encrypted_image = encrypted_image.astype(np.uint8)
    
    binary_image = ''.join(format(pixel, '08b') for pixel in encrypted_image.flatten())
    dna_encoded = binary_to_dna(binary_image)
    
    encrypted_image_path = os.path.join('static/results/', 'encrypted.png')
    cv2.imwrite(encrypted_image_path, encrypted_image)
    
    plt.figure()
    plt.hist(encrypted_image.ravel(), bins=256, range=[0, 256], color='black', alpha=0.7)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Encrypted Image')
    encrypted_histogram_path = os.path.join('static/results/', 'encrypted_histogram.png')
    plt.savefig(encrypted_histogram_path)
    plt.close()
    
    return encrypted_image_path, encrypted_histogram_path, dna_encoded

