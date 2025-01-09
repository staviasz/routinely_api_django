from pathlib import Path
from main.configs.env import env

PYTHON_ENV = env["env"]
BASE_DIR = Path(__file__).resolve().parent.parent.parent


DATABASE = {}

match PYTHON_ENV:
    case "development":
        DATABASE = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "django_/db.sqlite3",
            }
        }
    case "production":
        DATABASE = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": env["backend"]["url"],
                "USER": env["backend"]["url"],
                "PASSWORD": env["backend"]["url"],
                "HOST": env["backend"]["url"],
                "PORT": env["backend"]["port"],
            }
        }
    case "test":
        DATABASE = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "django_/db_test.sqlite3",
            }
        }
