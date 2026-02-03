"""
Settings module configuration.
Loads settings based on DJANGO_SETTINGS_MODULE environment variable.
"""

import os

ENVIRONMENT = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.base')

if ENVIRONMENT == 'config.settings.prod':
    from .prod import *
elif ENVIRONMENT == 'config.settings.dev':
    from .dev import *
else:
    from .base import *
