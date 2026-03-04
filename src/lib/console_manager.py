from typing import Any, Dict
from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status


def dict_to_markdown_table(dictionary: Dict[str, Any]) -> str:
    table = "| Key | Value |\n| --- | ----- |\n"
    for key, value in dictionary.items():
        table += f"| {key} | {value} |\n"
    return table


class ConsoleManager:
    def __init__(self) -> None:
        self.console = Console()

    def print_markdown(self, markdown: str) -> None:
        self.console.print(Markdown(markdown))

    def print_success(self, message: str) -> None:
        self.console.print(f"[bold green](success)[/bold green] {message}")

    def print_error(self, message: str) -> None:
        self.console.print(f"[bold red](error)[/bold red] {message}")

    def print_info(self, message: str) -> None:
        self.console.print(f"[bold blue](info)[/bold blue] {message}")

    def print_dict(self, dictionary: Dict[str, Any], header: str = "") -> None:
        markdown_table = dict_to_markdown_table(dictionary)
        if header:
            self.print_markdown(f"# {header}\n")

        self.console.print(Markdown(markdown_table))

    def status(self, message: str) -> Status:
        return self.console.status(f"[bold green]{message}[/bold green]")


console_manager = ConsoleManager()
