from flask import Blueprint, render_template, session, redirect, url_for
from app.auth import login_required
from app.models import query_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page - redirect to dashboard or login"""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with stats"""
    # Get counts for dashboard
    employees_count = query_db('SELECT COUNT(*) as count FROM employees', one=True)['count']
    announcements_count = query_db('SELECT COUNT(*) as count FROM announcements', one=True)['count']

    # Get recent announcements
    recent_announcements = query_db(
        'SELECT * FROM announcements ORDER BY created_at DESC LIMIT 5'
    )

    return render_template('dashboard.html',
                         employees_count=employees_count,
                         announcements_count=announcements_count,
                         recent_announcements=recent_announcements)

@bp.route('/set-difficulty/<level>')
def set_difficulty(level):
    """Set the difficulty level"""
    if level in ['easy', 'medium', 'hard']:
        session['difficulty'] = level
    return redirect(request.referrer or url_for('main.dashboard'))

# Import request at the top level to avoid issues
from flask import request
