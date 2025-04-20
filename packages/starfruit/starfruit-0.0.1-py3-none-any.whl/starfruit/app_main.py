from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.css.query import NoMatches
from textual.widgets import Button, Label, Static

from starfruit.logger import get_logger

logger = get_logger(__name__)


class AppMain(Static):
    def __init__(self, app_instance: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_instance = app_instance

    def compose(self) -> ComposeResult:
        yield Container(
            Label(id="alert-message-label", markup=True),
            id="alert-container",
            classes="hidden",
        )
        yield Container(
            Horizontal(
                Button(
                    label="✧  Chat  ✦",
                    id="open-webapp-btn",
                    variant="primary",
                    disabled=False,
                    name="open_webapp",
                ),
                id="webapp-buttons",
            ),
            id="webapp-container",
        )

    def show_alert(self, message: str) -> None:
        try:
            container = self.query_one("#alert-container", Container)
            label = self.query_one("#alert-message-label", Label)
            label.update(message)
            container.remove_class("hidden")
        except NoMatches:
            logger.error("could not find alert components")
