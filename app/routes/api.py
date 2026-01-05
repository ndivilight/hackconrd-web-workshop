from flask import Blueprint, request, jsonify
from app.auth import token_required, create_token
from app.models import get_db_connection, query_db
import subprocess

bp = Blueprint('api', __name__)

@bp.route('/auth/token', methods=['POST'])
def get_token():
    """Get JWT token - VULNERABLE TO SQL INJECTION"""
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    # VULNERABLE: SQL injection in API endpoint
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
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                }
            })
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/employees', methods=['GET'])
@token_required
def list_employees(current_user):
    """List employees - VULNERABLE TO SQL INJECTION"""
    search = request.args.get('search', '')
    department = request.args.get('department', '')

    # Build query with vulnerabilities
    query = "SELECT id, employee_id, first_name, last_name, email, department, position FROM employees WHERE 1=1"

    if search:
        # VULNERABLE: SQL injection via search parameter
        query += f" AND (first_name LIKE '%{search}%' OR last_name LIKE '%{search}%')"

    if department:
        # VULNERABLE: SQL injection via department parameter
        query += f" AND department = '{department}'"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        employees = cursor.fetchall()
        conn.close()

        return jsonify({
            'success': True,
            'employees': [dict(emp) for emp in employees]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/employees/<int:id>', methods=['GET'])
@token_required
def get_employee(current_user, id):
    """Get employee details - VULNERABLE TO IDOR"""
    # VULNERABLE: No authorization check - any valid token can access any employee
    employee = query_db('SELECT * FROM employees WHERE id = ?', [id], one=True)

    if employee:
        return jsonify({
            'success': True,
            'employee': dict(employee)
        })
    return jsonify({'success': False, 'error': 'Employee not found'}), 404

@bp.route('/tools/ping', methods=['POST'])
@token_required
def api_ping(current_user):
    """Ping via API - VULNERABLE TO COMMAND INJECTION"""
    data = request.get_json() or {}
    host = data.get('host', '')

    if not host:
        return jsonify({'success': False, 'error': 'Host is required'}), 400

    # VULNERABLE: Command injection
    command = f"ping -c 3 {host}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return jsonify({
            'success': True,
            'command': command,
            'output': result.stdout + result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/debug', methods=['GET'])
def debug_info():
    """Debug endpoint - Information disclosure"""
    # VULNERABLE: Exposes sensitive configuration
    from app.config import Config
    return jsonify({
        'secret_key': Config.SECRET_KEY[:10] + '...',
        'jwt_secret': Config.JWT_SECRET_KEY,
        'database': Config.DATABASE_PATH,
        'debug': Config.DEBUG
    })
