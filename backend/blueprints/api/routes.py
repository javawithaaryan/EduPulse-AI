from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

api_bp = Blueprint('api', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({
            "message": "File received successfully",
            "filename": filename
        }), 200

@api_bp.route('/analyze', methods=['POST'])
def analyze_data():
    data = request.json
    # Simulate AI processing
    return jsonify({
        "summary": "This is a simulated AI summary of the uploaded content.",
        "score": 85,
        "recommendations": ["Review chapter 3", "Practice more calculus problems"]
    }), 200
