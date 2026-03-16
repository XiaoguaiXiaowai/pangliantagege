import os
import subprocess
import sys
import signal

PID_DIR_NAME = "run"
LOG_DIR_NAME = "logs"
PID_FILE_NAME = "frontend.pid"
OUT_LOG = "frontend.out"
ERR_LOG = "frontend.err"

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, 'frontend')

    pid_dir = os.path.join(project_root, PID_DIR_NAME)
    log_dir = os.path.join(project_root, LOG_DIR_NAME)
    os.makedirs(pid_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    pid_file = os.path.join(pid_dir, PID_FILE_NAME)
    out_log_path = os.path.join(log_dir, OUT_LOG)
    err_log_path = os.path.join(log_dir, ERR_LOG)

    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"Frontend already running with PID {pid}")
            return
        except Exception:
            try:
                os.remove(pid_file)
            except Exception:
                pass

    print(f"Starting frontend preview server in {frontend_dir} (0.0.0.0:5173)...")

    out_f = open(out_log_path, "ab", buffering=0)
    err_f = open(err_log_path, "ab", buffering=0)
    try:
        # Use vite preview to serve built files
        # Ensure host is 0.0.0.0 to expose externally
        cmd = ['npm', 'run', 'preview', '--', '--host', '0.0.0.0', '--port', '5173']
        proc = subprocess.Popen(
            cmd,
            cwd=frontend_dir,
            stdout=out_f,
            stderr=err_f,
            start_new_session=True,
        )
        with open(pid_file, "w") as f:
            f.write(str(proc.pid))
        print(f"Frontend started in background with PID {proc.pid}")
    except Exception as e:
        print(f"Error starting frontend: {e}")
    finally:
        try:
            out_f.flush()
            err_f.flush()
        except Exception:
            pass

if __name__ == '__main__':
    main()

