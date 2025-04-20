#!/usr/bin/env python
"""
system tray process
https://pystray.readthedocs.io/en/latest/usage.html
"""

import argparse
import atexit
import os
import signal
import threading
import time

import psutil
import pystray
from PIL import Image, ImageDraw

from starfruit.logger import enable_console_logging, get_logger
from starfruit.utils.internal_post import internal_post

ICON_UPDATE_INTERVAL_S = 1
ICON_UPDATE_ERROR_WAIT_S = 5
PARENT_MONITOR_INTERVAL_S = 1
CLEANUP_WAIT_S = 0.1

logger = get_logger(__name__)

parser = argparse.ArgumentParser(description="starfruit systray process")
parser.add_argument("--host", type=str, default="127.0.0.1", help="App host")
parser.add_argument("--port", type=str, default="8023", help="App port")
parser.add_argument("--api-host", type=str, default="127.0.0.1", help="API host")
parser.add_argument("--api-port", type=str, default="8022", help="API port")
parser.add_argument("--version", type=str, default="0.0.1", help="App version")
parser.add_argument("--parent-pid", type=str, help="Parent process ID to monitor")
args = parser.parse_args()

WEBAPP_URL = f"http://{args.host}:{args.port}"
VERSION = args.version

icon = None
shutting_down = False
parent_pid = None

# Initialize parent PID
if args.parent_pid:
    try:
        parent_pid = int(args.parent_pid)
    except ValueError:
        logger.warning(f"Invalid parent PID provided: {args.parent_pid}")
else:
    parent_pid = os.getppid()
    logger.info(f"Using parent process PID: {parent_pid}")


def create_tray_icon():
    width, height = 22, 22
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    center_x, center_y = width // 2, height // 2

    # Define diamond points (taller than wide)
    top_point = (center_x, 1)
    bottom_point = (center_x, height - 2)
    left_point = (center_x - (width // 4), center_y)
    right_point = (center_x + (width // 4), center_y)

    diamond_points = [top_point, right_point, bottom_point, left_point]

    # Draw the diamond
    draw.polygon(diamond_points, fill=(0, 0, 0, 255), outline=(255, 255, 255, 255), width=1)

    return image


def create_square_icon():
    """Creates a square icon image."""
    width, height = 22, 22
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Define square points (inset slightly)
    top_left = (2, 2)
    bottom_right = (width - 3, height - 3)

    # Draw the square
    draw.rectangle(
        [top_left, bottom_right], fill=(0, 0, 0, 255), outline=(255, 255, 255, 255), width=1
    )

    return image


def on_open_window(icon, item):
    try:
        response = internal_post("/webview/launch", caller_logger=logger)
        if not response:
            logger.error("Failed to request webview launch.")
    except Exception as e:
        logger.error(f"Unexpected error during webview launch request: {e}")


def monitor_parent_process():
    """Monitor the parent process and exit if it terminates"""
    global shutting_down, parent_pid

    if parent_pid is None:
        logger.info("No parent PID to monitor")
        return

    logger.info(f"starting parent process monitor for PID: {parent_pid}")
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
                # This case can happen if the process exits between pid_exists and Process()
                logger.info("Parent process no longer exists (race condition), shutting down")
                shutting_down = True
                cleanup()
                os._exit(0)  # Force exit

        except Exception as e:
            logger.error(f"Error monitoring parent process: {e}")
            # Don't exit on monitoring errors

        # Check every second
        time.sleep(PARENT_MONITOR_INTERVAL_S)


def update_icon_periodically(icon_obj):
    """Periodically updates the icon between diamond and square."""
    global shutting_down
    use_diamond = True
    while not shutting_down:
        try:
            if use_diamond:
                icon_obj.icon = create_tray_icon()
            else:
                icon_obj.icon = create_square_icon()
            icon_obj.update_menu()
            use_diamond = not use_diamond
            time.sleep(ICON_UPDATE_INTERVAL_S)
        except Exception as e:
            # Avoid crashing the update thread on errors
            logger.error(f"Error updating icon: {e}", exc_info=True)
            time.sleep(ICON_UPDATE_ERROR_WAIT_S)  # Wait a bit longer after an error


def setup_icon():
    global icon

    logger.info("Setting up systray icon...")

    icon_image = create_tray_icon()
    logger.info("Creating pystray.Icon object.")
    icon = pystray.Icon("starfruit", icon=icon_image, title="starfruit")

    logger.info("Starting icon update thread.")
    threading.Thread(target=update_icon_periodically, args=(icon,), daemon=True).start()

    logger.info("Calling icon.run()...")
    try:
        icon.run()
        logger.info("icon.run() finished.")
    except Exception as e:
        logger.error(f"Error during icon.run(): {e}", exc_info=True)


def signal_handler(sig, frame):
    logger.info(f"Received signal {sig}, cleaning up.")
    cleanup()
    os._exit(0)


def cleanup():
    global icon, shutting_down
    if shutting_down:
        return
    logger.info("Cleanup requested.")
    shutting_down = True
    try:
        if icon:
            logger.info("Stopping icon...")
            icon.stop()
            logger.info("Waiting for icon to stop...")
            time.sleep(CLEANUP_WAIT_S)  # wait for icon to stop
            logger.info("Icon stopped.")
    except Exception as e:
        logger.error(f"error stopping icon: {e}", exc_info=True)


atexit.register(cleanup)


if __name__ == "__main__":
    enable_console_logging()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    threading.Thread(target=monitor_parent_process, daemon=True).start()
    setup_icon()
