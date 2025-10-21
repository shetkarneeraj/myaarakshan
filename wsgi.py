#!/usr/bin/env python3
"""
WSGI Entry Point for Maratha Aarakshan Django Application
Production-ready configuration with Gunicorn and Django
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maratha_aarakshan.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# This is what Gunicorn will use
application = get_wsgi_application()

if __name__ == "__main__":
    # Development mode - run Django development server
    import django
    from django.core.management import execute_from_command_line
    django.setup()
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])