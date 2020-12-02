# File sets up the django environment, used by other scripts that need to
# execute in django land
import os
import django
from django.conf import settings

APP_NAME = "crawfish"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), APP_NAME))


def boot_django():
    settings.configure(
        APP_ENVIRONMENT="test",
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(APP_NAME,),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()