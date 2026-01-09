from flask import request, jsonify
from . import vision_bp
from services.vision_service import VisionService

vision_service = VisionService()

@vision_bp.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read file as bytes
        image_data = file.read()
        
        # Analyze using service
        result = vision_service.analyze_image(image_data)
        
        if "error" in result:
            return jsonify(result), 500
            
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500
