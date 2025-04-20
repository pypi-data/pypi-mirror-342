import logging
from typing import Any, Dict, Optional

import httpx

from starfruit.logger import get_logger
from starfruit.utils.const import API_HOST, API_PORT


def internal_post(
    endpoint: str,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: float = 10.0,
    caller_logger: Optional[logging.Logger] = None,
) -> Optional[httpx.Response]:
    request_logger = caller_logger or get_logger(__name__)

    url = f"http://{API_HOST}:{API_PORT}{endpoint}"
    request_logger.debug(f"Making internal API request to: {url}")
    try:
        response = httpx.post(url, json=json_data, timeout=timeout)
        response.raise_for_status()
        request_logger.debug(f"Internal API request to {endpoint} successful.")
        return response
    except httpx.RequestError as e:
        request_logger.error(f"API request error contacting {endpoint}: {e}", exc_info=True)
        return None
    except httpx.HTTPStatusError as e:
        request_logger.error(
            f"API request failed contacting {endpoint}: {e.response.status_code} - {e.response.text}",
            exc_info=True,
        )
        return None
    except Exception as e:
        request_logger.error(f"Unexpected error contacting {endpoint} via API: {e}", exc_info=True)
        return None
