from config import Config
import random

class MLService:
    @staticmethod
    def predict_risk(student_id, recent_scores, attendance_rate=100):
        """
        Predicts student performance risk.
        input: list of recent scores, attendance_rate (0-100)
        output: dict {risk_level, confidence, trend}
        """
        if Config.USE_MOCK_AI:
            avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0
            count = len(recent_scores)
            
            # Base risk from grades
            risk_level = "low"
            if avg < 5: risk_level = "high"
            elif avg < 7.5: risk_level = "medium"
            
            # Attendance Factor: Chronic absenteeism (below 75%) triggers 'high' or 'medium'
            if attendance_rate < 75:
                # Upgrading risk if attendance is low
                if risk_level == "low": risk_level = "medium"
                elif risk_level == "medium": risk_level = "high"
            
            # Simple trend analysis
            is_declining = False
            if count >= 2:
                is_declining = recent_scores[-1] < recent_scores[-2]
            
            confidence = 0.85 + (random.random() * 0.1)
            trend = "stable"
            if is_declining: trend = "declining"
            elif count >= 2 and recent_scores[-1] > recent_scores[-2]: trend = "improving"
            
            return {
                "risk_level": risk_level, 
                "confidence": round(confidence, 2), 
                "trend": trend,
                "attendance_impact": "low" if attendance_rate > 90 else "critical"
            }
        
        return {"risk_level": "low", "confidence": 0.9, "trend": "stable"}

