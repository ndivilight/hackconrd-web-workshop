from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import get_db_connection, query_db
from app.auth import create_token

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - VULNERABLE TO SQL INJECTION"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # VULNERABLE: Direct string concatenation in SQL query
        # This allows SQL injection attacks like:
        # username: admin' --
        # username: ' OR '1'='1
        # password: ' OR '1'='1' --
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']

                # Get employee_id for profile link
                employee = query_db(
                    'SELECT id FROM employees WHERE user_id = ?',
                    [user['id']], one=True
                )
                if employee:
                    session['employee_id'] = employee['id']

                flash('Welcome back!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                # Different error messages based on difficulty
                difficulty = session.get('difficulty', 'easy')
                if difficulty == 'easy':
                    flash(f'Login failed. Query executed: {query}', 'danger')
                elif difficulty == 'medium':
                    flash('Invalid username or password. Check your credentials.', 'danger')
                else:
                    flash('Login failed.', 'danger')

        except Exception as e:
            difficulty = session.get('difficulty', 'easy')
            if difficulty == 'easy':
                flash(f'Database error: {str(e)}', 'danger')
            elif difficulty == 'medium':
                flash('A database error occurred.', 'danger')
            else:
                flash('Login failed.', 'danger')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    """Logout - clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/token', methods=['POST'])
def get_token():
    """Get JWT token - VULNERABLE TO SQL INJECTION"""
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    # Same SQL injection vulnerability as login
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            token = create_token(user['id'], user['username'], user['role'])
            return jsonify({
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
