import logging
import threading
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.logging import TextualHandler
from textual.widgets import Button, Footer, Header, TabbedContent

from starfruit.app_logs import AppLogs
from starfruit.app_main import AppMain
from starfruit.logger import get_logger
from starfruit.server import API_HOST, API_PORT, run_server_in_thread
from starfruit.systray import launch_systray, terminate_systray
from starfruit.utils.check_update import check_update
from starfruit.utils.const import PACKAGE_NAME
from starfruit.utils.get_version import get_version
from starfruit.utils.internal_post import internal_post

SIMULATE_UPDATE = False
SERVER_URL = f"http://{API_HOST}:{API_PORT}"
GITHUB_REPO = "substratelabs/starfruit"

logging.basicConfig(
    level="DEBUG",
    handlers=[TextualHandler()],
)
logger = get_logger(__name__)


class StarfruitApp(App):
    TITLE = f"✧ starfruit v{get_version()}"
    BINDINGS = [
        Binding(
            key="ctrl+c",
            action="quit",
            description="Quit App",
            show=True,
        ),
        Binding(
            key="ctrl+g",
            action="open_github",
            description="github.com/substratelabs/starfruit",
            show=True,
        ),
    ]
    CSS_PATH = ["app.tcss"]

    server_thread: Optional[threading.Thread] = None
    app_main_ref: Optional[AppMain] = None

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent("✦ menu", "✧ logs", id="main"):
            yield AppMain(self, id="main-tab")
            yield AppLogs(id="logs-tab")

        yield Footer()

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"

        try:
            self.app_main_ref = self.query_one("#main-tab", AppMain)
        except NoMatches:
            logger.error("could not find main tab")

        self.server_thread = run_server_in_thread()
        if self.server_thread:
            logger.info(f"server thread started: {self.server_thread.ident}")
        else:
            logger.error("failed to start server thread.")

        systray_launched = launch_systray(
            webapp_host=API_HOST,
            webapp_port=API_PORT,
            api_host=API_HOST,
            api_port=API_PORT,
            version=get_version(),
        )
        if systray_launched:
            logger.info("systray launched successfully.")
        else:
            logger.error("failed to launch systray.")

        self.run_worker(self._check_for_updates_worker, thread=True, name="UpdateCheck")

    def action_launch_webview(self) -> None:
        thread = threading.Thread(target=self._launch_webview_in_thread, daemon=True)
        thread.start()

    def _launch_webview_in_thread(self) -> None:
        try:
            response = internal_post("/webview/launch", caller_logger=logger)
            if response:
                try:
                    result = response.json()
                    status = result.get("status")
                    message = result.get("message")

                    if status in ["launching", "focused", "already_running"]:
                        logger.info(
                            f"(Thread) webview launch/focus command successful. status: {status}, message: {message}"
                        )
                    else:
                        logger.warning(
                            f"(Thread) webview launch command returned unexpected status: {status}, message: {message}"
                        )
                except Exception as e:
                    logger.error(
                        f"(Thread) Error processing webview launch response: {e}", exc_info=True
                    )
            else:
                logger.error("(Thread) Failed to launch webview via API.")

        except Exception as e:
            logger.error(f"(Thread) Unexpected error launching webview via API: {e}", exc_info=True)

    def _check_for_updates_worker(self):
        """Worker to check for updates and update UI if needed."""
        logger.debug("Update check worker started.")
        update_message = check_update(PACKAGE_NAME)
        if SIMULATE_UPDATE:
            update_message = (
                f"Update available → v2.0.0\n\nRun: [bold]pipx upgrade {PACKAGE_NAME}[/bold]"
            )

        if update_message and self.app_main_ref:
            self.call_from_thread(self.app_main_ref.show_alert, update_message)
        else:
            logger.debug("no update found")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_name = event.button.name
        if button_name == "open_webapp":
            self.action_launch_webview()

    def action_open_github(self) -> None:
        thread = threading.Thread(target=self._open_github_in_thread, daemon=True)
        thread.start()

    def _open_github_in_thread(self) -> None:
        github_url = f"https://github.com/{GITHUB_REPO}"
        logger.info(f"Requesting to open GitHub URL: {github_url}")
        try:
            response = internal_post(
                "/open_url", json_data={"url": github_url}, caller_logger=logger
            )
            if response:
                try:
                    result = response.json()
                    logger.info(
                        f"(Thread) Open URL request successful: {result.get('message', 'No message')}"
                    )
                except Exception as e:
                    logger.error(f"(Thread) Error processing open URL response: {e}", exc_info=True)
            else:
                logger.error(f"(Thread) Failed to open URL {github_url} via API.")

        except Exception as e:
            logger.error(
                f"(Thread) Unexpected error opening URL {github_url} via API: {e}", exc_info=True
            )


if __name__ == "__main__":
    app = StarfruitApp()
    try:
        app.run()
    except Exception as e:
        logger.error(f"CRITICAL ERROR in main app loop: {e}", exc_info=True)
    finally:
        logger.info("application has finished running.")
        try:
            terminate_systray()
        except Exception as term_e:
            logger.error(f"error terminating systray during final cleanup: {term_e}")
