import typer
from typing import Optional
from typer.models import Context
from zennix.commands import generate
from zennix.commands import scan
from zennix.version import __version__

app = typer.Typer(
    epilog="✨ Built with love by the Zennix team.",
    add_completion=False,
    )  # This sets up the CLI group

app.add_typer(generate.app, name="generate", help="Generate project files like README, usage docs, and more!")
app.command()(scan.scan)

@app.command()
def welcome(name: str = "Zennits"):
    """Welcome to Zennix World! Hope it'll help you out with your stuff."""
    typer.secho(f"👋 Hello, {name}!", fg=typer.colors.BRIGHT_MAGENTA, bold=True)

@app.callback(invoke_without_command=True)
def cli_callback(
    ctx: Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        is_eager=True,
    )
):
    """Zennix: AI-powered project setup CLI."""

    if version:
        # If user just asked for version, show only version and exit
        typer.secho(f"Zennix v{__version__} 🚀", fg=typer.colors.CYAN, bold=True)
        return

    if ctx.invoked_subcommand is None:
        # If user ran just `zennix`, show version + help
        typer.secho(f"Zennix v{__version__} 🚀", fg=typer.colors.CYAN, bold=True)
        typer.echo(ctx.get_help())
        return
    
def main():
    app()  # <-- Run the CLI group

if __name__ == "__main__":
    main()
