"""
WSGI config for mainapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os  # pragma: no cover

from django.core.wsgi import get_wsgi_application  # pragma: no cover

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainapp.settings')  # pragma: no cover

application = get_wsgi_application()  # pragma: no cover
