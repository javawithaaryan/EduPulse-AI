from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.library import Resource, LearningProgress, LibraryRecommendation
from services.openai_service import OpenAIService
from services.recommendation_service import RecommendationService

library_bp = Blueprint('library', __name__, template_folder='templates')

@library_bp.route('/hub')
@login_required
def hub():
    # Get AI-powered recommendations for students
    if current_user.role == 'student':
        try:
            rec_data = RecommendationService.generate_recommendations(current_user.id, limit=3)
            recommendations = [r['resource'] for r in rec_data]
            rec_reasons = {r['resource'].id: r['reason'] for r in rec_data}
        except Exception as e:
            # Fallback if recommendation fails
            print(f"Recommendation error: {e}")
            recommendations = Resource.query.limit(3).all()
            rec_reasons = {}
    else:
        recommendations = Resource.query.limit(3).all()
        rec_reasons = {}
    
    recent = Resource.query.order_by(Resource.created_at.desc()).limit(5).all()
    
    return render_template('library/hub.html', 
                         recommendations=recommendations,
                         rec_reasons=rec_reasons,
                         recent=recent)

@library_bp.route('/search')
@login_required
def search():
    """Semantic search for library resources"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('library.hub'))
    
    # Simple keyword search (can be enhanced with OpenAI embeddings)
    search_terms = query.lower().split()
    
    results = Resource.query.filter(
        db.or_(
            Resource.title.ilike(f'%{query}%'),
            Resource.description.ilike(f'%{query}%'),
            Resource.subject.ilike(f'%{query}%')
        )
    ).all()
    
    # Score results based on relevance (simple matching)
    scored_results = []
    for res in results:
        score = 0
        text = f"{res.title} {res.description} {res.subject}".lower()
        for term in search_terms:
            score += text.count(term)
        scored_results.append({'resource': res, 'score': score})
    
    # Sort by relevance
    scored_results.sort(key=lambda x: x['score'], reverse=True)
    results = [r['resource'] for r in scored_results]
    
    return render_template('library/search.html',
                         query=query,
                         results=results,
                         count=len(results))

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
