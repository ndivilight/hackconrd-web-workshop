from flask import Blueprint, render_template, request, session
from jinja2 import Template
from app.auth import login_required
from app.models import query_db

bp = Blueprint('reports', __name__)

@bp.route('/')
@login_required
def index():
    """Report templates page"""
    return render_template('reports/index.html')

@bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    """Generate report - VULNERABLE TO SSTI"""
    output = None
    error = None
    template_content = request.form.get('template', '') or request.args.get('template', '')

    # Pre-built templates
    templates = {
        'employee_list': '''
<h3>Employee Directory Report</h3>
<p>Generated for: {{ user.username }}</p>
<table class="table">
    <tr><th>Name</th><th>Department</th><th>Position</th></tr>
    {% for emp in employees %}
    <tr><td>{{ emp.first_name }} {{ emp.last_name }}</td><td>{{ emp.department }}</td><td>{{ emp.position }}</td></tr>
    {% endfor %}
</table>
''',
        'announcement_summary': '''
<h3>Announcements Summary</h3>
<p>Total: {{ announcements|length }} announcements</p>
{% for a in announcements %}
<div class="card mb-2">
    <div class="card-body">
        <h5>{{ a.title }}</h5>
        <p>{{ a.content[:100] }}...</p>
    </div>
</div>
{% endfor %}
'''
    }

    if request.method == 'POST':
        template_name = request.form.get('template_name', '')

        if template_name and template_name in templates:
            template_content = templates[template_name]
        elif not template_content:
            template_content = request.form.get('custom_template', '')

        if template_content:
            try:
                # VULNERABLE: User-controlled template is directly rendered
                # This allows Server-Side Template Injection (SSTI)
                #
                # Payload examples:
                # - {{ 7*7 }} -> 49
                # - {{ config }}
                # - {{ config.SECRET_KEY }}
                # - {{ ''.__class__.__mro__[1].__subclasses__() }}
                # - {{ ''.__class__.__mro__[1].__subclasses__()[X].__init__.__globals__['os'].popen('id').read() }}
                #
                # More advanced payloads for RCE:
                # {{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}

                # Fetch data for template context
                employees = query_db('SELECT * FROM employees')
                announcements = query_db('SELECT * FROM announcements')
                user = {
                    'username': session.get('username', 'Unknown'),
                    'role': session.get('role', 'employee')
                }

                # VULNERABLE: Creating template from user input
                template = Template(template_content)
                output = template.render(
                    employees=employees,
                    announcements=announcements,
                    user=user,
                    config=None  # Intentionally not passing config, but it's still accessible via SSTI
                )

            except Exception as e:
                difficulty = session.get('difficulty', 'easy')
                if difficulty == 'easy':
                    error = f'Template error: {str(e)}'
                elif difficulty == 'medium':
                    error = f'Error: {type(e).__name__}'
                else:
                    error = 'Failed to generate report'

    return render_template('reports/generate.html',
                         output=output,
                         error=error,
                         template_content=template_content,
                         templates=templates)

@bp.route('/preview', methods=['POST'])
@login_required
def preview():
    """Preview template - also VULNERABLE TO SSTI"""
    template_content = request.form.get('template', '')

    if not template_content:
        return {'error': 'No template provided'}, 400

    try:
        template = Template(template_content)
        output = template.render(
            user={'username': session.get('username', 'Unknown')},
            employees=[],
            announcements=[]
        )
        return {'output': output}
    except Exception as e:
        return {'error': str(e)}, 400
