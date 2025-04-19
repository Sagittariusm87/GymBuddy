
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from waitress import serve  # Import waitress for serving the app
from pushup_web_module import analyze_frame  # Use the real-time pushup analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['frame']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    result = analyze_frame(img)
    return jsonify(result)

if __name__ == '__main__':
    # Replace app.run() with waitress.serve()
    serve(app, host='0.0.0.0', port=8080)
