import atexit
import os
import subprocess
import sys
import time
from pathlib import Path

from starfruit.logger import get_logger
from starfruit.server import API_HOST, API_PORT

logger = get_logger(__name__)

_systray_process = None


def launch_systray(
    webapp_host=API_HOST,
    webapp_port=API_PORT,
    api_host="127.0.0.1",
    api_port=8022,
    version="unknown",
):
    """
    Launch the system tray icon in a separate process.
    Returns success (bool): True if the systray process was launched successfully.
    """
    global _systray_process

    # Make sure Python executable is available
    python_exe = sys.executable
    if not python_exe:
        logger.error("Could not determine Python executable")
        return False

    # Get the script path
    script_dir = Path(__file__).parent
    systray_script = script_dir / "proc_systray.py"

    if not systray_script.exists():
        logger.error(f"Systray script not found at: {systray_script}")
        return False

    current_pid = os.getpid()

    try:
        # Build command
        cmd = [
            python_exe,
            str(systray_script),
            "--host",
            str(webapp_host),
            "--port",
            str(webapp_port),
            "--api-host",
            str(api_host),
            "--api-port",
            str(api_port),
            "--version",
            str(version),
            "--parent-pid",
            str(current_pid),  # Pass parent PID for monitoring
        ]

        logger.debug(f"Launching systray with command: {cmd}")

        _systray_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
        )

        logger.debug(f"Systray process launched with PID: {_systray_process.pid}")

        # Give it a moment to start
        time.sleep(0.2)

        # Check if process is still running
        if _systray_process.poll() is not None:
            # Process exited immediately - check for errors
            errors = _systray_process.stderr.read() if _systray_process.stderr else "Unknown error"
            logger.error(f"Systray process failed to start: {errors}")
            return False

        # Register cleanup on program exit
        atexit.register(terminate_systray)

        return True

    except Exception as e:
        logger.error(f"Error launching systray: {e}")
        return False


def terminate_systray():
    global _systray_process

    if not _systray_process:
        logger.debug("No systray process to terminate")
        return False

    try:
        if _systray_process.poll() is None:
            logger.debug(f"Terminating systray process: {_systray_process.pid}")
            _systray_process.terminate()

            # Wait briefly for termination
            try:
                _systray_process.wait(1.0)
            except subprocess.TimeoutExpired:
                logger.warning("Systray did not terminate gracefully, forcing kill")
                _systray_process.kill()

        logger.debug("Systray process terminated")
        _systray_process = None
        return True

    except Exception as e:
        logger.error(f"Error terminating systray process: {e}")
        return False
