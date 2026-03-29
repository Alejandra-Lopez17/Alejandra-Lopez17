from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status
from typing import Any, Dict, Optional


class ConsoleManager:
    def __init__(self) -> None:
        self.console = Console()
        self._last_message: Optional[str] = None

    def _print_unique(self, message: str, style: Optional[str] = None) -> None:
        if message != self._last_message:
            if style is not None:
                self.console.print(f"[{style}]{message}[/{style}]")
            else:
                self.console.print(message)
            self._last_message = message

    def print_markdown(self, markdown: str) -> None:
        self._print_unique(markdown)

    def print_success(self, message: str) -> None:
        self._print_unique(f"✓ {message}", "bold green")

    def print_error(self, message: str) -> None:
        self._print_unique(f"✗ {message}", "bold red")

    def print_info(self, message: str) -> None:
        self._print_unique(f"ℹ {message}", "bold blue")

    def print_warning(self, message: str) -> None:
        self._print_unique(f"⚠ {message}", "bold yellow")

    def print_dict(self, dictionary: Dict[str, Any], header: str = "") -> None:
        table = "| Key | Value |\n| --- | ----- |\n"
        for key, value in dictionary.items():
            table += f"| {key} | {value} |\n"
        if header:
            self.print_markdown(f"### {header}\n{table}")
        else:
            self.print_markdown(table)

    def status(self, message: str) -> Status:
        return self.console.status(f"[bold green]{message}[/bold green]")


console_manager = ConsoleManager()
