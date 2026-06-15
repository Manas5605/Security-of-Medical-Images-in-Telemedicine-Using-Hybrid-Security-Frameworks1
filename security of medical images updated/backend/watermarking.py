import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend to avoid thread issues
import matplotlib.pyplot as plt
from flask import Blueprint, request, jsonify
import os

# Define Blueprint
watermarking_blueprint = Blueprint('watermarking', __name__)

UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def apply_watermark(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    watermark = np.random.randint(0, 256, image.shape, dtype=np.uint8) // 2  # Simulated watermark
    watermarked_image = cv2.add(image, watermark)
    
    watermarked_path = os.path.join(RESULT_FOLDER, 'watermarked.png')
    cv2.imwrite(watermarked_path, watermarked_image)
    
    # Generate histogram
    plt.figure()
    plt.hist(watermarked_image.ravel(), bins=256, range=[0,256], color='black', alpha=0.7)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Watermarked Image')
    hist_path = os.path.join(RESULT_FOLDER, 'histogram.png')
    plt.savefig(hist_path)
    plt.close()
    
    return watermarked_path, hist_path

@watermarking_blueprint.route('/apply_watermark', methods=['POST'])
def process_watermarking():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)
    
    watermarked_image, histogram = apply_watermark(image_path)
    
    return jsonify({
        'success': True,
        'watermarked_image': watermarked_image,
        'histogram': histogram
    })
