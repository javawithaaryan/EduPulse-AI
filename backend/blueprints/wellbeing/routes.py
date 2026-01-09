from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.wellbeing import EmotionalCheckin, SupportLog
from datetime import datetime, timedelta

wellbeing_bp = Blueprint('wellbeing', __name__, template_folder='templates')

@wellbeing_bp.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    # Check if already checked in today
    today = datetime.utcnow().date()
    existing = EmotionalCheckin.query.filter_by(
        user_id=current_user.id
    ).filter(
        db.func.date(EmotionalCheckin.date) == today
    ).first()
    
    if request.method == 'POST':
        mood = int(request.form.get('mood'))
        stress = int(request.form.get('stress'))
        notes = request.form.get('notes', '')
        
        if existing:
            # Update existing
            existing.mood_level = mood
            existing.stress_level = stress
            existing.notes = notes
        else:
            # Create new
            checkin = EmotionalCheckin(
                user_id=current_user.id,
                mood_level=mood,
                stress_level=stress,
                notes=notes,
                date=today
            )
            db.session.add(checkin)
        
        db.session.commit()
        
        # Generate AI support response
        ai_response = generate_support_message(mood, stress, notes)
        
        # Log the support interaction
        log = SupportLog(
            user_id=current_user.id,
            trigger_type=f"mood_{mood}_stress_{stress}",
            ai_response=ai_response
        )
        db.session.add(log)
        db.session.commit()
        
        flash(ai_response, 'info')
        return redirect(url_for('wellbeing.insights'))
    
    return render_template('wellbeing/checkin.html', existing=existing)

@wellbeing_bp.route('/insights')
@login_required
def insights():
    # Get last 7 days of check-ins
    week_ago = datetime.utcnow() - timedelta(days=7)
    checkins = EmotionalCheckin.query.filter_by(
        user_id=current_user.id
    ).filter(
        EmotionalCheckin.created_at >= week_ago
    ).order_by(EmotionalCheckin.date).all()
    
    # Calculate trends
    if checkins:
        avg_mood = sum(c.mood_level for c in checkins) / len(checkins)
        avg_stress = sum(c.stress_level for c in checkins) / len(checkins)
    else:
        avg_mood = 0
        avg_stress = 0
    
    return render_template('wellbeing/insights.html',
                         checkins=checkins,
                         avg_mood=round(avg_mood, 1),
                         avg_stress=round(avg_stress, 1))

def generate_support_message(mood, stress, notes):
    """Generate supportive (non-clinical) AI response"""
    
    # Low mood responses
    if mood <= 2:
        messages = [
            "I notice you're feeling a bit down. Remember, it's okay to have tough days. Take a short break and try something you enjoy! 🌟",
            "Thank you for sharing how you're feeling. Small wins matter - celebrate completing even one task today! 💙"
        ]
    # High stress responses
    elif stress >= 4:
        messages = [
            "Feeling stressed? Try breaking big tasks into smaller steps. You've got this! Take it one step at a time. 🎯",
            "High stress detected. Remember to breathe! Maybe take a 5-minute walk or listen to calming music. 🌿"
        ]
    # Neutral/positive
    elif mood >= 4:
        messages = [
            "Great to see you're feeling good! Keep up the momentum - you're doing amazing! ⭐",
            "Love the positive energy! Stay consistent with your study habits. 🚀"
        ]
    else:
        messages = [
            "Thanks for checking in! Consistency is key. Keep showing up for yourself! 💪",
            "Every day is progress. Stay focused on your goals! 🎓"
        ]
    
    import random
    return random.choice(messages)
