#!/usr/bin/env python
"""
standalone script to run the webview in its own process.
this ensures it has its own main thread, required for macOS.
"""

import atexit
import os
import platform
import signal
import sys
import threading
import time

import psutil
import webview

from starfruit.logger import get_logger
from starfruit.server import API_HOST, API_PORT
from starfruit.utils.env import get_webview_debug

logger = get_logger(__name__)

window = None
shutting_down = False
parent_pid = None


url = f"http://{API_HOST}:{API_PORT}"
title = "✧ starfruit ✦"


def signal_handler(sig, frame):
    global shutting_down
    logger.info(f"Received signal {sig}, closing webview")
    shutting_down = True
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

#  Windows-specific signal handlers
if platform.system() == "Windows":
    try:
        # Use getattr to avoid linter errors
        win_break_signal = getattr(signal, "SIGBREAK", None)
        if win_break_signal is not None:
            signal.signal(win_break_signal, signal_handler)
    except (AttributeError, ValueError):
        # SIGBREAK doesn't exist or can't be used on this Windows installation
        logger.warning("SIGBREAK signal not available on this Windows installation.")


def cleanup():
    global window, shutting_down
    shutting_down = True

    # First destroy the window to release all UI resources
    if window and hasattr(webview, "windows") and webview.windows:
        try:
            logger.info("Destroying window on exit")
            window.destroy()
        except Exception as e:
            logger.error(f"Error destroying window: {e}")

    # Force exit the process after cleanup to ensure nothing keeps it alive
    logger.info("Cleanup complete - exiting process")
    # Give a moment for cleanup to complete before exit
    threading.Timer(1.0, lambda: os._exit(0)).start()


atexit.register(cleanup)


def on_window_close():
    global shutting_down
    shutting_down = True
    # This will trigger the atexit handler after the function completes
    sys.exit(0)


def monitor_parent_process():
    """Monitor the parent process and exit if it terminates"""
    global shutting_down, parent_pid

    if parent_pid is None:
        # If no parent PID specified, get the parent of this process
        parent_pid = os.getppid()
        logger.info(f"Using current parent process PID: {parent_pid}")

    logger.info(f"Starting parent process monitor for PID: {parent_pid}")

    while not shutting_down:
        try:
            # Check if parent process exists
            if not psutil.pid_exists(parent_pid):
                logger.info(f"Parent process (PID: {parent_pid}) no longer exists, shutting down")
                shutting_down = True
                cleanup()
                os._exit(0)  # Force exit

            # Check if parent is zombie/dead but still in process table
            try:
                parent = psutil.Process(parent_pid)
                if parent.status() == psutil.STATUS_ZOMBIE:
                    logger.info("Parent process is zombie, shutting down")
                    shutting_down = True
                    cleanup()
                    os._exit(0)  # Force exit
            except psutil.NoSuchProcess:
                logger.info("Parent process no longer exists (race condition), shutting down")
                shutting_down = True
                cleanup()
                os._exit(0)  # Force exit

        except Exception as e:
            logger.error(f"Error monitoring parent process: {e}")
            # Don't exit on monitoring errors

        # Check every second
        time.sleep(1)


if __name__ == "__main__":

    def delayed_watchdog():
        global shutting_down, window
        # Give the app 30 seconds to properly initialize
        time.sleep(30)
        # If we're still running (GUI is active) after 30 seconds, don't exit
        if not shutting_down and window is None:
            logger.error("Watchdog: Window failed to initialize after 30 seconds. Exiting.")
            os._exit(1)  # Force exit if window never appears

    # Start watchdog timer
    threading.Thread(target=delayed_watchdog, daemon=True).start()

    # Start parent process monitor
    threading.Thread(target=monitor_parent_process, daemon=True).start()

    # Create and start the window
    logger.info(f"Creating webview for: {url}")
    try:
        # Check if create_window exists
        if hasattr(webview, "create_window"):
            logger.info(f"Webview module: {webview.__name__}")
            logger.info(
                f"Available webview functions: {[name for name in dir(webview) if not name.startswith('_')]}"
            )
            window = webview.create_window(
                title, url, width=420, height=300, resizable=False, on_top=True
            )

            # Set on_close handler if supported
            if hasattr(window, "events") and hasattr(window.events, "closed"):
                window.events.closed += on_window_close
                logger.info("Registered window close handler")

            webview.start(func=lambda: None, debug=get_webview_debug())
            logger.info("Webview closed")

            # If we get here, it means the webview loop has ended
            # Make sure we exit
            on_window_close()
        else:
            logger.error("ERROR: The webview module doesn't have create_window attribute")
            logger.error(f"Available attributes: {dir(webview)}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"ERROR creating window: {e}")
        logger.exception("Traceback:")  # Use logger.exception to include traceback info
        sys.exit(1)
