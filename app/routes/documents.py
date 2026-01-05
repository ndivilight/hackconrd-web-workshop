import os
from flask import Blueprint, render_template, request, send_file, session, abort
from app.auth import login_required
from app.config import Config

bp = Blueprint('documents', __name__)

@bp.route('/')
@login_required
def index():
    """List available documents"""
    documents_path = Config.DOCUMENTS_PATH
    files = []

    if os.path.exists(documents_path):
        for filename in os.listdir(documents_path):
            filepath = os.path.join(documents_path, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                })

    return render_template('documents/index.html', files=files)

@bp.route('/download')
@login_required
def download():
    """Download a document - VULNERABLE TO DIRECTORY TRAVERSAL"""
    filename = request.args.get('file', '')

    if not filename:
        abort(400, 'No file specified')

    # VULNERABLE: No path validation or sanitization
    # Allows directory traversal attacks like:
    # - ../../../etc/passwd
    # - ....//....//....//etc/passwd
    # - ..%2f..%2f..%2fetc/passwd (URL encoded)
    filepath = os.path.join(Config.DOCUMENTS_PATH, filename)

    difficulty = session.get('difficulty', 'easy')

    # In easy mode, show the resolved path
    if difficulty == 'easy':
        # Still vulnerable, just shows more info
        resolved_path = os.path.abspath(filepath)
        if not os.path.exists(resolved_path):
            return render_template('documents/error.html',
                                 error=f'File not found: {resolved_path}',
                                 attempted_path=filepath), 404

    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        if difficulty == 'easy':
            return render_template('documents/error.html',
                                 error=f'File not found: {filepath}'), 404
        elif difficulty == 'medium':
            return render_template('documents/error.html',
                                 error='File not found'), 404
        else:
            abort(404)

@bp.route('/view')
@login_required
def view():
    """View document contents - VULNERABLE TO DIRECTORY TRAVERSAL"""
    filename = request.args.get('file', '')

    if not filename:
        abort(400, 'No file specified')

    # Same vulnerability as download
    filepath = os.path.join(Config.DOCUMENTS_PATH, filename)

    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return render_template('documents/view.html',
                             filename=filename,
                             content=content)
    except Exception as e:
        difficulty = session.get('difficulty', 'easy')
        if difficulty == 'easy':
            return render_template('documents/error.html',
                                 error=f'Error reading file: {str(e)}'), 500
        else:
            abort(404)
