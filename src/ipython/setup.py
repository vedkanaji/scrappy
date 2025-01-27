import os
import sys
from pathlib import Path

# Get base directory by going up one level from the current file
BASE_DIR = str(Path(__file__).resolve().parent.parent)

def init_django(project_name='config'):
    """
    Initialize Django environment for scripts/notebooks.
    
    Args:
        project_name (str): Name of the Django project (default: 'config')
    """
    if not project_name:
        raise ValueError("project_name must be specified")

    # Check if Django is already configured
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        import django.apps
        if django.apps.apps.ready:
            print("Django is already configured.")
            return

    try:
        # Ensure BASE_DIR is in the Python path
        if BASE_DIR not in sys.path:
            sys.path.insert(0, BASE_DIR)
        
        # Configure Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        
        # Import and setup Django
        import django
        django.setup()
        
        print(f"Django setup complete. Using project: {project_name}")
        print(f"Settings module: {os.environ['DJANGO_SETTINGS_MODULE']}")
        print(f"Base directory: {BASE_DIR}")
        
    except Exception as e:
        print(f"Failed to initialize Django: {str(e)}")
        raise

# Print diagnostic information when module is imported
if __name__ != '__main__':
    print(f"setup.py loaded from: {__file__}")
    print(f"Base directory: {BASE_DIR}")