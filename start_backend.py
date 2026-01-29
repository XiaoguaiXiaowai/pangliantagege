import os
import subprocess
import sys

def main():
    """
    Start the Django backend server.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, 'backend')
    
    print(f"Starting Django backend in {backend_dir}...")
    
    # Check if manage.py exists
    manage_py = os.path.join(backend_dir, 'manage.py')
    if not os.path.exists(manage_py):
        print(f"Error: {manage_py} not found.")
        return

    # Run the server
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'], cwd=backend_dir, check=True)
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    except Exception as e:
        print(f"Error starting backend: {e}")

if __name__ == '__main__':
    main()
