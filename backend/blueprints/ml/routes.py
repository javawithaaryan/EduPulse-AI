from flask import request, jsonify
from . import ml_bp
from services.ml_service import MLService

@ml_bp.route('/health', methods=['GET'])
def check_connection():
    """
    Checks connection to Azure ML Workspace.
    """
    result = MLService.verify_connection()
    status_code = 200 if result.get("status") == "Connected" else 500
    return jsonify(result), status_code

@ml_bp.route('/predict', methods=['POST'])
def predict_risk():
    """
    Predicts student risk.
    Payload: { "student_id": "123", "recent_scores": [8, 9, 7], "attendance_rate": 95 }
    """
    try:
        data = request.get_json() or {}
        student_id = data.get("student_id", "unknown")
        recent_scores = data.get("recent_scores", [])
        attendance_rate = data.get("attendance_rate", 100)

        result = MLService.predict_risk(student_id, recent_scores, attendance_rate)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
