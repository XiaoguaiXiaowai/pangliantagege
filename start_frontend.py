import os
import subprocess
import sys

def main():
    """
    Start the Vue frontend development server.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, 'frontend')
    
    print(f"Starting Vue frontend in {frontend_dir}...")
    
    # Check if package.json exists
    package_json = os.path.join(frontend_dir, 'package.json')
    if not os.path.exists(package_json):
        print(f"Error: {package_json} not found.")
        return

    # Run the dev server
    try:
        # Use 'npm.cmd' on Windows, 'npm' on Unix-like systems
        npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
        subprocess.run([npm_cmd, 'run', 'dev'], cwd=frontend_dir, check=True)
    except KeyboardInterrupt:
        print("\nFrontend server stopped.")
    except Exception as e:
        print(f"Error starting frontend: {e}")

if __name__ == '__main__':
    main()
