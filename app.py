from flask import Flask, render_template, request, redirect, url_for, jsonify
import cv2
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not open camera", 500

    # Capture a frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Error: Could not read frame", 500

    # Save the image
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"photo_{timestamp}.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cv2.imwrite(filepath, frame)

    return jsonify({"filename": filename})

@app.route('/display/<filename>')
def display(filename):
    return render_template('display.html', filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
