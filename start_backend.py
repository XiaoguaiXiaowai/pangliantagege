import os
import subprocess
import sys

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, 'backend')

    print(f"Starting Django backend in {backend_dir} (127.0.0.1:8000)...")
    print("Press Ctrl+C to stop.")

    manage_py = os.path.join(backend_dir, 'manage.py')
    if not os.path.exists(manage_py):
        print(f"Error: {manage_py} not found.")
        return

    try:
        # Run in foreground
        subprocess.run(
            [sys.executable, 'manage.py', 'runserver'],
            cwd=backend_dir
        )
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    except Exception as e:
        print(f"Error running backend: {e}")

if __name__ == '__main__':
    main()
