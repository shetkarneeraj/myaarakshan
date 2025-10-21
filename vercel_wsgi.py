"""
Vercel-specific WSGI application entry point
Optimized for serverless deployment
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Set Django settings for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maratha_aarakshan.settings')

# Initialize Django
import django
django.setup()

# Import WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()

# Vercel-specific optimizations
app = application
