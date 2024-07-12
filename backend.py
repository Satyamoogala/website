# Backend (Flask)
from flask import Flask, requests, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Receive the video feed from the frontend
    video_feed = requests.get_json()['video_feed']

    # Detect the face and extract the skin region
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(video_feed, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        skin_region = video_feed[y:y+h, x:x+w]
        skin_region = cv2.cvtColor(skin_region, cv2.COLOR_BGR2HSV)

    # Analyze the skin color and recommend foundation and makeup products
    avg_skin_color_hsv = np.mean(skin_region, axis=(0, 1))
    foundation_shade = "Unknown"
    lipstick_shade = "Unknown"
    min_diff = float('inf')
    for shade, hsv_value in foundation_shade.items():
        diff = np.linalg.norm(np.array(hsv_value) - avg_skin_color_hsv)
        if diff < min_diff:
            min_diff = diff
            foundation_shade = shade
    min_diff = float('inf')
    for shade, hsv_value in lipstick_shade.items():
        diff = np.linalg.norm(np.array(hsv_value) - avg_skin_color_hsv)
        if diff < min_diff:
            min_diff = diff
            lipstick_shade = shade

    # Return the recommended products to the frontend
    return jsonify({'foundation_shade': foundation_shade, 'lipstick_shade': lipstick_shade})

if __name__ == '__main__':
    app.run(debug=True)