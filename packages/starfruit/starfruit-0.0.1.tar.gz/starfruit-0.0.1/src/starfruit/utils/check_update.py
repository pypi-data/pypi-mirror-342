import httpx
import packaging.version

from starfruit.logger import get_logger
from starfruit.utils.get_version import get_version

logger = get_logger(__name__)


def check_update(package_name: str) -> str | None:
    current_version_str = get_version()

    try:
        response = httpx.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5.0)
        response.raise_for_status()
        latest_version_str = response.json()["info"]["version"]

        current_version = packaging.version.parse(current_version_str)
        latest_version = packaging.version.parse(latest_version_str)

        if latest_version > current_version:
            return f"Update available → v{latest_version_str}\n\nRun: [bold]pipx upgrade {package_name}[/bold]"
        return None

    except httpx.RequestError as e:
        logger.warning(f"Update check failed: Network error - {e}")
        return None
    except Exception as e:
        logger.warning(f"Update check failed: Unexpected error - {e}")
        return None
