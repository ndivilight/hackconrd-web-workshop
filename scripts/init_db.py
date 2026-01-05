#!/usr/bin/env python3
"""
Database initialization script for TechCorp Portal
Creates tables and populates with sample data for the workshop
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import init_db, execute_db, get_db_connection

def seed_database():
    """Populate database with sample data"""

    # Sample users (passwords in plain text - intentionally insecure)
    users = [
        ('admin', 'admin123', 'admin', 'IT', 'admin@techcorp.local'),
        ('jsmith', 'password123', 'employee', 'Engineering', 'jsmith@techcorp.local'),
        ('mjones', 'welcome1', 'employee', 'HR', 'mjones@techcorp.local'),
        ('rbrown', 'qwerty', 'manager', 'Finance', 'rbrown@techcorp.local'),
        ('kwilliams', 'letmein', 'employee', 'Marketing', 'kwilliams@techcorp.local'),
        ('test', 'test', 'employee', 'IT', 'test@techcorp.local'),
    ]

    # Sample employees
    employees = [
        ('EMP001', 'John', 'Smith', 'jsmith@techcorp.local', 'Engineering', 'Senior Developer', 95000.00, '555-0101', '2020-03-15', 2),
        ('EMP002', 'Maria', 'Jones', 'mjones@techcorp.local', 'HR', 'HR Manager', 78000.00, '555-0102', '2019-07-22', 3),
        ('EMP003', 'Robert', 'Brown', 'rbrown@techcorp.local', 'Finance', 'Finance Director', 125000.00, '555-0103', '2018-01-10', 4),
        ('EMP004', 'Karen', 'Williams', 'kwilliams@techcorp.local', 'Marketing', 'Marketing Specialist', 62000.00, '555-0104', '2021-09-01', 5),
        ('EMP005', 'Admin', 'User', 'admin@techcorp.local', 'IT', 'System Administrator', 85000.00, '555-0100', '2017-06-01', 1),
        ('EMP006', 'David', 'Miller', 'dmiller@techcorp.local', 'Engineering', 'Junior Developer', 55000.00, '555-0105', '2023-02-14', None),
        ('EMP007', 'Sarah', 'Davis', 'sdavis@techcorp.local', 'HR', 'Recruiter', 52000.00, '555-0106', '2022-11-30', None),
        ('EMP008', 'Michael', 'Wilson', 'mwilson@techcorp.local', 'Finance', 'Accountant', 68000.00, '555-0107', '2020-08-17', None),
        ('EMP009', 'Emily', 'Taylor', 'etaylor@techcorp.local', 'Marketing', 'Content Writer', 48000.00, '555-0108', '2023-04-03', None),
        ('EMP010', 'James', 'Anderson', 'janderson@techcorp.local', 'IT', 'Network Engineer', 92000.00, '555-0109', '2019-12-01', None),
    ]

    # Sample announcements
    announcements = [
        ('Welcome to TechCorp Portal', 'Welcome to our new internal portal! Here you can find company documents, employee directory, and IT tools.', 1),
        ('Q1 2026 All-Hands Meeting', 'Join us for our quarterly all-hands meeting on January 15th at 2 PM in the main conference room. Remote employees can join via the usual video link.', 1),
        ('New Security Policy Update', 'Please review the updated security policy in the Documents section. All employees must acknowledge by end of month.', 3),
        ('IT Maintenance Window', 'Scheduled maintenance this Saturday from 2 AM to 6 AM. Some services may be unavailable during this time.', 1),
        ('Employee of the Month', 'Congratulations to John Smith for being selected as Employee of the Month! Thank you for your outstanding contributions.', 3),
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert users
    print("Creating users...")
    for user in users:
        try:
            cursor.execute(
                'INSERT INTO users (username, password, role, department, email) VALUES (?, ?, ?, ?, ?)',
                user
            )
            print(f"  Created user: {user[0]}")
        except Exception as e:
            print(f"  Skipping {user[0]}: {e}")

    # Insert employees
    print("\nCreating employees...")
    for emp in employees:
        try:
            cursor.execute(
                '''INSERT INTO employees
                   (employee_id, first_name, last_name, email, department, position, salary, phone, hire_date, user_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                emp
            )
            print(f"  Created employee: {emp[1]} {emp[2]}")
        except Exception as e:
            print(f"  Skipping {emp[1]} {emp[2]}: {e}")

    # Insert announcements
    print("\nCreating announcements...")
    for ann in announcements:
        try:
            cursor.execute(
                'INSERT INTO announcements (title, content, author_id) VALUES (?, ?, ?)',
                ann
            )
            print(f"  Created announcement: {ann[0][:40]}...")
        except Exception as e:
            print(f"  Skipping announcement: {e}")

    conn.commit()
    conn.close()
    print("\nDatabase seeding complete!")

def main():
    print("=" * 50)
    print("TechCorp Portal - Database Initialization")
    print("=" * 50)
    print()

    # Initialize database schema
    print("Initializing database schema...")
    init_db()
    print("Schema created successfully!\n")

    # Seed with sample data
    seed_database()

    print()
    print("=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print()
    print("Default credentials:")
    print("  admin / admin123  (Administrator)")
    print("  jsmith / password123  (Employee)")
    print("  test / test  (Test account)")
    print()

if __name__ == '__main__':
    main()
