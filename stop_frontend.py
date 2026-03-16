import os
import signal
import time

PID_DIR_NAME = "run"
PID_FILE_NAME = "frontend.pid"

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    pid_file = os.path.join(project_root, PID_DIR_NAME, PID_FILE_NAME)

    if not os.path.exists(pid_file):
        print("Frontend PID file not found; nothing to stop.")
        return

    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
    except Exception as e:
        print(f"Failed to read PID file: {e}")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Sent SIGTERM to frontend PID {pid}")
        for _ in range(50):
            try:
                os.kill(pid, 0)
                time.sleep(0.1)
            except OSError:
                break
        else:
            print("Process did not exit, sending SIGKILL")
            os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        print("Frontend process not running.")
    finally:
        try:
            os.remove(pid_file)
        except Exception:
            pass

if __name__ == "__main__":
    main()

