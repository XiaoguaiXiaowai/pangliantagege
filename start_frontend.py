import os
import subprocess

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, 'frontend')

    print(f"Starting frontend dev server in {frontend_dir} (127.0.0.1:5173)...")
    print("Press Ctrl+C to stop.")

    try:
        # Run in foreground (npm run dev instead of preview for local development)
        subprocess.run(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir
        )
    except KeyboardInterrupt:
        print("\nFrontend server stopped.")
    except Exception as e:
        print(f"Error starting frontend: {e}")

if __name__ == '__main__':
    main()

