import atexit
import platform
import subprocess
import sys
import threading
from pathlib import Path

import psutil
from fastapi import APIRouter, BackgroundTasks

from starfruit.logger import get_logger

logger = get_logger(__name__)


router = APIRouter(prefix="/webview", tags=["webview"])

_webview_active = False
_webview_process = None


# Register cleanup function to ensure webview is terminated on server exit
def _cleanup_webview():
    global _webview_active, _webview_process

    # Terminate the process
    if _webview_process:
        try:
            if _webview_process.poll() is None:
                logger.debug(f"Terminating webview process (PID: {_webview_process.pid})")
                _webview_process.terminate()
                # Don't wait longer than 1 second - we need to exit
                try:
                    _webview_process.wait(1.0)
                except subprocess.TimeoutExpired:
                    logger.warning("Webview process did not terminate gracefully, forcing kill")
                    _webview_process.kill()

            _webview_active = False
            _webview_process = None
        except Exception as e:
            logger.error(f"Error terminating webview process: {e}")


atexit.register(_cleanup_webview)


@router.post("/launch")
async def launch_webview(
    background_tasks: BackgroundTasks, webapp_url: str = "http://127.0.0.1:8022", title: str = ""
):
    """Launch a webview window pointing to the App"""
    global _webview_active, _webview_process

    # Check if already active
    if _webview_active and _webview_process and _webview_process.poll() is None:
        # Try to focus the existing window
        focused = _focus_webview_window()
        if focused:
            return {"status": "focused", "message": "Brought existing webview to the foreground"}
        else:
            return {
                "status": "already_running",
                "message": "Webview is already running but couldn't bring to foreground",
            }

    # Reset state if process has terminated
    if _webview_process and _webview_process.poll() is not None:
        _webview_active = False
        _webview_process = None

    # Launch in a background task to not block the response
    background_tasks.add_task(_launch_webview_process, webapp_url, title if title else "starfruit")

    return {"status": "launching", "message": "Launching webview process"}


@router.post("/focus")
async def focus_webview():
    global _webview_active, _webview_process

    if not _webview_active or not _webview_process or _webview_process.poll() is not None:
        return {"status": "not_running", "message": "No webview process is running"}

    if _focus_webview_window():
        return {"status": "focused", "message": "Brought webview to the foreground"}
    else:
        return {"status": "error", "message": "Couldn't focus webview window"}


@router.get("/status")
async def webview_status():
    global _webview_active, _webview_process

    # Update status if needed
    if _webview_active and _webview_process and _webview_process.poll() is not None:
        _webview_active = False
        _webview_process = None

    return {
        "active": _webview_active,
        "process_running": _webview_process is not None and _webview_process.poll() is None,
    }


@router.post("/close")
async def close_webview():
    global _webview_active, _webview_process

    if not _webview_process:
        return {"status": "not_running", "message": "No webview process is running"}

    try:
        _webview_process.terminate()
        _webview_active = False
        _webview_process = None
        return {"status": "closed", "message": "Webview process terminated"}
    except Exception as e:
        logger.error(f"Error closing webview: {e}")
        return {"status": "error", "message": f"Error closing webview: {e}"}


# --- Helper Functions ---
def _focus_webview_window():
    """
    Platform-specific function to focus the webview window
    Returns True if successful, False otherwise
    """
    global _webview_process

    if not _webview_process:
        return False

    try:
        system = platform.system()

        if system == "Darwin":  # macOS
            # AppleScript to activate the app
            script = """
            tell application "System Events"
                set frontmost of every process whose unix id is {0} to true
            end tell
            """.format(_webview_process.pid)

            subprocess.run(["osascript", "-e", script], check=False)
            logger.debug(f"Focused macOS webview window for PID {_webview_process.pid}")
            return True

        elif system == "Windows":
            # On Windows, we can use pywin32, but we'll use a direct command approach here
            # using pythonw.exe's window title to find it
            try:
                # First try with psutil to get all window titles
                proc = psutil.Process(_webview_process.pid)
                # Then use powershell to focus the window by process ID
                ps_cmd = f"(Get-Process -Id {proc.pid} | Where-Object {{$_.MainWindowTitle}} | ForEach-Object {{ (New-Object -ComObject WScript.Shell).AppActivate($_.MainWindowTitle) }})"
                subprocess.run(["powershell", "-command", ps_cmd], check=False)
                logger.debug(f"Focused Windows webview window for PID {_webview_process.pid}")
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                logger.error("Could not focus webview window - process not found or access denied")
                return False

        elif system == "Linux":
            # For Linux, we'd use wmctrl but it's not always available
            # We could also try xdotool
            try:
                proc = psutil.Process(_webview_process.pid)
                # Try using wmctrl (if installed)
                subprocess.run(["wmctrl", "-i", "-a", str(proc.pid)], check=False)
                logger.debug(f"Focused Linux webview window for PID {_webview_process.pid}")
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):
                logger.error(
                    "Could not focus webview window - wmctrl not available or process issue"
                )
                return False

        logger.warning(f"No focus implementation for platform: {system}")
        return False

    except Exception as e:
        logger.error(f"Error focusing webview window: {e}")
        return False


def _launch_webview_process(webapp_url, title):
    """Launch the webview process and monitor it"""
    global _webview_active, _webview_process

    try:
        launcher_path = Path(__file__).parent / "proc_webview.py"

        if not launcher_path.exists():
            logger.error(f"Webview process script not found at: {launcher_path}")
            return

        python_exe = sys.executable
        cmd = [
            python_exe,
            str(launcher_path),
        ]

        logger.debug(f"Launching webview process with command: {' '.join(cmd)}")

        _webview_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
        )

        _webview_active = True

        def monitor_process():
            global _webview_active

            proc = _webview_process  # Local reference

            if not proc:
                return

            logger.debug(f"Monitoring webview process PID: {proc.pid}")

            # Read output
            while proc and proc.poll() is None:
                try:
                    if proc.stdout:
                        line = proc.stdout.readline().strip()
                        if line:
                            logger.debug(f"Webview process: {line}")
                except (IOError, BrokenPipeError) as e:
                    logger.debug(f"Error reading from webview stdout: {e}")
                    break

            # Process has exited
            exit_code = proc.returncode if proc and proc.returncode is not None else "unknown"
            logger.debug(f"Webview process exited with code: {exit_code}")

            # Check for errors
            if proc and proc.stderr:
                try:
                    error = proc.stderr.read()
                    if error:
                        logger.error(f"Webview process error: {error}")
                except (IOError, BrokenPipeError) as e:
                    logger.debug(f"Error reading from webview stderr: {e}")

            # Update state
            _webview_active = False

        # Start monitor thread
        threading.Thread(target=monitor_process, daemon=True, name="webview-monitor").start()

    except Exception as e:
        logger.error(f"Failed to launch webview: {e}")
        _webview_active = False
        _webview_process = None
