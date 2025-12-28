from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.library import Resource, LearningProgress, LibraryRecommendation
from services.openai_service import OpenAIService

library_bp = Blueprint('library', __name__, template_folder='templates')

@library_bp.route('/hub')
@login_required
def hub():
    # Fetch recommended resources (mocked or from DB)
    recommendations = Resource.query.limit(3).all() 
    recent = Resource.query.order_by(Resource.created_at.desc()).limit(5).all()
    
    return render_template('library/hub.html', 
                         recommendations=recommendations, 
                         recent=recent)

@library_bp.route('/resource/<int:id>')
@login_required
def view_resource(id):
    resource = Resource.query.get_or_404(id)
    # Track usage (simplistic)
    prog = LearningProgress(user_id=current_user.id, resource_id=id, status='viewed')
    db.session.add(prog)
    db.session.commit()
    
    return render_template('library/detail.html', resource=resource)

@library_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != 'teacher' and current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('library.hub'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        res_type = request.form.get('type')
        # ... handle upload logic
        # For MVP, we'll create a dummy resource
        new_res = Resource(
            title=title,
            subject=request.form.get('subject'),
            difficulty=request.form.get('difficulty'),
            resource_type=res_type,
            uploaded_by=current_user.id,
            description=request.form.get('description')
        )
        db.session.add(new_res)
        db.session.commit()
        flash("Resource added to Library!", "success")
        return redirect(url_for('library.hub'))
        
    return render_template('library/upload.html')
