from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.auth import login_required
from app.models import query_db, execute_db

bp = Blueprint('announcements', __name__)

@bp.route('/')
@login_required
def index():
    """List all announcements"""
    announcements = query_db('''
        SELECT a.*, u.username as author_name
        FROM announcements a
        LEFT JOIN users u ON a.author_id = u.id
        ORDER BY a.created_at DESC
    ''')
    return render_template('announcements/index.html', announcements=announcements)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create new announcement - VULNERABLE TO STORED XSS"""
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')

        if title and content:
            # VULNERABLE: Content is stored without sanitization
            # and will be rendered without escaping
            # Payload examples:
            # - <script>alert('XSS')</script>
            # - <img src=x onerror="alert('XSS')">
            # - <svg onload="alert('XSS')">
            execute_db(
                'INSERT INTO announcements (title, content, author_id) VALUES (?, ?, ?)',
                [title, content, session.get('user_id')]
            )
            flash('Announcement posted successfully!', 'success')
            return redirect(url_for('announcements.index'))
        else:
            flash('Title and content are required.', 'danger')

    return render_template('announcements/new.html')

@bp.route('/search')
@login_required
def search():
    """Search announcements - VULNERABLE TO REFLECTED XSS"""
    query = request.args.get('q', '')
    announcements = []

    if query:
        announcements = query_db('''
            SELECT a.*, u.username as author_name
            FROM announcements a
            LEFT JOIN users u ON a.author_id = u.id
            WHERE a.title LIKE ? OR a.content LIKE ?
            ORDER BY a.created_at DESC
        ''', [f'%{query}%', f'%{query}%'])

    # VULNERABLE: The query parameter will be reflected in the template
    # without proper escaping in certain places
    return render_template('announcements/search.html',
                         announcements=announcements,
                         query=query)

@bp.route('/<int:id>')
@login_required
def view(id):
    """View single announcement"""
    announcement = query_db('''
        SELECT a.*, u.username as author_name
        FROM announcements a
        LEFT JOIN users u ON a.author_id = u.id
        WHERE a.id = ?
    ''', [id], one=True)

    if not announcement:
        flash('Announcement not found.', 'warning')
        return redirect(url_for('announcements.index'))

    return render_template('announcements/view.html', announcement=announcement)
