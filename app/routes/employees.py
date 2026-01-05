from flask import Blueprint, render_template, request, session
from app.auth import login_required
from app.models import get_db_connection, query_db

bp = Blueprint('employees', __name__)

@bp.route('/')
@login_required
def index():
    """Employee directory listing"""
    employees = query_db('SELECT * FROM employees ORDER BY last_name, first_name')
    return render_template('employees/index.html', employees=employees)

@bp.route('/search')
@login_required
def search():
    """Search employees - VULNERABLE TO SQL INJECTION"""
    query_param = request.args.get('q', '')
    employees = []
    error = None

    if query_param:
        # VULNERABLE: Direct string concatenation allows SQL injection
        # Examples:
        # - ' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11 --
        # - ' UNION SELECT id,username,password,role,department,email,created_at,null,null,null,null FROM users --
        # - ' OR '1'='1
        sql = f"""
            SELECT * FROM employees
            WHERE first_name LIKE '%{query_param}%'
            OR last_name LIKE '%{query_param}%'
            OR department LIKE '%{query_param}%'
            OR position LIKE '%{query_param}%'
        """

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            employees = cursor.fetchall()
            conn.close()
        except Exception as e:
            difficulty = session.get('difficulty', 'easy')
            if difficulty == 'easy':
                error = f'Database error: {str(e)} | Query: {sql}'
            elif difficulty == 'medium':
                error = f'Database error: {str(e)}'
            else:
                error = 'An error occurred while searching.'

    return render_template('employees/search.html',
                         employees=employees,
                         query=query_param,
                         error=error)

@bp.route('/<int:id>')
@login_required
def profile(id):
    """View employee profile - VULNERABLE TO IDOR"""
    # VULNERABLE: No authorization check
    # Any authenticated user can view any employee's profile by changing the ID
    employee = query_db('SELECT * FROM employees WHERE id = ?', [id], one=True)

    if not employee:
        return render_template('employees/not_found.html'), 404

    # Get user info if linked
    user = None
    if employee['user_id']:
        user = query_db('SELECT id, username, role, email FROM users WHERE id = ?',
                       [employee['user_id']], one=True)

    return render_template('employees/profile.html', employee=employee, user=user)

@bp.route('/<int:id>/payslip')
@login_required
def payslip(id):
    """View employee payslip - VULNERABLE TO IDOR"""
    # VULNERABLE: No authorization check
    # Any authenticated user can view any employee's salary/payslip
    employee = query_db('SELECT * FROM employees WHERE id = ?', [id], one=True)

    if not employee:
        return render_template('employees/not_found.html'), 404

    return render_template('employees/payslip.html', employee=employee)
