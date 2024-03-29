#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("switching to test mode")
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.test"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # This allows easy placement of apps within the interior apps directory.
    sys.path.append(f'{Path(__file__).parent / "apps"}')
    sys.path.append(f'{Path(__file__).parent / "config"}')

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
