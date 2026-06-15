import cv2
import numpy as np
import torch
from flask import Blueprint, request, jsonify
import os
from torchvision import transforms
from models.steganographymodel import Autoencoder
import matplotlib.pyplot as plt

steganography_blueprint = Blueprint('stego', __name__)

UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Autoencoder().to(device)
model.load_state_dict(torch.load("models/steganographymodel.pth", map_location=device))
model.eval()

# Image transformation
transform = transforms.Compose([transforms.ToTensor()])

def apply_steganography(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (128, 128))
    tensor_image = transform(image).unsqueeze(0).to(device)

    # Pass through autoencoder
    with torch.no_grad():
        stego_image = model(tensor_image).cpu().squeeze().numpy()

    # Save stego image
    stego_image_path = os.path.join(RESULT_FOLDER, 'stego.png')
    cv2.imwrite(stego_image_path, (stego_image * 255).astype(np.uint8))

    # Generate histogram
    plt.figure()
    plt.hist(stego_image.ravel(), bins=256, range=[0, 256], color='black', alpha=0.7)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Stego Image')
    stego_histogram_path = os.path.join(RESULT_FOLDER, 'stego_histogram.png')
    plt.savefig(stego_histogram_path)
    plt.close()

    return stego_image_path, stego_histogram_path

@steganography_blueprint.route('/apply_stego', methods=['POST'])
def process_steganography():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    stego_image, stego_histogram = apply_steganography(image_path)

    return jsonify({
        'success': True,
        'stego_image': stego_image,
        'stego_histogram': stego_histogram
    })