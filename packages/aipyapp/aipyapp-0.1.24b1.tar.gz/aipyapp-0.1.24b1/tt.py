from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from rich.panel import Panel

class RichToTextual(App):
    def compose(self) -> ComposeResult:
        yield Static(Panel("Hello, [bold green]Textual[/]!"))
        yield Input(placeholder="What's your name?")

    def on_input_submitted(self, event: Input.Submitted):
        self.query_one(Static).update(f"Hello, [blue]{event.value}[/]!")

if __name__ == "__main__":
    app = RichToTextual()
    app.run()
