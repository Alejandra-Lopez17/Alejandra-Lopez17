from interfaces.cli.main import app as cli_app
from interfaces.web.fastapi_app import create_app
import typer

web_app = create_app()


def main() -> None:
    """Entry point for the csds-352-vault command."""
    cli_app()


if __name__ == "__main__":
    main()
