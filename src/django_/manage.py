#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from pathlib import Path
import sys


def main():
    """Run administrative tasks."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    sys.path.append(str(BASE_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        port = os.getenv("PORT", 3000)
        if len(sys.argv) > 2:
            sys.argv.pop(-1)
        sys.argv.append(f"{port}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
