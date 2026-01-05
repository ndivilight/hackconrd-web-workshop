# TechCorp Portal - Vulnerable Web Application for HackConRD 2026
# WARNING: This application is intentionally vulnerable. DO NOT deploy in production!

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=1

# Install system dependencies for network tools
RUN apt-get update && apt-get install -y \
    iputils-ping \
    dnsutils \
    traceroute \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/documents

# Initialize the database and seed data
RUN python scripts/init_db.py

# Create sample documents
RUN echo "TechCorp Employee Handbook\n\nWelcome to TechCorp!\n\nThis handbook contains important policies and procedures." > data/documents/employee_handbook.txt && \
    echo "TechCorp Security Policy\n\nAll employees must follow these security guidelines:\n1. Use strong passwords\n2. Lock your workstation\n3. Report suspicious activity" > data/documents/security_policy.txt && \
    echo "Q1 2026 Financial Report\n\nRevenue: $1,234,567\nExpenses: $987,654\nNet Profit: $246,913" > data/documents/q1_report.txt && \
    echo "IT Support Procedures\n\nFor IT support:\n1. Submit a ticket\n2. Include detailed description\n3. Priority levels: Low, Medium, High, Critical" > data/documents/it_procedures.txt && \
    echo "flag{directory_traversal_success}" > /flag.txt

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
