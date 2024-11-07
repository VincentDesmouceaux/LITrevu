"""
ASGI config for litrevu project.

This file exposes the ASGI callable as a module-level variable named `application`.

ASGI (Asynchronous Server Gateway Interface) is the interface between web servers and asynchronous Python web applications.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'litrevu' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litrevu.settings')

# Instantiate the ASGI application object
application = get_asgi_application()
