from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

def analyze_image(img):
    # Example: return image size as dummy result
    h, w, _ = img.shape
    return {"status": "success", "height": h, "width": w}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['frame']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    result = analyze_image(img)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
