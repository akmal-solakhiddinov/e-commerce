# manage.py
import os
import sys
from decouple import config

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    port = config('DJANGO_PORT', default='8000')
    print(f"Running server on port: {port}")
    execute_from_command_line([sys.argv[0], 'runserver', port])

if __name__ == '__main__':
    main()
