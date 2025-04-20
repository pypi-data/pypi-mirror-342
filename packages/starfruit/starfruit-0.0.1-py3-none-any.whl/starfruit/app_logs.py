import platform
import subprocess
from io import StringIO
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Log, Static

from starfruit.logger import LOG_FILE, get_logger

logger = get_logger(__name__)


class AppLogs(Static):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._log_file_path: Path = LOG_FILE
        self._log_file_handle: StringIO | None = None
        self._last_log_position: int = 0

    def compose(self) -> ComposeResult:
        with Vertical(id="logs-container"):
            yield Log(highlight=True, auto_scroll=True, id="app-logs")
            yield Button("Open logs file", id="open-log-file-btn", name="open_log_file")

    def on_mount(self) -> None:
        # Load initial logs and start watching
        self._load_initial_logs()
        self.set_interval(0.5, self._watch_log_file)  # Check every 500ms

        # Add a startup message to help with debugging
        logger.debug("Logs panel initialized")

    def _load_initial_logs(self) -> None:
        log_widget = self.query_one("#app-logs", Log)
        try:
            with open(self._log_file_path, "r", encoding="utf-8") as f:
                log_content = f.read()
                log_widget.write(log_content)
                self._last_log_position = f.tell()
        except Exception as e:
            log_widget.write(f"Error loading log file {self._log_file_path}: {e}")
            logger.error(f"Error loading log file {self._log_file_path}: {e}")

    def _watch_log_file(self) -> None:
        """Periodically check the log file for new content and append it."""
        log_widget = self.query_one("#app-logs", Log)
        try:
            with open(self._log_file_path, "r", encoding="utf-8") as f:
                f.seek(self._last_log_position)
                new_content = f.read()
                if new_content:
                    log_widget.write(new_content)
                    self._last_log_position = f.tell()
        except Exception as e:
            logger.error(f"Error reading log file {self._log_file_path}: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.name == "open_log_file":
            self.action_open_log_file()

    def action_open_log_file(self) -> None:
        """Opens the log file using the default system application."""
        log_file_path = LOG_FILE
        try:
            logger.debug(f"Attempting to open log file: {log_file_path}")
            if platform.system() == "Windows":
                subprocess.Popen(["start", str(log_file_path)], shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", str(log_file_path)])
            else:  # Linux and other Unix-like systems
                subprocess.Popen(["xdg-open", str(log_file_path)])
        except Exception as e:
            logger.error(f"Failed to open log file {log_file_path}: {e}")
