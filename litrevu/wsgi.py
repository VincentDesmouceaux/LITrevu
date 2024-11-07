"""
WSGI config for litrevu project.

This file exposes the WSGI callable as a module-level variable named `application`.

WSGI (Web Server Gateway Interface) is the interface between web servers and Python web applications. It allows Django to communicate with the server in a standardized way.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'litrevu' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litrevu.settings')

# Instantiate the WSGI application object
application = get_wsgi_application()
