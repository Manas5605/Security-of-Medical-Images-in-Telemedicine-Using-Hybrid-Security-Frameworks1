from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from watermarking import watermarking_blueprint
from stego import steganography_blueprint
from encryption import encrypt_image
import hashlib
import time
import os
import shutil

app = Flask(__name__)
app.secret_key = "c99d740b7bc045af2c5bb93f79edc8d1"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['STORED_FOLDER'] = 'static/stored'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STORED_FOLDER'], exist_ok=True)

users = {}
app.register_blueprint(watermarking_blueprint, url_prefix='/watermarking')
app.register_blueprint(steganography_blueprint, url_prefix='/steganography')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username in users:
            return jsonify({"success": False, "message": "Username already exists"}), 400
        users[username] = generate_password_hash(password)
        return jsonify({"success": True, "message": "Signup successful!"})
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username not in users or not check_password_hash(users[username], password):
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
        session['user'] = username
        return jsonify({"success": True})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return jsonify({"message": "Upload successful", "file_path": file_path})

@app.route('/watermarking')
def watermarking():
    return render_template('watermarking.html')

@app.route('/stego')
def stego():
    return render_template('stego.html', watermarked_image='/static/results/watermarked.png')

@app.route('/encryption')
def encryption():
    return render_template('encryption.html', stego_image='/static/results/stego.png')

@app.route('/encryption/apply_encryption', methods=['POST'])
def apply_encryption_route():
    encrypted_image_path, encrypted_histogram_path, dna_encoded = encrypt_image('static/results/stego.png')
    return jsonify({
        "encrypted_image": encrypted_image_path,
        "encrypted_histogram": encrypted_histogram_path,
        "dna_encoded": dna_encoded
    })

@app.route('/blockchain/store', methods=['POST'])
def store_in_blockchain():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    image_path = 'static/results/encrypted.png'
    if not os.path.exists(image_path):
        return jsonify({"success": False, "message": "Image not found"}), 404
    timestamp = str(int(time.time()))
    new_filename = f"encrypted_{timestamp}.png"
    stored_path = os.path.join(app.config['STORED_FOLDER'], new_filename)
    shutil.copy(image_path, stored_path)
    tx_hash = hashlib.sha256((timestamp + new_filename).encode()).hexdigest()
    return jsonify({
        "success": True,
        "transaction_hash": tx_hash,
        "stored_image_url": f"/static/stored/{new_filename}"
    })

@app.route('/blockchain')
def blockchain_page():
    return render_template('blockchain.html')

@app.route('/blockchain/stored_images')
def get_stored_images():
    images = os.listdir(app.config['STORED_FOLDER'])
    images = [url_for('static', filename=f'stored/{img}') for img in images]
    return jsonify(images)

@app.route('/watermarking/back')
def back_to_watermarking():
    return redirect(url_for('watermarking'))

if __name__ == '__main__':
    app.run(debug=True)
