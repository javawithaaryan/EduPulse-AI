from models import db
from models.quiz import QuizAttempt, Quiz
from models.performance import Performance
from models.library import Resource

class AdaptiveService:
    """Adaptive learning path engine"""
    
    # Define topic prerequisites and progression
    LEARNING_PATHS = {
        'Mathematics': [
            {'topic': 'Basic Arithmetic', 'level': 'Beginner', 'next': 'Algebra Basics'},
            {'topic': 'Algebra Basics', 'level': 'Beginner', 'prerequisite': 'Basic Arithmetic', 'next': 'Quadratic Equations'},
            {'topic': 'Quadratic Equations', 'level': 'Intermediate', 'prerequisite': 'Algebra Basics', 'next': 'Calculus Intro'},
            {'topic': 'Calculus Intro', 'level': 'Advanced', 'prerequisite': 'Quadratic Equations'},
        ],
        'Science': [
            {'topic': 'Scientific Method', 'level': 'Beginner', 'next': 'Basic Chemistry'},
            {'topic': 'Basic Chemistry', 'level': 'Beginner', 'prerequisite': 'Scientific Method', 'next': 'Advanced Chemistry'},
            {'topic': 'Advanced Chemistry', 'level': 'Intermediate', 'prerequisite': 'Basic Chemistry'},
        ],
        'Computer Science': [
            {'topic': 'Programming Basics', 'level': 'Beginner', 'next': 'Data Structures'},
            {'topic': 'Data Structures', 'level': 'Intermediate', 'prerequisite': 'Programming Basics', 'next': 'Algorithms'},
            {'topic': 'Algorithms', 'level': 'Advanced', 'prerequisite': 'Data Structures'},
        ]
    }
    
    @staticmethod
    def get_learning_path(user_id, subject='Mathematics'):
        """Generate personalized learning path for a student"""
        
        # For MVP, use performance data instead of quiz attempts
        from models.performance import Performance
        
        # Get student's performance for this subject  
        perf = Performance.query.filter_by(
            student_id=user_id,
            subject=subject
        ).first()
        
        # Mock mastery scores based on performance
        topic_mastery = {}
        if perf:
            # Use risk level to infer mastery
            if perf.risk_level == 'low':
                base_score = 8
            elif perf.risk_level == 'medium':
                base_score = 6
            else:
                base_score = 4
                
            # Assign scores to first few topics
            path = AdaptiveService.LEARNING_PATHS.get(subject, [])
            for i, node in enumerate(path[:3]):
                topic_mastery[node['topic']] = max(0, base_score - i)
        
        # Get learning path for subject
        path = AdaptiveService.LEARNING_PATHS.get(subject, [])
        
        # Determine current position and recommendations
        unlocked_topics = []
        locked_topics = []
        current_topic = None
        
        for node in path:
            topic_name = node['topic']
            mastery_score = topic_mastery.get(topic_name, 0)
            
            # Check prerequisites
            prereq = node.get('prerequisite')
            prereq_met = True
            if prereq:
                prereq_score = topic_mastery.get(prereq, 0)
                prereq_met = prereq_score >= 6  # 60% mastery required
            
            node_data = {
                'topic': topic_name,
                'level': node['level'],
                'mastery': mastery_score,
                'unlocked': prereq_met,
                'completed': mastery_score >= 8,  # 80% = mastered
                'next': node.get('next')
            }
            
            if prereq_met:
                unlocked_topics.append(node_data)
                if mastery_score < 8 and not current_topic:
                    current_topic = node_data
            else:
                locked_topics.append(node_data)
        
        # Find recommended next resource
        recommended_resource = None
        if current_topic:
            recommended_resource = Resource.query.filter_by(
                subject=subject,
                difficulty=current_topic['level']
            ).first()
        
        return {
            'subject': subject,
            'unlocked': unlocked_topics,
            'locked': locked_topics,
            'current': current_topic,
            'recommended_resource': recommended_resource,
            'overall_progress': len(unlocked_topics) / len(path) * 100 if path else 0
        }
    
    @staticmethod
    def suggest_difficulty(user_id, subject):
        """Suggest appropriate difficulty based on performance"""
        perf = Performance.query.filter_by(
            student_id=user_id,
            subject=subject
        ).first()
        
        if not perf:
            return 'Beginner'
        
        # Average score-based difficulty
        recent_attempts = QuizAttempt.query.filter_by(
            student_id=user_id
        ).order_by(QuizAttempt.submitted_at.desc()).limit(3).all()
        
        if not recent_attempts:
            return 'Beginner'
        
        avg_score = sum(a.score for a in recent_attempts) / len(recent_attempts)
        
        if avg_score < 6:
            return 'Beginner'
        elif avg_score < 8:
            return 'Intermediate'
        else:
            return 'Advanced'
