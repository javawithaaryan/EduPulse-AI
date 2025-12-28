from models import db
from models.library import Resource, LibraryRecommendation
from models.performance import Performance
from models.quiz import QuizAttempt
from models.attendance import Attendance
from datetime import datetime, timedelta

class RecommendationService:
    """AI-powered content recommendation engine"""
    
    @staticmethod
    def generate_recommendations(user_id, limit=5):
        """
        Generate personalized resource recommendations based on:
        - Student performance (weak subjects)
        - Quiz attempt history
        - Attendance patterns
        """
        recommendations = []
        
        # 1. Identify weak subjects from performance
        weak_subjects = Performance.query.filter_by(
            student_id=user_id
        ).filter(
            Performance.risk_level.in_(['medium', 'high'])
        ).all()
        
        # 2. Get quiz attempts to find struggling topics
        recent_attempts = QuizAttempt.query.filter_by(
            student_id=user_id
        ).order_by(QuizAttempt.submitted_at.desc()).limit(5).all()
        
        low_score_subjects = []
        for attempt in recent_attempts:
            if attempt.score < 7:  # Below 70%
                # Get quiz subject (assuming quiz has subject)
                from models.quiz import Quiz
                quiz = Quiz.query.get(attempt.quiz_id)
                if quiz and quiz.subject:
                    low_score_subjects.append(quiz.subject)
        
        # 3. Combine insights
        target_subjects = []
        for perf in weak_subjects:
            target_subjects.append(perf.subject)
        target_subjects.extend(low_score_subjects)
        
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
        
        if resource.subject in low_score_subjects:
            reasons.append(f"Helps improve recent {resource.subject} quiz performance")
        
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
