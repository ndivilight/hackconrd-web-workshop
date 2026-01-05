from flask import Flask, session
from app.config import Config

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register context processor for difficulty levels
    @app.context_processor
    def inject_difficulty():
        return {
            'difficulty': session.get('difficulty', 'easy'),
            'difficulties': ['easy', 'medium', 'hard']
        }

    # Register blueprints
    from app.routes import auth, main, employees, announcements, documents, tools, reports, api

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(employees.bp, url_prefix='/employees')
    app.register_blueprint(announcements.bp, url_prefix='/announcements')
    app.register_blueprint(documents.bp, url_prefix='/documents')
    app.register_blueprint(tools.bp, url_prefix='/tools')
    app.register_blueprint(reports.bp, url_prefix='/reports')
    app.register_blueprint(api.bp, url_prefix='/api')

    return app
