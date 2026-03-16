import os
import subprocess
import sys
import signal

PID_DIR_NAME = "run"
LOG_DIR_NAME = "logs"
PID_FILE_NAME = "backend.pid"
OUT_LOG = "backend.out"
ERR_LOG = "backend.err"

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, 'backend')

    pid_dir = os.path.join(project_root, PID_DIR_NAME)
    log_dir = os.path.join(project_root, LOG_DIR_NAME)
    os.makedirs(pid_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    pid_file = os.path.join(pid_dir, PID_FILE_NAME)
    out_log_path = os.path.join(log_dir, OUT_LOG)
    err_log_path = os.path.join(log_dir, ERR_LOG)

    # If already running, don't start a duplicate
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"Backend already running with PID {pid}")
            return
        except Exception:
            # Stale PID file; remove it and continue
            try:
                os.remove(pid_file)
            except Exception:
                pass

    print(f"Starting Django backend in {backend_dir} (0.0.0.0:8000)...")

    manage_py = os.path.join(backend_dir, 'manage.py')
    if not os.path.exists(manage_py):
        print(f"Error: {manage_py} not found.")
        return

    # Start in background with stdout/stderr redirected to logs
    out_f = open(out_log_path, "ab", buffering=0)
    err_f = open(err_log_path, "ab", buffering=0)
    try:
        proc = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'],
            cwd=backend_dir,
            stdout=out_f,
            stderr=err_f,
            start_new_session=True,
        )
        with open(pid_file, "w") as f:
            f.write(str(proc.pid))
        print(f"Backend started in background with PID {proc.pid}")
    except Exception as e:
        print(f"Error starting backend: {e}")
    finally:
        # Don't close files before the process has a chance to inherit
        try:
            out_f.flush()
            err_f.flush()
        except Exception:
            pass

if __name__ == '__main__':
    main()
