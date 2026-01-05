import subprocess
import shlex
from flask import Blueprint, render_template, request, jsonify, session
from app.auth import login_required

bp = Blueprint('tools', __name__)

@bp.route('/')
@login_required
def index():
    """Network tools page"""
    return render_template('tools/index.html')

@bp.route('/ping', methods=['POST'])
@login_required
def ping():
    """Ping utility - VULNERABLE TO COMMAND INJECTION"""
    host = request.form.get('host', '')

    if not host:
        return jsonify({'error': 'Host is required'}), 400

    # VULNERABLE: Direct command execution without sanitization
    # Payload examples:
    # - ; cat /etc/passwd
    # - | whoami
    # - `whoami`
    # - $(cat /etc/passwd)
    # - 127.0.0.1; ls -la
    # - 127.0.0.1 && cat /etc/passwd
    command = f"ping -c 3 {host}"

    try:
        # VULNERABLE: shell=True allows command injection
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr

        difficulty = session.get('difficulty', 'easy')
        if difficulty == 'easy':
            output = f"Command: {command}\n\n{output}"

        return jsonify({'output': output})

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        difficulty = session.get('difficulty', 'easy')
        if difficulty == 'easy':
            return jsonify({'error': f'Error executing command: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Command execution failed'}), 500

@bp.route('/nslookup', methods=['POST'])
@login_required
def nslookup():
    """DNS lookup utility - VULNERABLE TO COMMAND INJECTION"""
    domain = request.form.get('domain', '')

    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    # VULNERABLE: Same command injection vulnerability
    command = f"nslookup {domain}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr

        difficulty = session.get('difficulty', 'easy')
        if difficulty == 'easy':
            output = f"Command: {command}\n\n{output}"

        return jsonify({'output': output})

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        difficulty = session.get('difficulty', 'easy')
        if difficulty == 'easy':
            return jsonify({'error': f'Error: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Lookup failed'}), 500

@bp.route('/traceroute', methods=['POST'])
@login_required
def traceroute():
    """Traceroute utility - VULNERABLE TO COMMAND INJECTION"""
    host = request.form.get('host', '')

    if not host:
        return jsonify({'error': 'Host is required'}), 400

    # VULNERABLE: Command injection
    command = f"traceroute -m 10 {host}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr

        difficulty = session.get('difficulty', 'easy')
        if difficulty == 'easy':
            output = f"Command: {command}\n\n{output}"

        return jsonify({'output': output})

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        return jsonify({'error': 'Traceroute failed'}), 500
