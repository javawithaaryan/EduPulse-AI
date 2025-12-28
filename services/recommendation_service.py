from models import db
from models.library import Resource, LibraryRecommendation
from models.performance import Performance
from models.attendance import Attendance
from datetime import datetime, timedelta

class RecommendationService:
    """AI-powered content recommendation engine"""
    
    @staticmethod
    def generate_recommendations(user_id, limit=5):
        """
        Generate personalized resource recommendations based on:
        - Student performance (weak subjects)
        - Attendance patterns
        """
        recommendations = []
        
        # 1. Identify weak subjects from performance
        weak_subjects = Performance.query.filter_by(
            student_id=user_id
        ).filter(
            Performance.risk_level.in_(['medium', 'high'])
        ).all()
        
        # 2. Combine insights
        target_subjects = []
        for perf in weak_subjects:
            target_subjects.append(perf.subject)
        
        # Remove duplicates
        target_subjects = list(set(target_subjects))
        
        # 4. Find resources matching these subjects
        if target_subjects:
            resources = Resource.query.filter(
                Resource.subject.in_(target_subjects)
            ).order_by(Resource.created_at.desc()).limit(limit).all()
        else:
            # Fallback: recommend recent resources
            resources = Resource.query.order_by(
                Resource.created_at.desc()
            ).limit(limit).all()
        
        # 5. Generate AI reasoning for each recommendation
        for resource in resources:
            reason = RecommendationService._generate_reason(
                resource, weak_subjects, low_score_subjects
            )
            
            recommendations.append({
                'resource': resource,
                'reason': reason,
                'confidence': 0.85 if target_subjects else 0.5
            })
        
        return recommendations
    
    @staticmethod
    def _generate_reason(resource, weak_subjects, low_score_subjects):
        """Generate AI-style reasoning for recommendation"""
        reasons = []
        
        # Check if resource subject matches weakness
        for perf in weak_subjects:
            if perf.subject == resource.subject:
                reasons.append(f"Addresses your {resource.subject} learning gap")
        
        # Difficulty matching
        if resource.difficulty == 'Beginner':
            reasons.append("Good starting point for foundational concepts")
        elif resource.difficulty == 'Intermediate':
            reasons.append("Builds on your existing knowledge")
        
        if not reasons:
            reasons.append("Recommended based on your learning profile")
        
        return " • ".join(reasons[:2])  # Max 2 reasons
    
    @staticmethod
    def save_recommendation(user_id, resource_id, reason, confidence):
        """Save recommendation to database for analytics"""
        rec = LibraryRecommendation(
            user_id=user_id,
            resource_id=resource_id,
            reason=reason,
            confidence=confidence
        )
        db.session.add(rec)
        db.session.commit()
