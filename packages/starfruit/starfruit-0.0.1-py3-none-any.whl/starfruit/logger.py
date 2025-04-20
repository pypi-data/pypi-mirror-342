import logging
import sys
import time

from starfruit.utils.get_app_dir import get_app_dir

APP_DIR = get_app_dir()
LOG_FILE = APP_DIR / "starfruit_session.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_log_formatter = None
_file_handler = None
_console_handler = None
_handlers_initialized = False


def _initialize_handlers():
    global _log_formatter, _file_handler, _console_handler, _handlers_initialized
    if _handlers_initialized:
        return

    class CustomFormatter(logging.Formatter):
        _level_map = {
            logging.DEBUG: "DBG",
            logging.INFO: "INF",
            logging.WARNING: "WRN",
            logging.ERROR: "ERR",
            logging.CRITICAL: "CRT",
        }

        def format(self, record):
            record.levelname = self._level_map.get(record.levelno, record.levelname[:3])
            if record.name.startswith("starfruit."):
                record.name = record.name[len("starfruit.") :]
            return super().format(record)

        def formatTime(self, record, datefmt=None):
            ct = self.converter(record.created)
            if datefmt:
                s = time.strftime(datefmt, ct)
            else:
                t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
                s = "%s,%03d" % (t, record.msecs)
            return s

    _log_formatter = CustomFormatter(
        fmt="%(asctime)s [%(levelname)-3s] [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    _file_handler.setFormatter(_log_formatter)
    _file_handler.setLevel(logging.DEBUG)

    _console_handler = logging.StreamHandler(sys.stderr)
    _console_handler.setFormatter(_log_formatter)
    _console_handler.setLevel(logging.DEBUG)

    _handlers_initialized = True
    logging.getLogger().addHandler(_file_handler)
    logging.getLogger().setLevel(logging.DEBUG)


def get_logger(name: str) -> logging.Logger:
    """Gets a logger instance configured with standard file and console handlers."""
    _initialize_handlers()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Loggers inherit handlers from the root logger by default.
    # We generally don't need to add handlers to individual loggers
    # unless we want specific behavior.
    # The root logger already has the file handler.
    # Console handler is managed by enable/disable functions.

    return logger


def enable_console_logging():
    """Adds the console handler to the root logger."""
    _initialize_handlers()
    root_logger = logging.getLogger()
    if _console_handler and _console_handler not in root_logger.handlers:
        root_logger.addHandler(_console_handler)
        get_logger(__name__).debug("Console logging ENABLED.")


def disable_console_logging():
    """Removes the console handler from the root logger."""
    _initialize_handlers()
    root_logger = logging.getLogger()
    if _console_handler and _console_handler in root_logger.handlers:
        root_logger.removeHandler(_console_handler)
        get_logger(__name__).debug("Console logging DISABLED.")


# --- Initial Setup --- #
_initialize_handlers()  # Initialize handlers when module is loaded
module_logger = get_logger(__name__)
# Console logging is OFF by default after initial load
disable_console_logging()
