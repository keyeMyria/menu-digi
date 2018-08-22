"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from whitenoise.django import DjangoWhiteNoise
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_digi.settings")
django.setup()

application = get_default_application
application = DjangoWhiteNoise(application)