from starfruit.app import StarfruitApp
from starfruit.logger import get_logger

logger = get_logger(__name__)


def start():
    try:
        app = StarfruitApp()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start Starfruit: {e}")
        raise
