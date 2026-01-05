import jwt
from functools import wraps
from flask import request, jsonify, session
from app.config import Config

def create_token(user_id, username, role):
    """Create a JWT token - intentionally vulnerable"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role
        # Note: No expiration - intentionally vulnerable
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

def decode_token(token):
    """Decode a JWT token - allows algorithm confusion"""
    try:
        # Vulnerable: accepts 'none' algorithm if specified in token header
        header = jwt.get_unverified_header(token)
        if header.get('alg') == 'none':
            # Algorithm confusion vulnerability
            return jwt.decode(token, options={"verify_signature": False})
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM, 'none'])
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator for JWT-protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid token'}), 401

        return f(payload, *args, **kwargs)

    return decorated

def login_required(f):
    """Decorator for session-protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            from flask import redirect, url_for
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated
