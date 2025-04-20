import os


def get_webview_debug() -> bool:
    return os.environ.get("STARFRUIT_WEBVIEW_DEBUG", "false").lower() == "true"
