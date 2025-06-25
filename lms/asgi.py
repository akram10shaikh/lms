"""
ASGI config for lms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys
import logging
from django.core.asgi import get_asgi_application

# Optional: Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')

# Optional: Basic logging for ASGI startup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting ASGI application...")

# Initialize ASGI application
application = get_asgi_application()
