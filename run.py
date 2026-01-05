#!/usr/bin/env python3
"""
Run the TechCorp Portal application
"""

import os
from app import create_app
from app.models import init_db

# Initialize database if it doesn't exist
if not os.path.exists('data/portal.db'):
    print("Initializing database...")
    init_db()
    # Run the seeder
    from scripts.init_db import seed_database
    seed_database()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
